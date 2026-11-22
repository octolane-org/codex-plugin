---
name: website-visitors-to-pipeline
description: Turn companies visiting the user's website into pipeline with Octolane Signal by showing who visited, how interested they look, how well they fit the ICP and whether they are already in the CRM, then creating deals for the ones worth pursuing. Use for "who visited our site", "website visitors this week", "turn site traffic into leads", or "which accounts are showing intent". Hands account research to the Sales plugin.
---

# Website visitors to pipeline

Octolane Signal identifies the companies behind anonymous website traffic. It identifies companies, not people.

## 1. Get visitors

Call `get_signal_visitors` once and let its filters do the narrowing:

- `last_visited_after`: the start of the window as a date, `YYYY-MM-DD` (UTC). Default: 7 days ago.
- `min_intent: 60`, unless the user wants a wider net. Scores run 20 to 80, and 60 or more is strong.
- `sort: "intent"` and `limit: 50`. Ask for a second page only if the user wants more than 50.
- `crm_status`, only when the user asks for one slice: `not_in_crm`, `account_no_deal`, `open_deal` or `closed_deal`. Otherwise leave it out and report every status.
- `page_contains`, only when the user names a page, for example `["/pricing"]`.

Every company comes back with its most viewed `pages`, its `crm_status` and its `open_deal`.

If nothing comes back, call again without the filters. An empty list then means Signal is not installed: call `get_signal_script`, give the user the install steps and stop. Otherwise tell the user nothing matched and offer a longer window or a lower `min_intent`.

## 2. Filter

- Drop the user's own company, internet providers, universities and personal email providers, unless the user sells to them.
- Skip locked companies (`is_locked` is true): they have no name, pages or status. Tell the user how many were locked.

## 3. Score fit

Read the `sales_icp` memory block (`memory_list` with `scope: "org"`, then `memory_get`). Rate each company high, medium or low with a one-line reason. If no ICP is saved, say fit is unscored and offer the teach-octolane skill.

## 4. Read the CRM status

Do not call `search_accounts` or `search_deals` for each company: the status is already on every row. Tag each company by its `crm_status`:

- `not_in_crm`: new company.
- `account_no_deal`: known account with no deal.
- `open_deal`: open deal. Name its stage from `open_deal`.
- `closed_deal`: customer or lost before. The status does not say which. For the few that make the list and need it, call `search_deals` with `account_name` and read the deal's stage.

The status matches accounts by domain, so a company saved under a different domain shows as `not_in_crm`.

## 5. Report

Show a ranked list: company, domain, intent score, sessions, last visit, top pages, fit, CRM status and a suggested action. Then highlight the top three with "why now".

## 6. Act on approval

- **Create deals:** `bulk_create_deals` with `account.domain`, the pipeline the user picks from `list_pipelines`, and `next_steps` such as "Reach out: visited the site on <date>".
- **Find people:** Octolane does not find new people at a company. Suggest the Sales plugin's Enrich Company And Contact Data skill or a data plugin, then save the results with the save-accounts-to-octolane skill.
- **Account plan:** hand the Octolane facts (visits, CRM history, fit) to the Sales plugin's Analyze Account Signals skill or account plan prompt.
- **Outreach:** only to contacts with real email addresses. Draft, get approval, then `schedule_bulk_emails`.

## Rules

- The user's own instructions take priority over this skill.
- Never say a named person visited, or name pages the tool did not return.
- Create nothing and schedule nothing without approval.
