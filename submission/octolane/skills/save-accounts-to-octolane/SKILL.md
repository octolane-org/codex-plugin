---
name: save-accounts-to-octolane
description: Save companies and people from a pasted list, an uploaded file, a research result or another plugin's output (such as the Sales plugin's enrichment) into Octolane without duplicates, optionally creating deals. Use for "add these companies to my CRM", "import this list", or "save these leads".
---

# Save accounts to Octolane

## Steps

1. Read the input and build two lists: companies (name and domain) and people (name, email, title, company domain). Set aside rows with no domain and no email.
2. Check for duplicates:
   - companies: `search_accounts` with `keywords`, ten domains per call;
   - people: `search_contacts` with `keywords`, ten emails per call.
3. Show the plan: how many are new, already in Octolane, or skipped (with the reason), and a sample of each.
4. On approval:
   - companies: `bulk_create_accounts`, at most 50 per call;
   - people: `bulk_create_contacts`, at most 50 per call;
   - deals, if asked: `bulk_create_deals` with an inline `account` and `primary_contact`, in the pipeline and stage the user picks.
5. Report created, existing, skipped and failed counts. List failures by row.

## Rules

- The user's own instructions take priority over this skill.
- Never make up an email address or domain to fill a gap.
- Create nothing without approval.
