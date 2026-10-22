# Release procedure

## Current implementation

The plugin-side v0.2.0 source, static checks, deterministic draft ZIP, and reviewer scenario metadata are implemented. The local Codex key-header package remains a separate distribution. No tools are removed or reimplemented. Current public source omits unknown support URL, demo URL, country targeting, commerce declarations and verified publisher assertions. Existing author identity is retained without implying verification.

Public MCP configuration now uses only schema-valid transport/endpoint fields and relies on OAuth discovery. Public metadata advertises DCR, authorization-code flow and PKCE S256. The prior per-server OAuth extension was removed because the actual published MCP schema rejects it; see `schemas/README.md`. This defines an intended discovery path only. No client registration, key creation, OAuth grant or account setup occurred.

## Release gates

`docs/release-gates.json` records release evidence outside the public package. Each gate needs `status: passed` plus a nonblank evidence reference after actual verification. Keep credentials and sensitive logs outside the repository. These records support human review; a script cannot authenticate their truth.

1. Confirm verified publisher, countries/languages and support ownership. Do not infer countries from the company address. Confirm the plugin only accesses existing subscriptions and does not sell subscriptions.
2. Verify all four listing URLs and actual content. The advertised `https://docs.octolane.com/support` redirected to `https://www.octolane.com/support`; direct HTTP returned 404 on 21 October 2026 Pacific. Supply an accessible support page, then set `supportURL` in both public and local manifests. Do not substitute a guessed URL or `mailto:`.
3. Have the owner validate privacy/terms coverage for all tools. The policy's “Attio services” wording requires correction or clarification by its owner. No legal text was changed here.
4. Complete backend follow-ups and validate OAuth, revoked keys, tenant/role/subscription enforcement and all 72 live tool contracts. Preserve evidence of actual calls, results and annotations. Keep migration workflows deferred.
5. Run the five positive/three negative review cases and broader per-tool coverage with synthetic fixtures. Record failed and not-run cases honestly.
6. Record and verify the walkthrough. Add the actual accessible URL to `extensions.com.openai.review.demo_recording_url`. A script is not a recording.
7. Verify dedicated reviewer access, permissions and service entitlements. Enter credentials only through secure portal review fields at the later authorized setup step.
8. Run unit tests and `validate --release`, then `build`. Inspect the ZIP and checksum. The builder excludes local manifests, headers, internal reports and release evidence.
9. During an authorized portal preparation phase, verify imported metadata, domain/developer identity, OAuth setup and scans; complete required attestations with the authorized publisher. Submission for review and publication are separate actions. No upload is automated here.

The repository checks are specific to this plugin and the current source layout. Separate validation against unmodified published Agent Plugins 1.0 schemas checks the public sources and ZIP manifests. OpenAI extension semantics are opaque in the generic schema; neither layer proves hosted behavior or directory approval. Recheck current official requirements before submission.

## Assets and listing

Existing logo and composer icon are identical square 523 × 523 PNGs, 8,346 bytes, with white marks on a dark background. Visual inspection confirmed a simple high-contrast symbol without small text. No new brand design or dark-mode variant was introduced; existing brand color is preserved. The build checks PNG structure/checksums, dimensions, and matching asset bytes across packages.

Public and local listing metadata are synchronized. The subtitle is “Manage your CRM in chat”; category is “Business & Operations”. Existing starter prompts and their order are preserved. Reviewer case metadata is packaged, but test status and evidence remain external.

## Validation and artifacts

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate_schemas.py
python3 scripts/package_plugin.py validate
python3 -m unittest discover -s tests -v
python3 scripts/package_plugin.py build --draft
python3 scripts/validate_schemas.py --zip dist/octolane-ai-crm-0.2.0-draft.zip
```

Expected current result: static checks and tests pass; draft artifact is produced with outstanding readiness gaps printed. `build` without `--draft` must fail until real release evidence and missing fields are complete. No release-date guarantee follows from passing these checks; any November target depends on readiness and review approval.
