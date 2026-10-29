# Published schema snapshots

Unmodified schema responses downloaded on 21 October 2026 Pacific:

- https://agent-plugins.org/schemas/1.0.0/plugin.schema.json
- https://agent-plugins.org/schemas/1.0.0/mcp.schema.json

Run `python3 scripts/validate_schemas.py` with `requirements-dev.txt` installed. Pass `--zip dist/octolane-0.2.0-draft.zip` to validate the actual archive manifests as well.

These schemas constrain portable metadata and transport. `plugin.json` extension objects are opaque to the generic schema, so passing does not validate every OpenAI listing/review requirement. Repository checks cover selected OpenAI constraints; portal validation remains a release gate.

The generic MCP schema still rejects per-server `extensions` when rechecked on 27 October 2026. OpenAI explicitly documents `extensions["com.openai"].auth.type: "oauth"` for submission, and the portal handoff reported that the previous URL-only package selected NoAuth. The public package declares OAuth with the read/write scope profile below; endpoint/client overrides and secrets are absent.

The vendor snapshots above remain unchanged. `validate_schemas.py` checks the exact read/write OAuth profile separately, removes only that validated extension from an in-memory copy, then checks the base/transport projection against the published schemas. This is an Octolane validation profile, NOT a claim that the full MCP document passes the generic published schema or that the portal accepted it. Missing auth, other auth modes, unknown fields and embedded credentials fail. Repository package checks independently enforce the same release packaging contract.

Official references:
- https://developers.openai.com/plugins/build/plugins#configure-mcp-authentication
- https://developers.openai.com/plugins/deploy/submission#configure-authentication-for-submission

Portal handoff: update the existing authorized draft, verify it retains the intended App identity and selects OAuth, and let discovery supply optional endpoint/client settings. Do not infer connection success, register a client or authorize a grant from this offline package change. Local API-key configuration is unchanged.

Update snapshots only after inspecting the upstream changes, then rerun schema and semantic tests. Do not silently patch the published schema to accept extra fields.

## Current read/write candidate profile

The candidate requires `auth: {"type":"oauth","baseScopes":["crm:read","crm:write"],"defaultScopes":[]}`. Validators reject narrower/missing scope declarations for this candidate. This supersedes the earlier read-only test profile and minimal auth-only profile above; no client or endpoint override is added. Actual requested scopes, consent and server enforcement require runtime verification after an authorized rollout. No portal settings or installed connections changed.
