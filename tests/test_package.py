import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('package_plugin', ROOT / 'scripts/package_plugin.py')
package = importlib.util.module_from_spec(spec)
spec.loader.exec_module(package)


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for directory in ('submission', 'plugins', 'docs', '.agents'):
            shutil.copytree(ROOT / directory, self.root / directory)
        self.source = self.root / package.PACKAGE

    def edit(self, path, change):
        data = json.loads(path.read_text())
        change(data)
        path.write_text(json.dumps(data))

    def test_draft_is_deterministic_and_contains_only_public_files(self):
        (self.root / '.env').write_text('PRIVATE_TEST_SENTINEL')
        target, missing, pending = package.build(self.root, draft=True)
        self.assertEqual(target.name, 'octolane-1.0.0-draft.zip')
        first = target.read_bytes()
        package.build(self.root, draft=True)
        self.assertEqual(first, target.read_bytes())
        self.assertIn('demo_recording_url', missing)
        self.assertIn('oauth_runtime_passed', pending)
        with zipfile.ZipFile(target) as archive:
            self.assertEqual(set(archive.namelist()), package.FILES)
            self.assertNotIn(b'PRIVATE_TEST_SENTINEL', b''.join(archive.read(n) for n in archive.namelist()))
            self.assertNotIn('.mcp.json', archive.namelist())
            self.assertEqual(json.loads(archive.read('plugin.json'))['name'], 'octolane')

    def test_light_and_dark_slots_share_the_expected_archive_assets(self):
        target, _, _ = package.build(self.root, draft=True)
        with zipfile.ZipFile(target) as archive:
            self.assertEqual(set(archive.namelist()), package.FILES)
            ui = json.loads(archive.read('plugin.json'))['extensions']['com.openai']['interface']
            for key, name in [('logo', 'logo.png'), ('composerIcon', 'composer-icon.svg'),
                              ('logoDark', 'logo-dark.png'),
                              ('composerIconDark', 'composer-icon-dark.svg')]:
                self.assertEqual(ui[key], './assets/' + name)
                self.assertEqual(archive.read('assets/' + name),
                                 (self.root / 'plugins/octolane/assets' / name).read_bytes())

    def test_dark_asset_is_required_and_must_be_valid(self):
        path = self.source / 'assets/logo-dark.png'
        original = path.read_bytes()
        path.unlink()
        with self.assertRaisesRegex(ValueError, 'package files'):
            package.build(self.root, draft=True)
        path.write_bytes(b'not a PNG')
        with self.assertRaisesRegex(ValueError, 'PNG'):
            package.validate(self.root)
        path.write_bytes(original)
        local = self.root / 'plugins/octolane/assets/logo-dark.png'
        local.write_bytes((self.source / 'assets/logo.png').read_bytes())
        with self.assertRaisesRegex(ValueError, 'asset drift'):
            package.validate(self.root)

    def test_dark_paths_cannot_escape_or_reference_other_assets(self):
        path = self.source / 'plugin.json'
        original = path.read_text()
        for key in ('logoDark', 'composerIconDark'):
            for value in ('../logo-dark.png', '/tmp/logo-dark.png', './assets/logo.png',
                          'https://example.com/logo.png'):
                with self.subTest(key=key, value=value):
                    self.edit(path, lambda d: d['extensions']['com.openai']['interface'].update({key: value}))
                    with self.assertRaisesRegex(ValueError, 'Unexpected asset path'):
                        package.validate(self.root)
                    path.write_text(original)

    def test_source_and_macos_junk_are_rejected(self):
        for name in ('assets/logo.svg', 'assets/icon.png', '.DS_Store', '__MACOSX/._logo.png'):
            with self.subTest(name=name):
                path = self.source / name
                path.parent.mkdir(exist_ok=True)
                path.write_text('unwanted')
                with self.assertRaisesRegex(ValueError, 'package files'):
                    package.build(self.root, draft=True)
                path.unlink()

    def test_release_refuses_unverified_runtime(self):
        with self.assertRaisesRegex(ValueError, 'Release blocked'):
            package.build(self.root)
        self.assertFalse((self.root / 'dist').exists())

    def test_cannot_remove_release_gate(self):
        self.edit(self.root / 'docs/release-gates.json', lambda d: d['gates'].pop('oauth_runtime_passed'))
        with self.assertRaisesRegex(ValueError, 'release gates'):
            package.validate(self.root)

    def test_hidden_override_and_secret_files_rejected(self):
        for name in ('.app.json', '.env', '.mcp.json'):
            with self.subTest(name=name):
                path = self.source / name
                path.write_text('{}')
                with self.assertRaisesRegex(ValueError, 'package files'):
                    package.build(self.root, draft=True)
                path.unlink()

    def test_symlink_rejected(self):
        image = self.source / 'assets/logo.png'
        image.unlink()
        image.symlink_to(self.root / 'plugins/octolane/assets/logo.png')
        with self.assertRaisesRegex(ValueError, 'Symlinks'):
            package.validate(self.root)

    def test_api_header_or_tool_subset_rejected(self):
        path = self.source / 'mcp.json'
        initial = path.read_text()
        for key, value in [('headers', {'X-API-Key': 'dummy'}), ('enabled_tools', ['search_deals'])]:
            with self.subTest(key=key):
                self.edit(path, lambda d: d['mcpServers']['octolane'].update({key: value}))
                with self.assertRaisesRegex(ValueError, 'headers, credentials, or tool filters'):
                    package.validate(self.root)
                path.write_text(initial)

    def test_duplicate_tool_inventory_rejected(self):
        self.edit(self.root / 'docs/tool-inventory.json', lambda d: d['tools'].__setitem__(1, d['tools'][0]))
        with self.assertRaisesRegex(ValueError, '72 distinct'):
            package.validate(self.root)

    def test_unknown_review_tool_rejected(self):
        self.edit(self.source / 'plugin.json', lambda d: d['extensions']['com.openai']['review']['test_cases']['positive'][0].update({'tools_triggered': 'imaginary_tool'}))
        with self.assertRaisesRegex(ValueError, 'absent from inventory'):
            package.validate(self.root)

    def test_corrupted_png_rejected(self):
        path = self.source / 'assets/logo.png'
        data = bytearray(path.read_bytes())
        data[50] ^= 1
        path.write_bytes(data)
        with self.assertRaisesRegex(ValueError, 'checksum'):
            package.validate(self.root)

    def test_listing_drift_rejected(self):
        self.edit(self.root / 'plugins/octolane/.codex-plugin/plugin.json', lambda d: d['interface'].update({'displayName': 'Different'}))
        with self.assertRaisesRegex(ValueError, 'listing drift'):
            package.validate(self.root)

    def skill(self, name='get-started'):
        return self.source / 'skills' / name

    def rewrite(self, path, old, new):
        text = path.read_text()
        self.assertIn(old, text)
        path.write_text(text.replace(old, new, 1))

    def test_all_seventeen_skills_ship_with_their_dependency_file(self):
        self.assertEqual(len(package.SKILLS), 17)
        target, _, _ = package.build(self.root, draft=True)
        with zipfile.ZipFile(target) as archive:
            names = set(archive.namelist())
            for skill in package.SKILLS:
                self.assertIn(f'skills/{skill}/agents/openai.yaml', names)
                self.assertEqual(archive.read(f'skills/{skill}/SKILL.md'),
                                 (self.skill(skill) / 'SKILL.md').read_bytes())

    def test_missing_extra_and_junk_skill_files_are_rejected(self):
        (self.skill() / 'SKILL.md').unlink()
        with self.assertRaisesRegex(ValueError, 'package files'):
            package.validate(self.root)
        for name in ('skills/extra/SKILL.md', 'skills/get-started/.DS_Store',
                     'skills/get-started/references/notes.md'):
            with self.subTest(name=name):
                path = self.source / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('unwanted')
                with self.assertRaisesRegex(ValueError, 'package files'):
                    package.validate(self.root)
                path.unlink()

    def test_skill_name_must_match_its_folder(self):
        self.rewrite(self.skill() / 'SKILL.md', 'name: get-started', 'name: other-skill')
        with self.assertRaisesRegex(ValueError, 'must equal its folder'):
            package.validate(self.root)

    def test_skill_needs_frontmatter_and_a_plain_description(self):
        path = self.skill() / 'SKILL.md'
        original = path.read_text()
        cases = {
            'frontmatter': original.replace('---\n', '', 1),
            'colon': original.replace('description: ', 'description: Use it: ', 1),
            'length': original.replace('description: ', 'description: ' + 'x' * 1030 + ' ', 1),
            'quote': original.replace('description: ', 'description: "', 1),
        }
        for label, text in cases.items():
            with self.subTest(label=label):
                path.write_text(text)
                with self.assertRaisesRegex(ValueError, 'Skill get-started'):
                    package.validate(self.root)
        path.write_text(original)

    def test_skill_dependency_file_is_pinned_to_the_octolane_server(self):
        path = self.skill() / 'agents/openai.yaml'
        original = path.read_text()
        for old, new in [('value: "octolane"', 'value: "other"'),
                         ('streamable_http', 'sse'),
                         ('https://mcp.octolane.com/mcp', 'https://example.com/mcp'),
                         ('short_description: "', 'short_description: "' + 'x' * 70)]:
            with self.subTest(old=old):
                path.write_text(original.replace(old, new))
                with self.assertRaisesRegex(ValueError, 'openai.yaml'):
                    package.validate(self.root)
        path.write_text(original)

    def test_onboarding_skill_and_category_are_pinned(self):
        path = self.source / 'plugin.json'
        original = path.read_text()
        self.edit(path, lambda d: d['extensions']['com.openai'].update(
            {'onboardingSkill': './skills/my-tasks/SKILL.md'}))
        with self.assertRaisesRegex(ValueError, 'onboarding skill'):
            package.validate(self.root)
        path.write_text(original)
        self.edit(path, lambda d: d['extensions']['com.openai']['interface'].update(
            {'category': 'Business & Operations'}))
        with self.assertRaisesRegex(ValueError, 'category'):
            package.validate(self.root)

    def test_brand_colors_must_be_hex(self):
        path = self.source / 'plugin.json'
        original = path.read_text()
        for key in ('brandColor', 'brandColorDark'):
            with self.subTest(key=key):
                self.edit(path, lambda d: d['extensions']['com.openai']['interface'].update(
                    {key: 'black'}))
                with self.assertRaisesRegex(ValueError, 'listing color'):
                    package.validate(self.root)
                path.write_text(original)

    def test_unsafe_or_malformed_svg_is_rejected(self):
        path = self.source / 'assets/composer-icon.svg'
        original = path.read_text()
        square = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 8 8">%s</svg>'
        cases = {
            'script': square % '<script>alert(1)</script>',
            'handler': square % '<rect width="8" height="8" onload="x()"/>',
            'link': square % '<image href="https://example.com/x.png"/>',
            'external fill': square % '<rect width="8" height="8" fill="url(https://example.com/x)"/>',
            'entity': '<!DOCTYPE svg [<!ENTITY a "b">]>' + square % '<rect width="8" height="8"/>',
            'not square': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 8 4"></svg>',
            'no namespace': '<svg viewBox="0 0 8 8"><rect width="8" height="8"/></svg>',
            'not svg': 'plain text',
        }
        for label, text in cases.items():
            with self.subTest(label=label):
                path.write_text(text)
                with self.assertRaises(ValueError):
                    package.validate(self.root)
        path.write_text(original)
        package.validate(self.root)

    def test_composer_icon_drift_between_packages_is_rejected(self):
        local = self.root / 'plugins/octolane/assets/composer-icon.svg'
        local.write_text(local.read_text() + '\n')
        with self.assertRaisesRegex(ValueError, 'asset drift'):
            package.validate(self.root)

    def test_visitors_skill_filters_in_the_tool_call(self):
        text = (self.skill('website-visitors-to-pipeline') / 'SKILL.md').read_text()
        for parameter in ('last_visited_after', 'min_intent', 'crm_status', 'page_contains'):
            self.assertIn(f'`{parameter}`', text)
        self.assertIn('Do not call `search_accounts` or `search_deals` for each company', text)

    def test_duplicate_json_key_rejected(self):
        (self.source / 'mcp.json').write_text('{"mcpServers": {}, "mcpServers": {}}')
        with self.assertRaisesRegex(ValueError, 'Duplicate JSON key'):
            package.validate(self.root)

    def test_local_marketplace_cannot_switch_to_public_package(self):
        self.edit(self.root / '.agents/plugins/marketplace.json', lambda d:
                  d['plugins'][0]['source'].update({'path': './submission/octolane'}))
        with self.assertRaisesRegex(ValueError, 'Local marketplace'):
            package.validate(self.root)

    def test_local_key_uses_native_bearer_environment_binding(self):
        path = self.root / 'plugins/octolane/.mcp.json'
        server = json.loads(path.read_text())['mcpServers']['octolane']
        self.assertEqual(server.get('bearer_token_env_var'), 'OCTOLANE_API_KEY')
        self.assertNotIn('headers', server)
        self.assertNotIn('http_headers', server)
        original = path.read_text()
        # The native config contract must reject both the original unsupported
        # header path and inline secret/template values, not just missing auth.
        for auth in ({}, {'headers': {'X-API-Key': '${OCTOLANE_API_KEY}'}},
                     {'headers': {'Authorization': 'Bearer ${OCTOLANE_API_KEY}'}},
                     {'http_headers': {'Authorization': 'Bearer synthetic-secret'}}):
            with self.subTest(auth=auth):
                path.write_text(json.dumps({'mcpServers': {'octolane': {
                    'url': server['url'], **auth}}}))
                with self.assertRaisesRegex(ValueError, 'Local API-key'):
                    package.validate(self.root)
                path.write_text(original)


if __name__ == '__main__':
    unittest.main()
