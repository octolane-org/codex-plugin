---
name: get-started
description: Set up Octolane after it is installed. Use when the user has just connected Octolane, asks how to start, or asks what Octolane can do. Checks the connection, the workspace, email and calendar sync and the saved sales context, then offers four starter tasks.
---

# Get started with Octolane

Octolane is a CRM that builds itself from the user's Gmail, Google Calendar and recorded calls. This skill confirms it works and gets the user to a first useful result in the same conversation.

## Steps

1. Call `get_current_user`. Greet the user by name and name the connected workspace. If the call fails, the connection is missing or expired: ask the user to reconnect Octolane in ChatGPT's plugin settings, and stop.
2. Call `list_pipelines`. Report each pipeline and its deal count. If there are none, explain that Octolane creates accounts and contacts as it reads email and meetings, and that a pipeline can be created when they want one.
3. Check that conversations are flowing: call `search_meetings` with `start_date` 14 days ago and `limit` 3, and `search_emails` with `limit` 3. If both come back empty, tell the user to connect Gmail and Google Calendar in Octolane under Settings, Integrations.
4. Call `memory_list` with `scope: "org"`, then with `scope: "user"`. Say which of these are saved and which are empty: ICP (`sales_icp`), pricing, sales process, product info, writing style, email signature, scheduling link. Empty blocks make drafts and fit scores generic. Offer once to fill them with the teach-octolane skill.
5. Offer four starter tasks, one line each, and ask which to run:
   - Prepare for your next call
   - Find deals that have gone quiet
   - See which companies visited your website this week
   - Find buying conversations that have no deal yet

## Rules

- The user's own instructions take priority over this skill.
- Report only what the tools return. Do not estimate counts or invent names.
- Change nothing in this skill, except saving memory the user explicitly gives you.
