> Historical audit snapshot. For current OAuth behavior, publication state and remaining gates, see [local readiness](local-readiness-checkpoint.md). Earlier no-refresh findings below describe the audited baseline, not the revised PR.

# OCT-4270 local review — 21 October 2026 Pacific

Latest local OAuth work and test results: [22 October checkpoint](local-readiness-checkpoint.md). The evidence below is the earlier package review.

**Not submission-ready.** Static package work is complete; live compatibility, reviewer access and owner decisions remain pending. No push, deployment, submission, new credentials or OAuth grants occurred.

## Verified locally

- Public sources and ZIP manifests pass the unmodified published Agent Plugins 1.0 schemas. The generic schema treats OpenAI extensions as opaque; this is not portal acceptance.
- Removed the per-server OAuth extension rejected by the published MCP schema. The public package now relies on protected-server OAuth discovery; live ChatGPT compatibility remains untested. See `schemas/README.md`.
- All 16 plugin tests pass. Two consecutive builds compare byte-for-byte equal. ZIP contains only `plugin.json`, `mcp.json`, `assets/icon.png`, `assets/logo.png`; inspected manifest bytes contain no keys, local paths or private fixture data.
- ZIP SHA-256: `802677a913bb8db0b243a5cba2471facf1fc2e0583848523ce35c2a92c0fbc52`.
- Existing Codex key-header configuration and marketplace path preserved and covered by static tests. No installed Codex runtime test was performed.
- GitHub CI configuration added, but CI has not run. Local checks are the evidence above.
- Backend patch `7cee805f3` in sibling `octolane-backend-review`, branch `rafi/oct-4270-chatgptcodex-plugin`, based on locally available origin/dev `fcf3e0bf`. It explicitly supplies false destructive hints for existing read-only groups, without changing handlers or removing tools. Not deployed.
- Real registrar regression enumerates 72 unique tools and explicit required booleans. It failed on the baseline for 25 missing destructive hints and passed after the patch. Targeted registrar, auth-provider and key-role suites: 15 tests passed with ts-jest diagnostics disabled for that invocation only. Normal runner failed before execution on shared-package resolution/AI telemetry type errors; no successful typecheck is claimed. Existing dependencies were reused read-only. No timeout changes.

## Public checks and corrections

`https://docs.octolane.com/support` redirects to `https://www.octolane.com/support` and returns 404. `https://docs.octolane.com/mcp/quickstart` redirects to `https://www.octolane.com/mcp/quickstart` and returns 404. These are observations for those exact URLs at the time checked. The parent independently received 404 for `https://docs.octolane.com/mcp/use-with-chatgpt` and 403/error 1010 for the different URL `https://octolane.com/docs/mcp/quickstart`; do not conflate those results. Earlier cached documentation is not reliable evidence of current availability. The parent verified HTTP 200 for `https://mcp.octolane.com/`, containing actual OAuth/key setup instructions and the `/mcp` endpoint. README and reviewer instructions now use that landing page; none of the failed guides is retained as a verified setup reference. Homepage changed to verified `https://www.octolane.com/`; the official alternative `https://octolane.com/docs/support/contact` was subsequently verified HTTP 200 and provides email, phone and in-app support instructions. Both manifests now use it. Support channel responsiveness itself was not tested.

Public OAuth metadata returns 200 and advertises authorization code, PKCE S256, dynamic registration, read/write scopes, refresh and revocation. Unauthenticated `/mcp` returns 401. Its challenge lacks a resource_metadata parameter; root protected-resource metadata exists. These reads do not prove authentication works. Source audit still requires resolution of code/client/resource/scope binding and token lifecycle; refresh is advertised although the inspected provider rejects refresh, and revocation is a no-op. Preserve existing clients when addressing these issues.

## Pending actions and approvals

| Action / target | Missing input or authorization | State |
| --- | --- | --- |
| Connect ChatGPT to designated synthetic Octolane workspace | Workspace/account names and explicit OAuth connection permission; no secrets in chat | Pending |
| Execute all 72 tools and eight review cases | Authorized fixtures, roles, two-tenant isolation setup and controlled create/update/delete/email scheduling permission | Pending |
| Prepare dedicated reviewer access | Existing approved sample-data account or separate approval for account/credential/access creation; secure portal handoff | Pending |
| Record demo using real successful flows | Working authorized connection and fixtures; accessible hosting choice | Pending |
| Complete publisher and listing metadata | Verified publisher, countries/languages, confirmation of the verified support destination, privacy owner approval (including current “Attio services” wording) | Pending |
| Backend OAuth lifecycle remediation and deployed validation | Resolve documented contract findings, validate in synthetic setup; deployment separately authorized | Pending |

No designated authorized live test workspace was found in the inspected MCP test/config sources; existing tests use local stubs. Do not infer live-test permission from development credentials. `runtime-evidence.md` provides 72 unexecuted rows; `reviewer-walkthrough.md` supplies the recording script. All release gates remain pending until supported by actual evidence.

A test initially attempted to write a log under the original checkout via reused dependency path resolution; the sandbox denied that file write (EPERM). Subsequent test invocation set APP_ROOT_PATH to the isolated writable checkout and passed. The denied original-path write was not retried. No approval-review rejection occurred.

## Test authoring rationale

The registrar regression protects the independent directory requirement for explicit boolean annotations and preserves the agreed 72-tool breadth. Removing a required hint or tool fails it. Existing description tests did not assert annotation presence. It extends the existing real-registration harness without introducing a production seam. It does not claim the annotations accurately describe every handler's effects; semantic and live review remain gates.
