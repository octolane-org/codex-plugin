---
name: find-missing-deals
description: Find buying conversations in the user's email and meetings that have no deal in the CRM yet, show the evidence, and create the deals the user approves. Use for "what deals am I missing", "find opportunities in my inbox", or "who is interested but not in my pipeline".
---

# Find missing deals

## 1. Look for buying signals

1. Meetings: `search_meetings` with `start_date` 30 days ago and `limit: 25`. Page with `offset` while `hasMore` is true, up to 100 meetings.
2. Emails: `search_emails` with `keywords: ["pricing", "proposal", "quote", "trial", "contract", "order form", "security review", "procurement", "next steps", "demo"]` and `limit: 25`.

## 2. Keep real prospects

- Group by company domain.
- Drop the user's own domain (`list_workspace_members`), newsletters and calendar notifications.
- Drop vendors pitching the user. A prospect asks about the user's product; a vendor sells to the user.
- Never judge from `workspace_email_subjects`. Those are other people's mail and only show subjects.

## 3. Check the CRM

For each company, `search_deals` with `account_name` across all stages. Keep companies with no open deal. Note when a closed-lost deal exists.

## 4. Report

For each: company, the dated evidence (email subject or meeting title, with a short quote), the main contact, a suggested pipeline and stage, and an amount only when one was stated.

## 5. Create on approval

Call `bulk_create_deals` with `account.domain`, `primary_contact.email` taken from the evidence, the chosen pipeline and stage, and `next_steps`. Then add the evidence as a `create_note` on each new deal. Report anything returned under `skipped`.

## Rules

- The user's own instructions take priority over this skill.
- Use only email addresses that appear in the evidence. Never guess one.
- Create nothing without approval.
