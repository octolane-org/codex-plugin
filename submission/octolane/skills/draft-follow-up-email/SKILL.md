---
name: draft-follow-up-email
description: Draft an email to a contact in the user's own voice, grounded in the real thread and the deal, then schedule it from the user's Gmail after approval. Use for "email Sarah", "reply to Acme", "send a follow-up", or "nudge them about the proposal".
---

# Draft a follow-up email

## Steps

1. Resolve the recipient: `search_contacts` with `query`. If several people match, ask which one.
2. Read the thread: `search_emails` with `contact_email`, then `get_email_thread` for the latest relevant thread.
3. Read the deal: `search_deals` with `account_name`, then `get_deal_details` for the stage and next step.
4. Read the voice: `memory_list` with `scope: "user"`, then `memory_get` for `writing_style`, `email_signature` and `scheduling_link`. With no saved style, match the tone of the user's own messages in that thread.
5. Read the facts: use the `pricing` and `product_info` memory blocks only when the email needs them.
6. Draft: subject, to, cc, and a body that answers what they last asked and ends with one clear next step. Keep it short unless the user asks for more.
7. Show the draft and revise it until the user is happy.
8. Recap the recipients, subject and send time, then call `schedule_bulk_emails` from the user's connected mailbox. Keep the returned `scheduled_mail_ids` in case the user wants to change it, which `update_scheduled_email` can do.

## Rules

- The user's own instructions take priority over this skill.
- Never invent prices, dates, attachments, features or promises.
- Nothing is scheduled without approval. Say "scheduled", never "sent".
