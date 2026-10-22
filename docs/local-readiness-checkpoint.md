# Local readiness checkpoint — 22 October 2026

**Ready for local code review, not submission.** The public ZIP remains a draft. No push, deployment, submission, live connection or real credential/access creation occurred.

## OAuth implementation

Isolated backend checkout `../octolane-backend-review`, branch `rafi/oct-4270-chatgptcodex-plugin`:

- `3bb3884f7`: opaque grant-backed tokens with persisted scopes, canonical MCP resource, fixed expiry and per-client revocation.
- `7a1f48cd0`: scope enforcement before tool handlers, consent propagation, accurate discovery and route regression coverage.
- Both author and committer verified as `md-abdul-halim-rafi <mdabdulhalimrafi@gmail.com>`. Standard commits, no hook bypass.

The smallest implemented lifecycle is **24-hour grants and reauthorization, no refresh tokens**. Discovery advertises only authorization-code grants; refresh requests return unsupported_grant_type. Grant records expire in Redis and expiry is also checked in code. The opaque token is SHA-256 hashed for its Redis lookup key. Its backing workspace API key remains server-side in the grant record for at most that TTL; no encryption-at-rest change is claimed. Privacy/security owners must include this retention in review.

Explicit foreign resources are rejected. An omitted resource defaults to the canonical `/mcp` resource for existing clients; only the exact origin resource previously advertised is accepted as an alias. Both old root and new path-specific protected-resource discovery URLs remain available. The 401 challenge points to the path-specific metadata.

Legacy direct workspace keys retain their existing permissions and current key/member validation. New OAuth grants are scoped and client-associated; revoking one grant never disables the shared key or another client's grant. Existing raw-key OAuth sessions cannot retrospectively gain per-client revocation; reconnect them to obtain the new grant model. Pre-upgrade in-flight codes lacking scope/resource require reauthorization. Deployment must verify these transition cases on approved synthetic clients.

Read-only grants can execute only tools marked readOnlyHint:true. Every other tool, including external cache synchronization and tools missing the annotation, requires crm:write. Write-only grants do not imply read access. Scope checks supplement existing role/tenant permissions. Consent lists the actual requested capability groups, including deletion, calendar/email and invitation effects. The registry remains 72 tools; no subset is packaged.

## Actual local proof

Six focused suites, **52 tests passed with normal type diagnostics enabled**:

- Provider: client/redirect/code binding, one-time code use, opaque tokens, scopes/resource, fixed expiry, missing-token rejection, client-specific revocation, legacy key preservation and current backing-key role/validity checks.
- Real Express/SDK routers with synthetic HTTP objects: consent through key entry and token exchange, PKCE failure/success, revocation, refresh rejection, discovery aliases and bearer challenge.
- Scope propagation from authenticated request into tool context, fail-closed missing grant scopes, and scope checks before handler invocation.
- Existing role and registrar suites, including all 72 unique tools and explicit annotations.

Redis and upstream services are mocked. No live Redis integration, actual browser/client connection or production behavior is claimed. The new tests protect independent authorization/transport contracts and introduce no production test seam. Existing socket-based MCP route suite attempted listen on 0.0.0.0 and was denied EPERM by the sandbox; it did not pass. The added scope-propagation test invokes the real router in-process with mocked transport. No timeout change or socket escalation was made.

ESLint on all changed TypeScript and git diff --check passed. Full app `tsc --noEmit` did not pass: 56 errors from unresolved shared build declarations and related project dependencies in this isolated checkout. The production tsconfig intentionally targets shared/dist; root/production tsconfigs were not altered. A normal shared-package build and whole-app typecheck remain an independent local validation gate, deferred to avoid a resource-heavy build while the stats investigation has priority.

The prior SDK 7 mismatch is resolved for these tests: cached AI SDK 6.0.311, gateway 3.0.218, provider 3.0.19 and provider-utils 4.0.61 were integrity-checked against npm cache SHA-512 and extracted into this checkout's packages/ai/node_modules. No network package download or writes to another task's dependencies. Initial npm cache write attempts were denied; read-only cache extraction into this checkout succeeded. No disposable acceptance environment was created. Other dependencies are still reused read-only, so this is not proof of a clean install.

## Submission gates and minimum next inputs

1. Complete shared-package build/type validation when resources permit, then review/deploy the backend through separately authorized normal release steps. Current code is local only.
2. Name the existing subscribed synthetic workspace, second tenant, test identities/roles, ChatGPT/Codex accounts and controlled mailbox. Obtain exact OAuth connection approval after identifying targets. Then approve bounded write/delete/outbound batches; no broad production tests.
3. Run authenticated discovery and all 72 tool contracts, isolation/role/subscription checks, legacy client transition and the eight reviewer scenarios. Record actual evidence; mocks do not satisfy these gates.
4. Confirm verified publisher, countries/languages, privacy owner approval (including grant retention and the earlier policy wording finding), and existing reviewer-access owner/account. No passwords or keys in chat/repository.
5. Record a real successful walkthrough and verify reviewer-accessible hosting. Supply the actual video URL. Reviewer credentials belong only in approved secure portal fields.
6. Revalidate listing URLs, build the release ZIP after evidence gates pass, and verify portal acceptance during an authorized preparation step. Public schema validation alone is not portal acceptance.

Support: https://octolane.com/docs/support/contact. Setup: https://mcp.octolane.com/. These were previously verified; no new external checks were performed in this local-only continuation. Existing plugin tests/schema/ZIP evidence remains in final-local-review.md. CI has not run and nothing has been pushed.
