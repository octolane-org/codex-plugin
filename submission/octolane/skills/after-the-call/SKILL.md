---
name: after-the-call
description: Turn a finished sales call into a follow-up email in the user's voice, deal updates, tasks and a call note, from Octolane's own recording of the call. Use for "follow up on my call with Acme", "write the recap from today's demo", or "update the deal from that call". Works alongside the Sales plugin's Follow Up After Call skill.
---

# After the call

Octolane's notetaker recorded the call, so the user does not paste notes. Prepare everything, show it once, and write only what the user approves.

## 1. Find and read the call

1. Call `search_meetings` with `recorded_only: true`, `sort: "desc"`, `limit: 5`, and the company as `query` when the user named one. Confirm the meeting if more than one fits.
2. Call `get_meeting_details`. Read the summary first. Page through the transcript with `transcript_offset` only to confirm commitments, numbers or dates.
3. No recording: ask the user to paste notes or say what happened, and continue from that.

## 2. Gather context

- Deal: `search_deals` with `account_name`, then `get_deal_details`, `list_pipeline_stages` for its pipeline, and `get_deal_fields` before changing any custom field.
- Thread: `search_emails` with the main contact's `contact_email`, then `get_email_thread` for the latest thread.
- Voice: `memory_list` with `scope: "user"`; read `writing_style`, `email_signature` and `scheduling_link` with `memory_get` when they exist.

## 3. Extract from the call

Decisions, commitments (who, what, by when), objections, new people and their roles, timeline, budget and next meeting. Attribute words to a speaker only when the transcript shows them.

## 4. Show one review

a. **Customer email:** to (attendee emails from the meeting), subject, body in the user's voice that recaps decisions and ends with the agreed next step, plus the saved signature and scheduling link.
b. **Internal summary:** five bullets with owners and dates.
c. **CRM changes** as before → after:
   - stage, only when the stage description's exit criteria were met on the call;
   - next step, next action date, close date;
   - amount, only when a number was stated;
   - new contacts with real email addresses;
   - tasks with owner and due date.

When `show_deal_changes` is available, show the stage, next step, close date and amount changes, and the follow-up tasks, as a card instead of a list. Call it once with:

- `deal_id`: the deal's `opportunity_id`.
- `meeting_id`: the call, so the quotes can be checked.
- `changes`: only changes the call supports. `field` is `stage` (a stage name from the deal's own pipeline), `amount` (a plain number), `close_date` (YYYY-MM-DD) or `next_step`. For each, `quote` is the exact words someone said, copied verbatim from the transcript. Never paraphrase or invent one: the card shows a quote only if it finds it in the call.
- `tasks`: the follow-ups the call produced, each with a short `title` and an optional `due_date` (YYYY-MM-DD).

The user ticks the changes they accept and clicks Apply on the card. Nothing is saved until then, so never say the changes are saved. New contacts, the internal note and the email stay in the review below, as text.

Ask for approval. The user can approve all, some, or edit any part.

## 5. Apply what was approved

- Stage, deal fields and tasks: the card's Apply button writes what the user ticked, so do not write those again. Without the card, stage: `update_deal_stage`; other deal fields: `bulk_update_deals`; tasks: `create_task` with `tasks` rows linked by `entity_type: "opportunity"`.
- Summary: `create_note` on the deal.
- Email: recap recipients, subject and send time, then `schedule_bulk_emails` from the user's connected mailbox. Default send time: 9:00 the next business morning in the user's timezone.

Report every change with the IDs returned. If a write fails, say which one and do not retry it automatically.

## Rules

- The user's own instructions take priority over this skill.
- Nothing is written or scheduled without approval. Say "scheduled", never "sent".
- No deal and clear buying interest on the call: offer to create one first with the create-deal skill.
