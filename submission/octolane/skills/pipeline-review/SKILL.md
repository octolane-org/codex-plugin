---
name: pipeline-review
description: Show what needs attention in the pipeline today, covering deals closing soon, deals past their close date, deals gone quiet, overdue follow-ups and stage health, ranked with one next action each. Use for "how's my pipeline", "what needs attention", "morning review", or "which deals are at risk this month". Works alongside the Sales plugin's pipeline risk review.
---

# Pipeline review

## 1. Pick the pipeline

Call `list_pipelines`. Use the pipeline the user named. Otherwise, if several pipelines hold open deals, ask once which to review; suggest the main sales pipeline.

## 2. Gather

1. Health: `get_pipeline_overview` with `pipeline_name`. Quote `deals_with_value` next to `avg_deal_size`.
2. Closing this month: `search_deals` with `pipeline_name`, `close_date_from` today and `close_date_to` the month's last day, `limit: 50`.
3. Past close date: `search_deals` with `pipeline_name` and `additional_filters: [{"property_name": "opportunity_close_date", "condition": "before_today"}]`. Leave out won and lost stages.
4. Quiet: `find_stale_deals` with `days: 14` and `pipeline_name`. List deals whose `stale_since_source` is `no_activity` separately, as "no activity recorded since created".
5. Overdue: `get_tasks` with `status: "open"` and `due_before` now.

## 3. Report

- **Health line:** open deals and value by stage, from the overview.
- **Needs attention today:** at most seven deals ranked by value and urgency (closing soon and quiet ranks first). For each: why it needs attention, and one concrete next action.
- **Quiet deals:** count and total value, top five by amount.
- **Overdue follow-ups:** count, with the three oldest.

## 4. Offer

Draft re-engagement emails (deals-gone-quiet skill), set close dates or next steps, create tasks, or brief one deal (deal-context skill). Ask before any change.

## Rules

- The user's own instructions take priority over this skill.
- Quote amounts and dates exactly as recorded. Do not forecast numbers Octolane does not hold.
- This skill only reads until the user approves a change.
