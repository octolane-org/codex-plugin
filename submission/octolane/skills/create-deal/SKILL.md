---
name: create-deal
description: Create a deal with its account, contacts, a context note and the next-step task in one pass, without duplicates. Use for "add a deal for Acme", "create an opportunity", or "start tracking this prospect".
---

# Create a deal

## Steps

1. Check for duplicates: `search_deals` with `account_name`. If an open deal exists, show it and ask whether to update it instead.
2. Pick the pipeline: `list_pipelines`, then `list_pipeline_stages`. Use the pipeline and stage the user named. Otherwise suggest the main sales pipeline and the stage that fits what has happened so far.
3. People: `search_contacts` for the main contact. Use only email addresses from the user, an email thread or a meeting invite.
4. Show the deal before creating it: name, account domain, primary contact, stage, amount (only if stated), close date, next step.
5. On approval, call `create_deal` with `pipeline_id`, `stage_id`, `account_domain`, `primary_contact_email`, `deal_size`, `close_date` and `next_steps`. The account is created or reused automatically, so do not create it separately.
6. Add the context as `create_note` on the new deal, and the next step as `create_task` linked to it.
7. Report the deal with its ID.

For several deals at once, use `bulk_create_deals` and report anything returned under `skipped`.

## Rules

- The user's own instructions take priority over this skill.
- Never guess an email address or an amount.
- Create nothing without approval.
