# Backend PR scope — separate from this plugin change

No backend implementation is included in OCT-4270's plugin repository changes.

## Annotation compatibility

In `apps/mcp/src/mcp/constants/tools.ts`, 25 registered READ tools omit `destructiveHint`. Add explicit booleans after checking actual behavior against OpenAI requirements. Audit additive writes, external effects and `search_emails` cache synchronization as well. Do not mechanically declare every search read-only or every create destructive.

Acceptance: authenticated `tools/list` has all 72 agreed tool names with accurate `readOnlyHint`, `destructiveHint` and `openWorldHint`; schemas and descriptions match implementation. Preserve the Claude integration.

## OAuth compatibility while preserving workspace key paste

Inspect `apps/mcp/src/auth/provider.ts`, OAuth routes/types and SDK routing. Source returns the workspace API key as the OAuth token and reports constant client identity and both scopes. Trace SDK and backend enforcement of resource/audience, authorization-code client binding, PKCE, redirect URI, scopes, expiry, replay and disconnect/revocation. This is a compatibility/security audit finding, not a demonstrated exploit.

Public discovery advertises refresh-token grants, while inspected source rejects refresh calls; revocation is a no-op. Reconcile deployed behavior and metadata. Avoid revoking a shared key as a side effect of disconnecting one client. Design changes only after confirming the lifecycle contract; never weaken tenant isolation or request keys in chat.

Acceptance: synthetic end-to-end ChatGPT/Codex connection succeeds using the existing hosted key-paste experience; invalid/revoked credentials and foreign tenant IDs fail; role changes take effect; reconnect/expiry behavior is accurate. Public discovery alone does not satisfy this gate.

## Subscription and tool contracts

Verify all subscribed customers can connect without a new plugin tier, while preserving existing role permissions and service entitlements. Test writes, external sends, duplicate retries, partial batch failure, permission denial and unknown outcomes. Source registration count is 72; production discovery and behavior remain to be reconciled.

Keep tests in a synthetic environment. Creating accounts, grants or credentials, deploying backend changes and running production mutations require their own authorized work. Full CRM migration remains iteration two.
