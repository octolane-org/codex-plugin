---
name: log-activity
description: Log phone calls, in-person meetings, LinkedIn, text and WhatsApp conversations that Octolane cannot see, set the follow-up, and update the deal if it changed. Use for "log a call with Sarah", "I met the Acme team today", or "note that I messaged them on LinkedIn". Gmail and Google Calendar sync automatically, so never log those.
---

# Log activity

## Steps

1. Resolve the record: `search_contacts` or `search_accounts`. If it does not exist, offer `create_contact` (only with a real email) or `create_account` (with a domain), and create it only on a yes.
2. Call `log_activity` with:
   - `activity_type`: CALL, IN_PERSON_MEETING, LINKEDIN_MESSAGE, TEXT_MESSAGE, WHATSAPP_MESSAGE, X_ACTIVITY or COMMENT;
   - `object_type` and `object_id`;
   - a short `title`, the user's notes as `description`, and `occurred_at`;
   - `participants` copied from the contact search.
3. If the user mentioned a next step, create it with `create_task` linked to the record, with a due date.
4. If what happened changes the deal (stage, next step, close date, amount), propose the change and apply it with `bulk_update_deals` or `update_deal_stage` only after approval.

## Rules

- The user's own instructions take priority over this skill.
- Log only what the user said happened.
- Do not log Gmail emails or Google Calendar meetings; Octolane already has them.
