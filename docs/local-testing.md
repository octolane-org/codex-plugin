# Test Octolane locally before publication

Use your existing Mac mini checkout and normal Codex/ChatGPT accounts. Do not
create a disposable account, alternate CODEX_HOME or throwaway CRM workspace.
These instructions are a proposed manual runbook; only the checks listed under
“Evidence” have actually run. Installation and connection commands below have
not been executed by the agent.

## 1. Build and inspect the package without credentials

From this repository on `rafi/oct-4270-chatgptcodex-plugin`:

```sh
git branch --show-current
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate_schemas.py
.venv/bin/python scripts/package_plugin.py validate
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/package_plugin.py build --draft
.venv/bin/python scripts/validate_schemas.py --zip dist/octolane-0.2.0-draft.zip
unzip -l dist/octolane-0.2.0-draft.zip
```

Reuse `.venv` on subsequent runs. Expected archive: plugin.json, mcp.json,
assets/icon.png and assets/logo.png only. Both icons are the official 528px PNG.
`validate --release` must still fail until live/reviewer evidence is recorded;
do not mark a gate passed to get a release ZIP. Static schemas do not prove host
acceptance. No server start is needed for this section.

## 2. Load the local Codex package (API-key path)

The installed Mac app bundles CLI 0.163.0-alpha.11.2. Its help confirms these
commands; `codex` was not on this task's PATH. Use the bundled executable:

```sh
CODEX_BIN=/Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex
"$CODEX_BIN" --version
"$CODEX_BIN" plugin marketplace list
"$CODEX_BIN" plugin list
"$CODEX_BIN" plugin marketplace add "$PWD"
"$CODEX_BIN" plugin add octolane@octolane
```

Review the existing marketplace/installation first. If `octolane` or this plugin
is already installed, do not replace or uninstall an established connection to
test an update. Confirm its source and the intended upgrade with Rafi first.
The add/install commands change the normal local configuration and may prompt
authentication; Rafi must approve that step. Stop before any unexpected OAuth
prompt. Marketplace policy is ON_INSTALL.

Open **Plugins** in the ChatGPT desktop app, find the local Octolane marketplace,
and inspect the list tile and plugin details. The source is
`plugins/octolane/.codex-plugin/plugin.json`. Start a new Codex session
and inspect the @ picker/composer icon. Capture light/dark screenshots of list,
details and composer, without keys, emails or customer records. Compare to
`docs/screenshots/asset-sizes-light-dark.png`. There is no custom MCP App UI in
this package to test. The IDE extension does not support plugins.

For a local-folder source refresh, restart the desktop app, reopen the plugin details and start a new session. Verify the installed identity and copy; do not assume source edits hot-reload. The current CLI's `plugin marketplace upgrade` refreshes Git marketplace snapshots, so it is not a verified refresh mechanism for this local folder. Use the host's supported update/reinstall flow after confirming the intended installation. See [identity migration](identity-migration.md) for the renamed package.

**Corrected transport contract:** the local `.mcp.json` now declares
`bearer_token_env_var: "OCTOLANE_API_KEY"`. Codex resolves this native environment
binding into `Authorization: Bearer <key>`, matching the backend SDK middleware.
The old X-API-Key mapping is removed. Do not replace it with an inline key or
assume header-string `${...}` interpolation is supported. The public OAuth
package remains header-free.

The official compatibility plugin parser deserializes native McpServerConfig,
whose HTTP transport supports bearer_token_env_var. The bundled CLI help also
confirms bearer environment binding. A synthetic SDK middleware check accepts
the resolved Bearer shape and rejects X-API-Key-only traffic. This proves the
configuration/wire contract, not live host environment inheritance or real key
validation; those still need the approved installation test.

After an approved non-production endpoint and this contract are confirmed,
point the **local working copy** of `plugins/octolane/.mcp.json` at that
endpoint before loading it; keep this test-only URL change out of commits and
restore it after testing. Leave the public submission package unchanged. Use
`git diff -- plugins/octolane/.mcp.json` to inspect the exact local change.
Do not proceed while the package still targets production.

For a CLI session only, Rafi can privately enter the existing test workspace key
without putting it in shell history (zsh):

```sh
read -rs 'OCTOLANE_API_KEY?Existing non-production workspace key: '
printf '\n'
export OCTOLANE_API_KEY
"$CODEX_BIN"
unset OCTOLANE_API_KEY
```

This does not set the environment of an already running desktop app. For desktop
authentication use the host's supported private connection/environment flow;
confirm how this installed host supplies the variable first. Never put the key
in chat, a manifest, a command argument, screenshots or a committed .env file.
API-key sessions have no refresh credential; do not apply OAuth expiry/revoke
expectations to this path.

## 3. Run the backend in the existing development workflow

Use the existing backend checkout's environment and Docker Compose project,
not the isolated review checkout as a second competing runtime. Confirm the
running checkout/branch and that no demo or other task owns its service before
switching or restarting anything. These commands are for Rafi after that check:

```sh
# In the normal octolane-backend checkout, after approved branch integration:
docker compose ps mcp-service
# Start/rebuild only when explicitly safe for the shared local runtime:
docker compose up -d --build mcp-service
curl --fail http://localhost:5010/health
```

The inspected Compose service is `mcp-service`, port 5010; its source is mounted
and `apps/mcp` runs start:dev with the existing Infisical `/mcp` environment.
Primary, Redis and connected services must already point to the designated test
resources. Do not print secrets with `docker compose config`, bootstrap new keys,
run migrations or switch shared demo services for this guide. App edits may need
an approved service restart even with a source bind mount.

Backend PR #4649 must be present to test its refresh implementation. Issuance
defaults OFF. Enabling `MCP_OAUTH_REFRESH_ENABLED` is a separate approved test
configuration action, after every relevant validator supports the new format.
A host-accessible HTTPS issuer/base URL must match discovery; plain localhost
is reachable from local clients, not directly from ChatGPT's cloud.

The no-network regression command, from the review checkout, is:

```sh
APP_ROOT_PATH="$PWD" node_modules/.bin/jest --config apps/mcp/jest.config.ts \
  --runInBand --silent --runTestsByPath \
  apps/mcp/src/auth/client-refresh.test.ts apps/mcp/src/auth/router.test.ts \
  apps/mcp/src/auth/provider.test.ts apps/mcp/src/mcp/utils/instrument.test.ts \
  apps/mcp/src/mcp/server.keyRole.test.ts \
  apps/mcp/src/mcp/tools/toolDescriptionIntegrity.test.ts \
  apps/mcp/src/routes/mcp.scope.test.ts
node_modules/.bin/tsc --project apps/mcp/tsconfig.json --noEmit --pretty false
```

## 4. ChatGPT connector / public-package OAuth path

This is a separate test from loading the Codex key-header package. Use an
already approved HTTPS staging endpoint or an existing approved Secure MCP
Tunnel to the local server. Do not create a tunnel, OAuth client or grant as an
implicit part of this guide.

Current official UI: ChatGPT **Plugins → plus → Add custom MCP server**. Enter
the approved `/mcp` endpoint (or select the existing tunnel), choose OAuth,
review permissions, then **Create as a plugin**. Rafi must approve the named
ChatGPT account, Octolane workspace and exact connection first. Enter the key
only on Octolane's hosted consent page. Review discovered tools, start a new
conversation, and select the plugin with @.

This validates the MCP connection; it does not by itself test the packaged
listing assets or establish directory approval. Test the complete package's
listing in the supported local marketplace separately. A public package has
`submission/octolane/mcp.json`, uses discovery and contains no API-key
header. Do not upload the local legacy manifest as the public package.

Optional direct inspection, after approving tool download and endpoint access:

```sh
npx @modelcontextprotocol/inspector@latest
```

In Inspector select Streamable HTTP and the approved endpoint. Follow its
private authentication flow; do not put a key in command arguments. Record the
Inspector version used. The command is current official guidance, not a tool
that was installed or run in this task.

## 5. Reusable acceptance sequence

Record date, repo SHA, host/version, test workspace alias, granted scopes,
expected result, actual result, tool names, sanitized request IDs and screenshots
for each row in your normal test notes. Never record token values.

| Test | Expected result / control |
| --- | --- |
| Package appearance | Official icon in list, details and @/composer on light/dark; paths resolve after install. |
| Discovery | Enumerate all pages of tools/list and compare the unique names to docs/tool-inventory.json: exactly 72; inspect annotations and schemas. This is static inventory until a real discovery run passes. |
| Safe reads | First get_current_user: verify test workspace identity. Then list_pipelines and get_pipeline_overview on a known synthetic pipeline. Do not continue if tenant is wrong. |
| Controlled write | Separately approve one named synthetic deal and exact task text/due date. Create one task, read it back, record the ID. Do not retry an uncertain create blindly. |
| Destructive/outbound | Separate explicit record IDs for cleanup; separate sender, controlled recipient, content and time approval for email/calendar/invites. Never use prospects. |
| Isolation/permissions | With approved test roles and a second test tenant, foreign IDs fail without disclosure; read-only grant denies writes; narrowing cannot expand consent. |
| Successful OAuth renewal | After access expiry (one hour, without changing system clocks), ordinary use refreshes, saves successor and continues without redirect. Capture sanitized server/client evidence. |
| Rotation/replay | On synthetic staging sessions only: identical concurrent requests within 30 seconds share successor; later authentic replay revokes family. This intentionally destroys that test connection, so obtain approval. |
| Expiry | Mock time-advance tests cover 90-day inactivity. Do not change real grant TTLs/system clocks to speed a live test. Validate staged expiry through an approved test harness if needed. |
| Outage/recovery | Actual SDK auth() can REDIRECT after one HTTP500 without deleting tokens; a later explicit retry can recover. Test actual host retry/backoff/UX in an approved fault harness, not by taking shared Redis/primary offline. |
| Revoke | On an approved synthetic OAuth connection, revoke it and verify all descendants fail while another client's grant and the backing raw key still work. Do not disable the shared workspace key. |
| Existing connections | Exercise a safe read through an existing approved Claude/ChatGPT raw-key connection before/after staged rollout without reinstalling it; no forced migration or new OAuth TTL. Never disconnect real users for this test. |

Then run the eight cases in reviewer-walkthrough.md using bounded-test-plan.md.
Migration workflows remain out of scope. Published tool updates and direct
custom-connector metadata refresh are distinct: for the custom connection use
its **Refresh** control after an approved backend update, then a new chat.

## Evidence and prerequisites

Actually verified: official asset bytes and local light/dark rendering; local
CLI version/help; package schemas, deterministic ZIP and 16 tests. Prior backend
proof: 70 tests and full types, with synthetic Redis/primary and in-process SDK
HTTP. No installed-host screenshots, live discovery, reads/writes, OAuth grants,
refresh, production traffic or account-setting changes were performed here.

Needed from Rafi: normal runtime owner/checkout, approved non-production endpoint
and matching issuer, private bearer environment availability, existing subscribed test
workspace and second tenant/roles, chosen Codex/ChatGPT accounts, private key input
method and explicit install/OAuth approval. Approve write/revoke/replay/outage
batches separately. Real Redis Lua CAS, no-eviction durability, persistence and
failover remain staging release gates; family storage contains backing keys,
HMAC secrets and latest token response. Publisher/privacy/reviewer access/demo
and portal acceptance remain separate gates after technical acceptance.

Sources checked 23 October 2026: [Build plugins](https://developers.openai.com/plugins/build/plugins),
[Connect and test](https://developers.openai.com/plugins/deploy/connect-chatgpt),
[Codex plugins](https://developers.openai.com/codex/plugins),
and the bundled CLI's `plugin add --help` / `plugin marketplace add --help`.

Configuration evidence: [official compatibility parser](https://github.com/openai/codex/blob/main/codex-rs/codex-mcp/src/plugin_config.rs)
and [native MCP configuration](https://github.com/openai/codex/blob/main/codex-rs/config/src/mcp_types.rs).
