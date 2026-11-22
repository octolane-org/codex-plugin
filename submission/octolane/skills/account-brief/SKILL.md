---
name: account-brief
description: Summarize everything Octolane knows about a company, covering contacts, deals, conversations, call themes, website visits and open work. Use for "what do we know about Acme", "account summary", or as the CRM half of an account plan the Sales plugin is building.
---

# Account brief

## Steps

1. `search_accounts` with `query` or `domain`, then `get_account_details`.
2. People: `search_contacts` with `company_name` and `limit: 50`.
3. Deals: `search_deals` with `account_name` across all stages, then `get_deal_details` for open ones.
4. Conversations: `search_emails` with `account_domain` and `limit: 15`; `search_meetings` with the company as `query`, `limit: 10`. Use summaries for themes.
5. Interest: `get_signal_visitors` with `search_query` set to the domain.
6. Open work: `get_notes` and `get_tasks` for the account.
7. Context: `memory_list` with `entity_type: "account"` and its `entity_id`; read any blocks with `memory_get`.

## Output

- **Snapshot:** what the company does (from the record), size, relationship status, total open pipeline.
- **Relationship map:** each contact, their role, who on our side talks to them, last touch.
- **Deal history:** open, won and lost, with dates and amounts as recorded.
- **What they care about:** priorities, objections and requests in their own words from calls and emails, each with its source.
- **Gaps:** no executive contact, a single-threaded deal, no meeting in 30 days.
- **Open commitments:** tasks and promises either side made.

To turn this into a full account plan with outside research, hand it to the Sales plugin.

## Rules

- The user's own instructions take priority over this skill.
- Separate what the record says from your own reading of it.
- This skill only reads.
