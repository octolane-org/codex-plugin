import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('validate_schemas', ROOT / 'scripts/validate_schemas.py')
schema_check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(schema_check)


class PublishedSchemaTests(unittest.TestCase):
    def documents(self):
        return {name: json.loads((ROOT / 'submission/octolane' / f'{name}.json').read_text())
                for name in ('plugin', 'mcp')}

    def test_actual_public_sources(self):
        self.assertEqual(schema_check.validate_documents(self.documents()), [])

    def test_oauth_profile_rejects_missing_auth_and_credentials(self):
        for extension in (None, {}, {'com.openai': {'auth': {'type': 'oauth'}}},
                          {'com.openai': {'auth': {'type': 'oauth', 'baseScopes': ['crm:read'], 'defaultScopes': []}}}, {'com.openai': {'auth': {'type': 'none'}}},
                          {'com.openai': {'auth': {'type': 'oauth', 'clientSecret': 'synthetic'}}}):
            with self.subTest(extension=extension):
                docs = self.documents()
                server = docs['mcp']['mcpServers']['octolane']
                if extension is None:
                    server.pop('extensions', None)
                else:
                    server['extensions'] = extension
                self.assertTrue(schema_check.validate_documents(docs))

    def test_portable_schema_rejects_legacy_manifest(self):
        docs = self.documents()
        docs['plugin']['mcpServers'] = './.mcp.json'
        self.assertTrue(schema_check.validate_documents(docs))
