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
        first = target.read_bytes()
        package.build(self.root, draft=True)
        self.assertEqual(first, target.read_bytes())
        self.assertIn('demo_recording_url', missing)
        self.assertIn('oauth_runtime_passed', pending)
        with zipfile.ZipFile(target) as archive:
            self.assertEqual(set(archive.namelist()), package.FILES)
            self.assertNotIn(b'PRIVATE_TEST_SENTINEL', b''.join(archive.read(n) for n in archive.namelist()))
            self.assertNotIn('.mcp.json', archive.namelist())

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
        image.symlink_to(self.root / 'plugins/octolane-ai-crm/assets/logo.png')
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
        self.edit(self.root / 'plugins/octolane-ai-crm/.codex-plugin/plugin.json', lambda d: d['interface'].update({'displayName': 'Different'}))
        with self.assertRaisesRegex(ValueError, 'listing drift'):
            package.validate(self.root)

    def test_duplicate_json_key_rejected(self):
        (self.source / 'mcp.json').write_text('{"mcpServers": {}, "mcpServers": {}}')
        with self.assertRaisesRegex(ValueError, 'Duplicate JSON key'):
            package.validate(self.root)

    def test_local_marketplace_cannot_switch_to_public_package(self):
        self.edit(self.root / '.agents/plugins/marketplace.json', lambda d:
                  d['plugins'][0]['source'].update({'path': './submission/octolane-ai-crm'}))
        with self.assertRaisesRegex(ValueError, 'Local marketplace'):
            package.validate(self.root)

    def test_local_key_uses_native_bearer_environment_binding(self):
        path = self.root / 'plugins/octolane-ai-crm/.mcp.json'
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
