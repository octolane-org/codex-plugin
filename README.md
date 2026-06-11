# Octolane AI CRM Codex Plugin

This repository is a Codex plugin marketplace for Octolane AI CRM. It publishes the `octolane-ai-crm` plugin, which connects Codex to Octolane's hosted MCP server.

## Install

Add this marketplace to Codex:

```bash
codex plugin marketplace add octolane/codex-plugin
```

Then open Codex, go to Plugins, find `Octolane AI CRM`, and install it.

If you are installing from a local checkout while testing:

```bash
codex plugin marketplace add /path/to/codex-plugin
```

## Authentication

Generate an Octolane API key from the Octolane dashboard under Settings > Integrations > API, then expose it to Codex as `OCTOLANE_API_KEY`.

```bash
export OCTOLANE_API_KEY="your_octolane_api_key"
```

The plugin sends this key to Octolane MCP using the `X-API-Key` header.

## Capabilities

The plugin enables Codex to use Octolane MCP for pipeline reviews, deal search and updates, contact and account lookup, task management, meeting prep, and Signal website visitor intelligence.

Example prompts:

- Show my Octolane pipeline overview.
- Find stale deals in Octolane.
- Prepare me for my next sales call.

## Repository Layout

```text
.agents/plugins/marketplace.json
plugins/octolane-ai-crm/.codex-plugin/plugin.json
plugins/octolane-ai-crm/.mcp.json
README.md
LICENSE
```

## Validate

From the repository root:

```bash
python3 /path/to/plugin-creator/scripts/validate_plugin.py plugins/octolane-ai-crm
python3 -m json.tool .agents/plugins/marketplace.json >/dev/null
python3 -m json.tool plugins/octolane-ai-crm/.codex-plugin/plugin.json >/dev/null
python3 -m json.tool plugins/octolane-ai-crm/.mcp.json >/dev/null
```

## Marketplace Metadata

- Marketplace name: `octolane`
- Marketplace display name: `Octolane`
- Plugin name: `octolane-ai-crm`
- Plugin display name: `Octolane AI CRM`
- Category: `Productivity`
- Installation policy: `AVAILABLE`
- Authentication policy: `ON_INSTALL`
