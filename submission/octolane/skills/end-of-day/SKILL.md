---
name: end-of-day
description: Close out the selling day by reviewing every customer call and email from today, updating the deals they touched, logging what happened and lining up tomorrow's follow-ups in one approval. Use for "end of day", "wrap up my day", or "update my CRM from today".
---

# End of day

## 1. Collect today

1. Meetings: `search_meetings` with `start_date` at 00:00 today and `end_date` now, both in the user's timezone, `only_mine: true`, `limit: 25`. Drop meetings whose attendees are all on the user's team (`list_workspace_members`).
2. Emails: for each outside company from those meetings, `search_emails` with `account_domain`. Then `search_emails` with `label: "sent"` and `limit: 25` to catch threads that had no meeting, and keep the ones sent today.
3. Group everything by company.

## 2. Work out the changes

For each company:

- Find its deal with `search_deals` and `account_name`.
- From meeting summaries and emails, propose: next step, next action date, stage (only when the stage description's criteria were met), tasks for anything the user promised, and a one-paragraph note.
- No deal and clear buying interest: propose creating one.

## 3. One review

Show a table: company | what happened today | proposed changes. Ask the user to approve all, some or none, or to edit.

## 4. Apply

- Deal fields: `bulk_update_deals` (at most 25 deals per call). Stages: `update_deal_stage`.
- Tasks: one `create_task` call with `tasks` rows.
- Notes: `create_note` per deal.
- New deals: `bulk_create_deals`.

## 5. Close out

Report what changed. Then call `get_tasks` with `status: "open"` and the due window for tomorrow, and list tomorrow's follow-ups. For any customer who is waiting on an email, offer the after-the-call skill to draft it.

## Rules

- The user's own instructions take priority over this skill.
- Change nothing without approval. Report failed writes and do not retry them automatically.
- Never invent outcomes for meetings that have no summary; list them as "no recording" instead.
