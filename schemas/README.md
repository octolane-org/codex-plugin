# Published schema snapshots

Unmodified schema responses downloaded on 21 October 2026 Pacific:

- https://agent-plugins.org/schemas/1.0.0/plugin.schema.json
- https://agent-plugins.org/schemas/1.0.0/mcp.schema.json

Run `python3 scripts/validate_schemas.py` with `requirements-dev.txt` installed. Pass `--zip dist/octolane-ai-crm-0.2.0-draft.zip` to validate the actual archive manifests as well.

These schemas constrain portable metadata and transport. `plugin.json` extension objects are opaque to the generic schema, so passing does not validate every OpenAI listing/review requirement. Repository checks cover selected OpenAI constraints; portal validation remains a release gate.

The downloaded MCP schema has `additionalProperties: false` on HTTP servers and does not allow per-server `extensions`. OpenAI's package guide documents OAuth extensions that this portable schema rejects. The public package therefore uses only the verified transport/endpoint and relies on OAuth discovery. It does not declare no-auth or embed a fixed key. At the later authorized portal setup, verify OAuth selection and DCR/scopes; resolve any portal requirement conflicting with this schema before submission. Do not claim this mismatch was tested in the portal.

Update snapshots only after inspecting the upstream changes, then rerun schema and semantic tests. Do not silently patch the published schema to accept extra fields.
