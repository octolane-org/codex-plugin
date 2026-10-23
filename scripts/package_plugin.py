#!/usr/bin/env python3
"""Offline Octolane package checks/build. Does not certify portal acceptance."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import sys
from urllib.parse import urlsplit
import zipfile
import zlib

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path('submission/octolane-ai-crm')
FILES = {'plugin.json', 'mcp.json', 'assets/logo.png', 'assets/icon.png'}
GATES = {
    'publisher_verified', 'countries_languages_confirmed', 'listing_urls_verified',
    'privacy_coverage_approved', 'oauth_runtime_passed', 'live_72_tool_contracts_passed',
    'tenant_role_subscription_tests_passed', 'tool_annotations_approved',
    'review_cases_passed', 'demo_recording_verified', 'reviewer_access_verified',
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, f'Duplicate JSON key: {key}')
            result[key] = value
        return result
    return json.loads(path.read_text(), object_pairs_hook=unique)


def https(value):
    require(isinstance(value, str) and len(value) <= 1024, 'Invalid URL type/length')
    url = urlsplit(value)
    require(url.scheme == 'https' and url.hostname and not url.username and not url.password,
            'Expected HTTPS URL without credentials')


def check_png(data, minimum):
    require(data[:8] == b'\x89PNG\r\n\x1a\n' and len(data) <= 5 * 1024 * 1024,
            'Invalid or oversized PNG')
    offset, dimensions, ended = 8, None, False
    while offset + 12 <= len(data):
        length = struct.unpack('>I', data[offset:offset + 4])[0]
        end = offset + 12 + length
        require(end <= len(data), 'Truncated PNG')
        kind = data[offset + 4:offset + 8]
        content = data[offset + 8:end - 4]
        crc = struct.unpack('>I', data[end - 4:end])[0]
        require(zlib.crc32(kind + content) & 0xffffffff == crc, 'PNG checksum mismatch')
        if offset == 8:
            require(kind == b'IHDR' and length == 13, 'Missing PNG header')
            dimensions = struct.unpack('>II', content[:8])
        offset = end
        if kind == b'IEND':
            ended = True
            break
    require(ended and offset == len(data), 'Missing PNG end or trailing data')
    require(dimensions and minimum <= dimensions[0] == dimensions[1] <= 4096,
            'PNG must be square and within required dimensions')


def validate(root=ROOT, release=False):
    package = root / PACKAGE
    require(not package.is_symlink() and not package.parent.is_symlink(),
            'Symlink package directory forbidden')
    members = list(package.rglob('*'))
    require(not any(p.is_symlink() for p in members), 'Symlinks forbidden in public package')
    actual = {p.relative_to(package).as_posix() for p in members if p.is_file()}
    require(actual == FILES, f'Unexpected/missing public package files: {sorted(actual ^ FILES)}')
    manifest = read_json(package / 'plugin.json')
    mcp = read_json(package / 'mcp.json')
    require(set(manifest) <= {'$schema', 'name', 'version', 'description', 'author',
                              'homepage', 'repository', 'license', 'keywords', 'extensions'},
            'Unexpected manifest fields')
    require(manifest['$schema'] == 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json',
            'Wrong portable manifest schema')
    require(manifest['name'] == 'octolane-ai-crm', 'Plugin identity changed')
    require(re.fullmatch(r'\d+\.\d+\.\d+', manifest['version']), 'Expected release SemVer')
    require(not ({'apps', 'interface', 'mcpServers', 'skills'} & manifest.keys()),
            'Legacy fields are not allowed in portable manifest')
    ext = manifest['extensions']['com.openai']
    require(set(ext) <= {'interface', 'review', 'publication'}, 'Unexpected OpenAI extension')
    ui = ext['interface']
    require(set(ui) <= {'displayName', 'shortDescription', 'longDescription', 'developerName',
                        'category', 'composerIcon', 'logo', 'capabilities', 'websiteURL',
                        'supportURL', 'privacyPolicyURL', 'termsOfServiceURL', 'brandColor',
                        'defaultPrompt'}, 'Unexpected listing fields')
    require(set(ext['review']) <= {'test_cases', 'demo_recording_url'},
            'Unexpected review fields; keep credentials outside the package')
    for key, maximum in [('displayName', 30), ('shortDescription', 30),
                         ('longDescription', 4000), ('developerName', 80)]:
        value = ui[key]
        require(isinstance(value, str) and value.strip() and len(value) <= maximum,
                f'Invalid listing field: {key}')
    require(ui['category'] == 'Business & Operations', 'Incorrect submission category')
    prompts = ui['defaultPrompt']
    require(isinstance(prompts, list) and 1 <= len(prompts) <= 3, 'Expected 1-3 prompts')
    for p in prompts:
        require(isinstance(p, str) and p.strip() and len(p) <= 128
                and '\n' not in p and '\r' not in p and '@' not in p, 'Invalid starter prompt')
    require(len({' '.join(p.split()) for p in prompts}) == len(prompts), 'Duplicate prompt')
    missing = []
    for key in ('websiteURL', 'supportURL', 'privacyPolicyURL', 'termsOfServiceURL'):
        if key not in ui:
            missing.append(key)
        else:
            https(ui[key])
    for key, file, minimum in [('logo', 'assets/logo.png', 256), ('composerIcon', 'assets/icon.png', 48)]:
        require(ui[key] in (file, './' + file), f'Unexpected asset path: {key}')
        check_png((package / file).read_bytes(), minimum)
    local = read_json(root / 'plugins/octolane-ai-crm/.codex-plugin/plugin.json')
    require(local.get('mcpServers') == './.mcp.json', 'Local MCP reference changed')
    local_mcp = read_json(root / 'plugins/octolane-ai-crm/.mcp.json')
    require(local_mcp == {'mcpServers': {'octolane': {
        'url': 'https://mcp.octolane.com/mcp',
        'bearer_token_env_var': 'OCTOLANE_API_KEY'}}},
        'Local API-key compatibility contract changed')
    marketplace = read_json(root / '.agents/plugins/marketplace.json')
    require(len(marketplace['plugins']) == 1 and marketplace['plugins'][0]['name'] == manifest['name']
            and marketplace['plugins'][0]['source'] == {
                'source': 'local', 'path': './plugins/octolane-ai-crm'},
            'Local marketplace must retain compatibility package')
    require(local['name'] == manifest['name'] and local['version'] == manifest['version'],
            'Local/public identity or version drift')
    require(local['interface'] == ui, 'Local/public listing drift')
    for file in ('assets/icon.png', 'assets/logo.png'):
        require((package / file).read_bytes() == (root / 'plugins/octolane-ai-crm' / file).read_bytes(),
                'Local/public asset drift')
    require(mcp['$schema'] == 'https://agent-plugins.org/schemas/1.0.0/mcp.schema.json',
            'Wrong MCP schema')
    require(set(mcp) == {'$schema', 'mcpServers'} and set(mcp['mcpServers']) == {'octolane'},
            'Unexpected MCP servers or fields')
    server = mcp['mcpServers']['octolane']
    require(set(server) == {'type', 'url'},
            'Public MCP config must not contain headers, credentials, or tool filters')
    require(server['type'] == 'streamable-http' and server['url'] == 'https://mcp.octolane.com/mcp',
            'Unexpected MCP endpoint/transport')
    tools = read_json(root / 'docs/tool-inventory.json')['tools']
    names = {t['name'] for t in tools}
    require(len(tools) == len(names) == 72, 'Expected 72 distinct existing tools')
    cases = ext['review']['test_cases']
    require(len(cases['positive']) == 5 and len(cases['negative']) == 3,
            'Expected five positive and three negative review cases')
    for group in ('positive', 'negative'):
        for case in cases[group]:
            fields = {'description', 'prompt'}
            if group == 'positive':
                fields |= {'tools_triggered', 'expected_behavior'}
            require(set(case) == fields, 'Unexpected review-case fields')
            require(all(isinstance(case[k], str) and case[k].strip() for k in fields),
                    'Review case fields must be nonblank strings')
            if group == 'positive':
                require(set(case['tools_triggered'].split(', ')) <= names,
                        'Review case references tools absent from inventory')
    gates = read_json(root / 'docs/release-gates.json')['gates']
    require(set(gates) == GATES, 'Missing or unexpected release gates')
    pending = [k for k, v in gates.items() if v.get('status') != 'passed' or not v.get('evidence', '').strip()]
    demo = ext['review'].get('demo_recording_url')
    if demo:
        https(demo)
    else:
        missing.append('demo_recording_url')
    if release:
        require(not missing and not pending,
                f'Release blocked: missing {missing}; unverified gates {pending}')
    return manifest, missing, pending


def build(root=ROOT, draft=False):
    manifest, missing, pending = validate(root, release=not draft)
    package = root / PACKAGE
    output = root / 'dist'
    output.mkdir(exist_ok=True)
    label = '-draft' if draft else ''
    target = output / f"{manifest['name']}-{manifest['version']}{label}.zip"
    contents = {name: (package / name).read_bytes() for name in sorted(FILES)}
    with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in contents.items():
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    with zipfile.ZipFile(target) as archive:
        require(set(archive.namelist()) == FILES and archive.testzip() is None,
                'Archive inventory/integrity mismatch')
        require(all(archive.read(name) == data for name, data in contents.items()),
                'Archive bytes differ from source')
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    target.with_suffix('.sha256').write_text(f'{digest}  {target.name}\n')
    return target, missing, pending


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['validate', 'build'])
    parser.add_argument('--draft', action='store_true', help='Build an explicitly incomplete draft archive')
    parser.add_argument('--release', action='store_true', help='Also require recorded release evidence')
    args = parser.parse_args()
    try:
        require(not (args.draft and args.release), 'Choose draft or release, not both')
        if args.command == 'build':
            target, missing, pending = build(draft=args.draft)
            print(target)
        else:
            _, missing, pending = validate(release=args.release)
            print('Repository static checks passed; not an OpenAI approval or runtime test.')
        if missing or pending:
            print(f'NOT SUBMISSION READY: missing {missing}; pending {pending}')
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
