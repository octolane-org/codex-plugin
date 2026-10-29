> Historical audit snapshot. For current OAuth behavior, publication state and remaining gates, see [local readiness](local-readiness-checkpoint.md). Earlier no-refresh findings below describe the audited baseline, not the revised PR.

# OAuth correctness checkpoint — 22 October 2026

**Historical findings below have now been addressed locally by backend commits `3bb3884f7` and `7a1f48cd0`. See [current checkpoint](local-readiness-checkpoint.md) for implementation, evidence and remaining gates. Nothing is deployed.**

Source findings refer to the isolated backend checkout, not a proven deployed exploit. Severity is engineering triage, not a CVSS assessment. The live service has not received these commits.

## Confirmed defects repaired locally

- **High: code binding.** `apps/mcp/src/auth/provider.ts` ignored the client in challenge lookup and code exchange and ignored the redirect URI supplied by the SDK. Added exact stored client/redirect checks. A valid code plus its PKCE verifier were still prerequisites; no claim of an unauthenticated bypass.
- **High: concurrent code replay.** Two exchanges could both read a code, delete it and return the key. Exchange now requires Redis DEL to return 1 before issuing a token. The other request receives invalid_grant. This uses the atomic single-key DEL contract without requiring a new Redis feature.
- **Medium: expired/rejected code error mapping.** Generic errors became server errors through the SDK. Invalid/expired/mismatched/replayed codes now use SDK InvalidGrantError.

Backend commit `a118081fd`. Six regression cases failed before the fix and passed after it. Tests use synthetic Redis return values, not a live Redis integration. They protect public provider behavior and introduce no test-only production API. Existing tests covered bearer validation but not code redemption.

## Remaining confirmed design defects — local engineering work, not reviewer-metadata blockers

| Finding | Source and consequence | Severity / next work |
| --- | --- | --- |
| No per-client grant token | Code exchange returns the workspace API key; verifyAccessToken reports clientId `mcp`. The token is not bound to the OAuth client. | High release blocker. Implement opaque grant-backed tokens while preserving legacy key authentication and existing Claude clients; test entirely with synthetic storage before live validation. |
| Lost scopes and resource | Pending records retain requested scopes, but auth-code records omit them; resource is not persisted. Verification always reports both CRM scopes and no audience. | High release blocker for OAuth least privilege/audience. Persist approved grant scope/resource, validate resource at authorization/exchange, and enforce at tool execution—not merely report narrower scopes. |
| Revocation does nothing | provider.revokeToken is empty while SDK advertises /revoke. | High lifecycle blocker. Revoke only the OAuth grant, never the shared workspace key; needs grant tokens above. |
| Expiry not enforced as advertised | exchange says one year; verification returns now plus one year on every request. | Medium lifecycle defect. Persist issuance/expiry in grant storage. Existing key disable/membership checks remain effective. |
| Refresh metadata contradicts provider | SDK createOAuthMetadata unconditionally advertises refresh_token; provider throws a generic error and never issues refresh tokens. | Medium interoperability defect. Choose explicit reauthorization with accurate discovery, or implement rotation/replay protection. Do not claim refresh support based on discovery alone. |
| Discovery challenge incomplete | Public 401 lacked resource_metadata; loader uses requireBearerAuth without resourceMetadataUrl. Root metadata exists. | Medium compatibility risk. Wire matching resource metadata and validate discovery through the real SDK route. Missing parameter alone does not prove every client fails. |

SDK inspection confirms tokenHandler validates S256 PKCE using challengeForAuthorizationCode before exchange. PKCE was not missing. Client authentication and initial redirect registration checks also exist. Those checks did not substitute for the repaired code/client binding.

## Type error diagnosis and proof

1. MCP tsconfig resolved shared subpaths to packages/shared/dist, absent in the isolated clone, while Jest already loaded shared source at runtime. This produced TS2307 for shared/utils or shared/constants. Backend commit `d489fd367` aligns the MCP test compiler paths to shared source. Root tsconfig and production build paths unchanged.
2. Reused read-only node_modules contains `ai` **7.0.107**, but packages/ai/package.json declares **^6.0.106**. SDK 7 rejects `experimental_telemetry.metadata` in packages/ai/src/llm/pipelineDraft.ts:39 (TS2353). Do not “fix” the SDK 6 application against this wrong-major install. A separate compatible dependency installation/build is still needed; no package install or mutation of the original checkout's dependencies occurred.

Actual checks:
- Normal configured auth-provider suite, diagnostics enabled: **12 passed** after source-path correction.
- Registrar + key-role + provider suites, diagnostics disabled for that earlier invocation: **21 passed**. Not a full typecheck.
- Normal registrar suite after source-path correction: fails before execution on the SDK 7 telemetry mismatch above, confirming that the shared-path error was removed.
- ESLint of changed provider and provider tests: passed. Prettier and git diff --check: passed.
- Commits use Rafi author and committer; no hook bypass flags used. No global timeout changes.

## Missing live verification and approvals

Actual ChatGPT OAuth callback/connection, all 72 live schemas and tool contracts, tenant/role/subscription enforcement, reviewer cases and recording are still unverified. Need designated non-production targets followed by exact connection and bounded test approvals. No credentials, grants, role changes, outbound messages, production mutations, pushes or deployments occurred.

Next independent engineering work is the grant-backed OAuth lifecycle and compatible local dependencies. This is distinct from waiting for publisher/reviewer metadata. Before deploying a replacement token model, validate legacy Claude/key clients and a synthetic ChatGPT connection; deployment remains separately authorized. Reviewer setup cannot substitute for fixing these confirmed lifecycle defects.
