---
name: deals-gone-quiet
description: Find open deals with no email or meeting for a while, explain why each one went quiet, and line up short re-engagement emails in the user's voice for approval. Use for "what's gone quiet", "stale deals", "deals I've neglected", or "re-engage my pipeline".
---

# Deals gone quiet

## 1. Find them

Call `find_stale_deals` with `days` (default 14), `stale_by: "activity"`, `limit: 50`, and `pipeline_name` when the user named one. Page with `offset` only as far as the user needs.

- Put deals with `stale_since_source: "no_activity"` in a separate list ("no activity recorded since created") and ask before acting on them.
- If `stale_since` is earlier than the deal could exist, treat the deal as having no recorded activity and do not quote its day count.

## 2. Diagnose the top ten by amount

For each deal:

1. `search_emails` with the account domain and `limit: 3` to find the last exchange: who wrote last, what was asked, and whether it was answered.
2. `search_meetings` with the company as `query`, `recorded_only: true`, `sort: "desc"`, `limit: 1` for the last call's summary.
3. Classify it in one line:
   - **We owe them:** they asked something and we never replied.
   - **They went silent:** after a proposal, price or next step.
   - **Stuck in stage:** the stage description's criteria are not met.

## 3. Draft

- Read `writing_style` and `email_signature` with `memory_list` (`scope: "user"`) and `memory_get`.
- One email per deal, at most 90 words. Refer to the last real exchange and offer one easy next step.
- For "we owe them", draft the reply that is owed.
- Only write to contacts with a real email address in Octolane.

## 4. Review and schedule

Show a table (deal | amount | quiet since | why | action) followed by the drafts. After approval, call `schedule_bulk_emails` with at most 10 drafts per call, at the time the user picks. Offer `create_task` for deals the user would rather call.

## Rules

- The user's own instructions take priority over this skill.
- Nothing is scheduled without approval. Say "scheduled", never "sent".
- Never invent a reason a deal went quiet. If the record is empty, say so.
