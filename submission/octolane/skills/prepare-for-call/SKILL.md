---
name: prepare-for-call
description: Brief the user before a sales call or customer meeting from Octolane's deals, emails, recorded calls, notes, tasks and website visits. Use for "prep me for my next call", "brief me on tomorrow's demo with Acme", or "what do I need to know before meeting Sarah". Works alongside the Sales plugin's research skills.
---

# Prepare for a call

Give the user a brief they can read in two minutes, built only from what Octolane holds.

## 1. Find the meeting

- If the user named a company or person, call `search_meetings` with that `query`, `start_date` now and `sort: "asc"`.
- For "my next call", call `search_meetings` with `start_date` now, `sort: "asc"`, `only_mine: true` and `limit: 5`. Pick the first meeting with an attendee outside the user's company (compare email domains with `list_workspace_members`). Skip internal meetings.
- If two meetings are equally likely, ask which one.

## 2. Gather context

1. People and company: `search_contacts` with `keywords` set to the attendee emails, `search_accounts` with `domain`, then `get_account_details`.
2. Deal: `search_deals` with `account_name`. If there is one open deal, call `get_deal_details`. Call `get_pipeline_overview` for that pipeline and read the deal's stage `description`: it says what the deal needs to move on.
3. Conversations: `search_emails` with `account_domain` and `limit: 10`; `search_meetings` with the company as `query`, `recorded_only: true`, `sort: "desc"`, `limit: 3`. Work from the meeting summaries. Open `get_meeting_details` only for the most recent call, and only if its summary lacks the agreed next steps.
4. Open work: `get_notes` and `get_tasks` for the deal or account.
5. Interest: `get_signal_visitors` with `search_query` set to the domain. Mention recent visits only as returned.
6. Rules and context: `memory_list` with `scope: "org"`; read `sales_process`, `pricing` and `product_info` with `memory_get` when they exist, and any block scoped to this account.

## 3. Write the brief

- **Meeting:** title, time in the user's timezone, attendees with title when known.
- **Where it stands:** stage, amount, close date, next step, days since the last email or meeting, and what the stage still needs.
- **So far:** three to five dated bullets, each naming the email subject or meeting it comes from.
- **Open questions and risks:** missing decision maker, unanswered objection, passed close date, silence.
- **Goal for this call** and **three questions to ask**.
- **What we owe them:** open tasks and promises from earlier calls.

## 4. Show the brief card

When `show_call_brief` is available, call it once for the meeting after you write the brief:

- `meeting_id`: the meeting from `search_meetings`.
- `deal_id`: the deal from `search_deals`, when there is one. Leave it out when there is none.
- `things_to_know`: at most three items, each taken only from what you found and naming its email or meeting. Never a guess.
- `goal`: what the user should get out of this call, in one sentence.

The card shows the time, link, attendees, the deal's stage, amount and close date, the goal, and Send notetaker and Open in Octolane buttons. Nothing is sent until the user clicks Send notetaker, so never say a notetaker is on the way. Then say in one sentence the main open question for the call.

If the card tool is not available, the written brief is the answer.

## 5. Offer next steps

- Outside research (news, funding, competitors, business case): suggest the Sales plugin's research skills and merge their output into the brief. Do not browse the web unless the user asks.
- No open deal and clear buying interest: offer once to create one with the create-deal skill.
- The meeting has a join link and the user wants it recorded: the card's Send notetaker button does it, or use the send-notetaker skill if there is no card.

## Rules

- The user's own instructions take priority over this skill.
- Write "not in Octolane" when something is missing. Never invent titles, amounts, dates or quotes.
- This skill only reads. Make no changes unless the user asks.
