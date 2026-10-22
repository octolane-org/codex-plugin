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
        return {name: json.loads((ROOT / 'submission/octolane-ai-crm' / f'{name}.json').read_text())
                for name in ('plugin', 'mcp')}

    def test_actual_public_sources(self):
        self.assertEqual(schema_check.validate_documents(self.documents()), [])

    def test_schema_rejects_documented_but_unsupported_oauth_extension(self):
        docs = self.documents()
        docs['mcp']['mcpServers']['octolane']['extensions'] = {'com.openai': {'auth': {'type': 'oauth'}}}
        self.assertTrue(schema_check.validate_documents(docs))

    def test_portable_schema_rejects_legacy_manifest(self):
        docs = self.documents()
        docs['plugin']['mcpServers'] = './.mcp.json'
        self.assertTrue(schema_check.validate_documents(docs))
