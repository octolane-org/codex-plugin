# Current release checkpoint — 23 October 2026

**Review draft, not submission-ready.** Backend changes are in [PR #4649](https://github.com/octolane-org/octolane-backend/pull/4649). The separate plugin package is published in [PR #1](https://github.com/octolane-org/codex-plugin/pull/1) against main; its initial package CI passed. Neither repository is deployed or submitted by this task. Historical audit documents are retained as evidence and are superseded by this checkpoint.

## Revised OAuth behavior

The backend now implements one-hour opaque access tokens and client-bound rotating refresh credentials for new connections. The proposed inactivity policy is **90 days since the last successful refresh**, renewed on rotation, with no daily manual reconnect or fixed maximum connection age. Privacy/security owners must approve this retention before release.

Refresh preserves resource/client binding, allows scope narrowing but never expansion, revalidates the backing key/member, and revokes the entire family on authentic old-token replay outside a 30-second retry window. Simultaneous refreshes and lost-response retries within that window receive the same successor; even immediate use of that successor remains stable for the window. A stale retry after the window can require authorization again. A narrower refresh does not retroactively change already issued access tokens, which expire within one hour.

Transient Redis or primary failures return server_error rather than invalid_grant. This preserves server-side retryability but does **not** guarantee that a host avoids reconnect UI: the actual SDK auth() client returns REDIRECT after one HTTP 500 server_error refresh response without invalidating tokens; HTTP 200 returns AUTHORIZED and saves the successor without redirect. A later explicit retry can recover with retained tokens, but the first redirect already occurred. Ordinary successful expiry renewal and transient-outage UX are separate contracts. Verify each actual host's redirect, token retention, backoff and recovery behavior before claiming interruption-free renewal. The workspace key is never returned as a refresh credential. Family records contain sensitive backing keys, per-family HMAC secrets and the last response for up to the renewable 90-day inactivity period. No encryption-at-rest change or production storage guarantee is claimed.

Existing raw-key connections retain current key/member validation and do not receive the new fixed OAuth TTL. Synthetic SDK bearer coverage accepts the same key after 370 days and rejects it after primary reports inactivity. Existing opaque no-family tokens retain their original stored expiry. Existing clients cannot be retroactively given refresh credentials or have their cached expiry overridden; no forced migration is proposed. Pre-upgrade in-flight codes lacking scope/resource may need authorization restarted.

A validator-first rollout is required: the new `MCP_OAUTH_REFRESH_ENABLED` switch defaults false and pauses **new** code-to-token issuance without consuming codes. Existing access/refresh validation remains active. After every replica supports the model and storage/host tests pass, enable issuance consistently. Do not roll back to old validators after new credentials are issued. This deliberate temporary pause affects new connections; it does not invalidate established sessions. No environment switch has been changed.

Detailed operational contract: `apps/mcp/docs/oauth-refresh-rollout.md` in backend PR #4649.

## Evidence and limits

- Backend: 70 focused tests (including two real SDK client-path cases) cover actual SDK handlers with synthetic primary/storage, consent/PKCE, optional scope/redirect compatibility, renewal through time advancement, narrowing, replay, concurrent rotation, revocation races, outages/recovery, old raw/opaque credentials, scope enforcement, roles and 72-tool registry integrity. The renewal regression fails against the pre-refresh provider with HTTP 400.
- Backend full MCP TypeScript and changed-file lint have passed locally. Shared/AI/memory builds passed in the preceding checkpoint; no package code changed for refresh. Normal pre-push compilation is required before publication.
- Tests mock the atomic Redis primitive. Its Lua script has not been executed against live Redis. Externally managed Redis is configured in the repository, but persistence, no-eviction, acknowledged-write durability and failover have **not** been verified. Stale restores can resurrect revocations; this is a release blocker until resolved.
- The preexisting socket test was denied by the sandbox (listen 0.0.0.0, EPERM), was not retried, and is not a passing test. In-process SDK/route coverage does not replace a live host connection.
- Plugin static validation, published Agent Plugins schemas, 16 regression tests, deterministic four-file draft ZIP and release-gate refusal are checked locally. Schema success does not establish OpenAI extension/portal acceptance.
- No real credentials, OAuth clients/grants, outbound tool actions or production mutations were created. CI results and review state must be reported from the actual PR checks, separately from local proof.

## Remaining gates

1. Independent security/code review of refresh, atomic storage behavior and rollout; verified durable Redis with no eviction and failover/recovery evidence. Review the proposed 90-day retention and 30-second retry tradeoff.
2. Name existing subscribed non-production workspaces (including a second tenant), roles, ChatGPT/Codex/Claude test accounts and controlled recipient/sender resources. Obtain precise OAuth and bounded tool-action approvals before live tests.
3. Verify automatic refresh, legacy client continuity, actual 72-tool discovery, role/tenant/subscription isolation and eight reviewer scenarios on approved hosts. No migration workflows in v1.
4. Publisher identity verification, countries/languages, privacy owner approval (including earlier policy wording and new credential retention), reviewer-access owner and secure portal credential handling.
5. Record a real successful demo and provide a reviewer-accessible video URL; validate all public links again before submission.
6. Release the backend through separately authorized normal deployment, enable issuance only after rollout gates, then populate real evidence in release-gates.json and build the release ZIP. Submission still requires explicit authorization.

The original Codex marketplace and API-key package are preserved. Their X-API-Key transport has not been live reverified. The public package discovers OAuth and contains no fixed headers, credentials or tool allowlist; all 72 tools remain served by the backend.

Setup: https://mcp.octolane.com/. Support: https://octolane.com/docs/support/contact. Earlier broken guide URLs remain only in historical audit evidence. Neither workflow configuration nor local test output is a claim that GitHub CI ran.
