#!/usr/bin/env python3
"""Validate portable sources and optionally ZIP bytes against published schemas."""
import argparse
import copy
import json
from pathlib import Path
import sys
import zipfile

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def validate_documents(documents, root=ROOT):
    errors = []
    # OpenAI documents this extension, while the unmodified generic MCP
    # schema forbids it. Validate the exact supported auth profile first,
    # then validate the transport projection; never strip unknown extensions.
    documents = copy.deepcopy(documents)
    for server_name, server in documents['mcp']['mcpServers'].items():
        expected = {'com.openai': {'auth': {'type': 'oauth', 'baseScopes': ['crm:read', 'crm:write'], 'defaultScopes': []}}}
        if server.get('extensions') != expected:
            errors.append(f'mcp.json/mcpServers/{server_name}: expected read/write OpenAI OAuth declaration without credentials or overrides')
        else:
            server.pop('extensions')
    for name in ('plugin', 'mcp'):
        schema = json.loads((root / 'schemas/agent-plugins-1.0.0' / f'{name}.schema.json').read_text())
        Draft202012Validator.check_schema(schema)
        for error in Draft202012Validator(schema).iter_errors(documents[name]):
            path = '/'.join(map(str, error.absolute_path))
            errors.append(f'{name}.json/{path}: {error.message}')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--zip', type=Path, help='Also validate the manifests inside this archive')
    args = parser.parse_args()
    documents = {name: json.loads((ROOT / 'submission/octolane' / f'{name}.json').read_text())
                 for name in ('plugin', 'mcp')}
    errors = validate_documents(documents)
    if args.zip:
        with zipfile.ZipFile(args.zip) as archive:
            errors += validate_documents({name: json.loads(archive.read(f'{name}.json'))
                                          for name in ('plugin', 'mcp')})
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print('Agent Plugins base/transport projection + documented read/write OpenAI OAuth profile: PASS. The full MCP document does NOT pass the generic published schema (extensions mismatch); portal acceptance and runtime remain unverified.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
