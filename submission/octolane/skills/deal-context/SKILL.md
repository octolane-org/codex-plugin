---
name: deal-context
description: Catch the user up on one deal by showing where it stands, everything that happened, who is involved, what changed and the best next step. Use for "catch me up on Acme", "where are we with the Globex deal", or "what happened on this deal".
---

# Deal context

## Steps

1. Find the deal: `search_deals` with `search_query`. If several match, ask which one.
2. `get_deal_details`, then `get_record_history` for stage, amount and close date changes.
3. Read the stage `description` from `get_pipeline_overview` for that pipeline.
4. People: `search_contacts` with `company_name`. Note each person's title and last interaction.
5. Conversations: `search_emails` with `account_domain` and `limit: 10`; `search_meetings` with the company as `query` and `sort: "desc"`, using the summaries.
6. `get_notes` and `get_tasks` for the deal.

## Output

- **Status line:** stage, amount, close date, owner, last touch.
- **Timeline:** dated bullets, newest first, each naming its source.
- **People:** who we talk to, their role, last contact. Flag a missing decision maker.
- **Gaps against the stage:** what the stage description needs that has not happened yet.
- **Next best step**, and offer to save it as the deal's next step and next action date.

## Rules

- The user's own instructions take priority over this skill.
- Quote only what the record holds. Say "not recorded" for missing fields.
- Change nothing without approval.
