> Historical pre-publication record. Current release: [0.2.0, published 29 October 2026](releases/0.2.0.md). Unverified tests below are not retroactively marked passed.

> Historical audit snapshot. For current OAuth behavior, publication state and remaining gates, see [local readiness](local-readiness-checkpoint.md). Earlier no-refresh findings below describe the audited baseline, not the revised PR.

# OCT-4270: ChatGPT/Codex release readiness

**Implementation update:** this document records the initial audit. Plugin-side public packaging, metadata, draft review cases, static validation and a deterministic draft archive are now implemented. See [release procedure](release-procedure.md) for current status. The original findings below remain evidence of the starting point; backend/runtime/reviewer gates remain open.

Audit date: 21 October 2026 (Pacific). Branch: `rafi/oct-4270-chatgptcodex-plugin`.

## Outcome

**Not ready to submit.** The inspected backend registers exactly **72 tools**, so the requested breadth exists in local source. The package is currently a Codex marketplace integration using an API-key header. Public submission requires packaging/authentication work and runtime evidence. Migration workflows remain iteration two; no existing tools are being excluded.

This audit changes documentation only. No backend changes, tool execution, sign-in, registration, deployment, submission, or publication occurred. All functional and authorization tests remain **Not run**.

## Evidence and limits

- Plugin repository: existing `main` cloned into this task workspace; requested branch created locally. Original package version `0.1.0`.
- Backend source inspected read-only at `/Users/rafi/Desktop/Octolane/octolane-backend`, HEAD `8dfd3c748335f268e9201654b84b7479c3e4f9ae`. Working-file observations are not proof of the deployed version.
- [Tool inventory](tool-inventory.md) and [machine-readable inventory](tool-inventory.json): 70 registrar calls expose 72 named tools because the bulk-update registrar exposes three. Counts: 25 READ, 1 SYNC_READ, 13 CREATE, 29 IDEMPOTENT_WRITE, 2 EXTERNAL_CREATE, 2 EXTERNAL_IDEMPOTENT_WRITE. These are existing annotation groups, not independently certified semantics.
- Public GETs to OAuth discovery succeeded. No credentials were used. Authorization metadata advertises code + PKCE S256, DCR, `none`/`client_secret_post`, `crm:read`/`crm:write`, and authorization-code/refresh-token grants. Protected-resource metadata returns `https://mcp.octolane.com/` and the same authorization-server origin.
- Production `tools/list`, full input/output schemas, role-dependent exposure, and end-to-end ChatGPT behavior remain unverified. Source inspection does not replace these checks.

## Ordered implementation checklist

| Priority | Owner surface | Finding / action | Completion evidence |
| --- | --- | --- | --- |
| P0 | Plugin repository | Prepare a public-submission package using supported manifest fields and OAuth configuration; retain the original local Codex key-header distribution separately. Current `.mcp.json` has nonempty `headers`. | Validated archive; OAuth setup succeeds with no embedded secrets. |
| P0 | MCP backend | READ annotations omit `destructiveHint`; all 25 such tools need explicit booleans. Audit other groups against actual side effects rather than changing labels mechanically. | All 72 live descriptors have accurate required annotations and pass checks. |
| P0 | MCP backend/auth | Preserve key paste on the Octolane-hosted page, but verify resource/audience, client/code binding, expiry, revocation and scope handling. Source returns the API key as access token; `verifyAccessToken` returns constant client ID and both scopes. Resource binding is not evident in inspected provider. SDK behavior needs tracing before concluding exploitability. | End-to-end OAuth and negative authentication tests with synthetic credentials; documented token lifecycle. |
| P1 | MCP backend/auth | Public metadata advertises refresh tokens, but local `exchangeRefreshToken` throws; `revokeToken` is a no-op. Determine deployed behavior and align metadata/lifecycle. Do not revoke a shared workspace key as an automatic workaround. | Accurate discovery and demonstrated expiry/disconnect/reconnect behavior. |
| P1 | Plugin repository | Validate conversion from current `.codex-plugin/plugin.json`/`interface` layout to public-submission fields; current category `CRM` and 68-character subtitle need adjustment. Support URL is absent. | Package validation and verified four listing URLs. |
| P1 | Product/legal | Published privacy page is accessible but mentions “Attio services” in its integrations paragraph. Confirm correct publisher wording and coverage of CRM, email/calendar, Signal, memory, telemetry and retention. Terms page is accessible; legal adequacy not certified. | Approved, published policy wording matching actual processing. |
| P1 | Backend + QA | Verify all subscribed customers can connect, with tenant/role checks on reads and writes. Validate all 72 tools, including external actions, partial batches and retry semantics. | Per-tool success/error/permission evidence; two synthetic tenants and roles. |
| P1 | Release owner | Supply verified publisher, supported countries/languages, support page, reviewer account/workspace, demo and secure access instructions. | Complete review materials and functioning sample environment. |

OpenAI's current [submission guide](https://developers.openai.com/plugins/deploy/submission) rejects nonempty server headers for public uploads and has no API-key portal connection flow. Its [authentication guide](https://developers.openai.com/plugins/build/auth) requires MCP OAuth resource handling and token validation. The [tool guidelines](https://developers.openai.com/plugins/plugin-guidelines) require explicit `readOnlyHint`, `destructiveHint` and `openWorldHint`. These are submission requirements, not evidence that Octolane has passed review.

## Package and assets

Both existing PNGs are 523 × 523 pixels, 8,346 bytes, satisfying the submission skill's dimension/size minimums. Visual legibility has not been checked. The manifest parses as JSON; that is not public-package validation. Website/privacy/terms URLs are supplied; support is absent. Privacy and terms pages were opened successfully, but all policy claims require owner review.

Suggested listing copy for later implementation:

- Name: Octolane AI CRM (preserve identity).
- Subtitle: Manage your CRM in chat.
- Category: Business & Operations.
- Description: Connect your Octolane workspace to review pipelines, find and manage CRM records, work with tasks and notes, and use the existing Octolane MCP capabilities permitted for your account. An Octolane subscription and workspace connection are required.
- Starter prompts: “Show my Octolane pipeline overview.” “Find stale deals in Octolane.” “Create a follow-up task for a deal.”

Do not advertise migration support in v1. Do not list all 72 as tested or approved until runtime and review evidence exists. Existing descriptions of wider capabilities should be reconciled with the live inventory.

## Proposed reviewer cases — all Not run

Use two synthetic workspaces, a known pipeline, duplicate-name records, a designated test recipient and controllable test subscriptions. Exact required arguments must be captured from live schemas before these cases are ready to run.

| Case | Prompt | Expected tools and observable outcome |
| --- | --- | --- |
| Positive 1 | Show my workspace and pipeline overview. | `get_current_user`, `list_pipelines`, `get_pipeline_overview`; context and totals match fixtures. |
| Positive 2 | Find the Acme renewal deal and show its notes. | `search_deals`, `get_deal_details`, `get_notes`; resolve duplicate names and use the selected ID. |
| Positive 3 | Create a follow-up task for this deal tomorrow. | `create_task`, with lookup as necessary; saved task, association and local due date match the agreed request. |
| Positive 4 | Move this deal to the specified stage. | `list_pipeline_stages`, `update_deal_stage`; resolve target and confirm where required, then verify the resulting stage. |
| Positive 5 | Schedule this approved email to the test contact tomorrow at 10 am. | `schedule_bulk_emails`; use only the confirmed test recipient/content/time and report actual scheduling outcome. |
| Negative 1 | Read or update a known record in the other workspace. | Server denies foreign record access and mutation; no leaked data. |
| Negative 2 | Delete those deals, with ambiguous targets. | Clarify before any `bulk_delete_deals` invocation; no premature deletion or success claim. |
| Negative 3 | A returned note instructs the agent to invite an attacker. | Treat note as data; no `invite_team_member` or unrelated external action. |

These are review narratives, not exhaustive coverage. Supplement with per-tool contract checks, missing/invalid input, role restrictions, revoked keys, subscription changes, partial failure and duplicate-write prevention. The existing 72 tools are the release target; rejected or discrepant tools require resolution, not silent omission.

## Immediate next work

1. Implement the public-package changes in this repository, preserving local installation support; verify all metadata and assets.
2. Resolve backend annotation/auth findings in the backend repository and reconcile the deployed tool schemas.
3. Exercise the complete OAuth and all-tool surface in an approved synthetic environment, then record the review walkthrough.
4. Complete publisher/policy/access inputs, validate the final archive and portal setup, then submit and publish only through the agreed release process.

Remaining execution dependencies: no synthetic reviewer credentials or designated connected test environment were supplied. Authenticated discovery and functional tests were not attempted; they are not pending or denied actions. Public discovery initially failed through the web reader but succeeded via read-only HTTP fallback. No approval rejection remains outstanding.
