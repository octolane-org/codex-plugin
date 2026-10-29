# Release procedure

## Current release: 0.2.0

Octolane 0.2.0 was published on 29 October 2026. The [release record](releases/0.2.0.md) is the source of truth for upload provenance, checksum, observed portal state and evidence limits. [CHANGELOG.md](../CHANGELOG.md) records package release chronology. Keep both manifests at 0.2.0 when merging this documentation reconciliation.

The public source declares OAuth through `extensions.com.openai.auth`, with `baseScopes: [crm:read, crm:write]` and `defaultScopes: []`. It contains no credentials, fixed headers or private App binding. The local Codex package separately uses `bearer_token_env_var: OCTOLANE_API_KEY`. Both use the production MCP URL, official 528px icons and the subtitle “Revenue Superintelligence”. No skills ship in 0.2.0.

## Offline verification and exact reproduction

```sh
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate_schemas.py
python3 scripts/package_plugin.py validate
python3 -m unittest discover -s tests -v
python3 scripts/package_plugin.py build --draft
python3 scripts/validate_schemas.py --zip dist/octolane-0.2.0-draft.zip
shasum -a 256 dist/octolane-0.2.0-draft.zip
```

Expected checksum: `5fd73ccc288d0f6284d2ed9cd309c354b54be4d57d28b0a6bdb02b11d8cb5339`. Build twice to check determinism. The archive contains only the two manifests and two icons. Its historical `-draft` filename is independent of publication status.

Validation uses the published base/transport schemas plus the documented OpenAI OAuth profile; see [schema limits](../schemas/README.md). Static success does not prove runtime behavior.

## Local checklist versus portal publication

`release-gates.json` is an engineering evidence ledger, not a portal status API. Keep unverified tests pending; do not mark all gates passed because the directory approved the package. `validate --release` and `build` without `--draft` deliberately require all local evidence and an embedded demo URL. The published upload supplied its demo/reviewer details separately through the portal, so those stricter commands still fail. This is not a claim that the published version remains a draft.

For future releases, reconcile the ledger with actual evidence, confirm current submission requirements, and record which fields are supplied in the package versus the portal. Keep credentials outside Git and archives. Preserve failed/not-run test results. Publisher attestations must be completed by the authorized owner.

## Future version changes

1. Describe the user-visible package change and select a version under the release policy; update portable and local manifests together. Documentation-only corrections do not change the published version.
2. Run the checks above with the matching version filename. Review archive contents, credentials exclusion, source parity and checksum.
3. Record the candidate and remaining runtime checks before any authorized upload. Backend releases have their own reviews and deployment evidence.
4. Treat upload, review submission and publication as separate authorized actions. Record approval and observed publication without inferring them from a successful build.
5. Add the published artifact checksum and chronology to the changelog/release record. Keep experimental desktop artifacts and migration work separate until validated and approved.
