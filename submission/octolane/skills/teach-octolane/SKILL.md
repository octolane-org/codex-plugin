---
name: teach-octolane
description: Save the user's ICP, pricing, sales process, product facts, writing style, email signature and scheduling link to Octolane memory, so every brief, fit score and draft uses them. Use for "remember our ICP is...", "learn my writing style", "save my signature", or "here's our pricing".
---

# Teach Octolane

## Steps

1. Show what is saved: `memory_list` with `scope: "both"`. List each category as saved or empty.
2. Save what the user gives you with `memory_upsert`:
   - Workspace-wide (`scope: "org"`, needs an admin): `sales_icp`, `pricing`, `sales_process`, `product_info`, `company_description`, `website`, `documentation`, `support_email`.
   - Personal (`scope: "user"`): `writing_style`, `email_signature`, `scheduling_link`, `role`.
   - Anything else: `category: "custom"` with a short `title`.
3. Writing style from real mail: when the user asks, read the user's 10 most recent sent emails (`search_emails` with `label: "sent"` and `limit: 10`). Describe their greeting, length, tone, sign-off and habits in a few lines, show it, and save it only after approval.
4. Check `saved` in each response. If it is false, report what is actually stored instead of what you asked for.
5. If an org write is refused because the user is not an admin, offer to save it to their personal scope and say who can save it for the workspace.

## Rules

- The user's own instructions take priority over this skill.
- Save only durable facts the user confirms, not passing remarks.
- Never save passwords, keys or other secrets.
