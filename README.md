# Octolane AI CRM plugin

Plugin packaging for Octolane's hosted MCP server. Version 0.2.0 prepares a ChatGPT/Codex public-directory package while preserving the existing local Codex marketplace installation.

The release target is all 72 existing MCP tools for subscribed Octolane customers, subject to workspace permissions and connected-service access. This repository does not implement, proxy, or filter the tools. The MCP server owns discovery and execution. Migration workflows are deferred to iteration two.

**Status: draft, not submitted or approved.** Static packaging works; OAuth runtime tests, live tool verification, backend annotation fixes, and review materials remain release gates. See [readiness](docs/release-readiness.md) and [release procedure](docs/release-procedure.md).

## Public package (OAuth)

Source: `submission/octolane-ai-crm/`.

- Portable Agent Plugins 1.0 `plugin.json` with listing metadata and five positive/three negative review scenarios.
- `mcp.json` connects to `https://mcp.octolane.com/mcp` using streamable HTTP and OAuth DCR with `crm:read` and `crm:write`.
- Discovery supplies authorization, token and registration endpoints. No client ID, secret, fixed headers or tool allowlist is packaged.
- Users enter the desired workspace's MCP API key on Octolane's hosted authorization page. Never paste keys into chat. End-to-end compatibility is pending; a manifest declaration does not register a client or grant access.

Run locally with Python 3.10+ (standard library only):

```bash
python3 scripts/package_plugin.py validate
python3 -m unittest discover -s tests -v
python3 scripts/package_plugin.py build --draft
```

The draft ZIP and SHA-256 file are written to ignored `dist/`. The ZIP contains one plugin at its root. The build reopens and verifies the archive; timestamps and file order are deterministic. These are repository-specific checks, not an official OpenAI schema validator or approval.

A release build requires verified evidence in `docs/release-gates.json` and complete listing/review fields:

```bash
python3 scripts/package_plugin.py validate --release
python3 scripts/package_plugin.py build
```

These commands intentionally fail while readiness gaps remain. Do not mark gates passed merely to produce a release archive. Builds never upload, register, submit or publish anything.

## Existing local Codex installation (API key)

Add the repository marketplace:

```bash
codex plugin marketplace add octolane-org/codex-plugin
```

Then install **Octolane AI CRM** from Codex Plugins. For local development:

```bash
codex plugin marketplace add /absolute/path/to/codex-plugin
```

The marketplace still points to `plugins/octolane-ai-crm/`. That compatibility package uses `OCTOLANE_API_KEY` in its `X-API-Key` header. Configure the variable privately in the Codex environment using the key from the desired Octolane workspace; do not commit or share its value. The existing local install route was preserved but not reinstalled during this change.

Do not upload this local package to the public directory. Use the dedicated OAuth source and build command above. Identity, version, listing fields and assets are checked for consistency across the two packages; authentication intentionally differs.

## Files

- `.agents/plugins/marketplace.json`: local Codex marketplace.
- `plugins/octolane-ai-crm/`: existing local API-key compatibility package.
- `submission/octolane-ai-crm/`: OAuth public-package source.
- `scripts/package_plugin.py`: offline validation and deterministic archive build.
- `tests/test_package.py`: archive isolation, metadata, assets and release-gate regression checks.
- `docs/tool-inventory.{json,md}`: 72-tool static baseline, not a live discovery result.
- `docs/reviewer-walkthrough.md`: synthetic fixtures, recording plan and evidence requirements.
- `docs/backend-followups.md`: separately scoped backend work.

Customer setup: [Octolane MCP quickstart](https://docs.octolane.com/mcp/quickstart). Public package requirements: [OpenAI submission guide](https://developers.openai.com/plugins/deploy/submission).
