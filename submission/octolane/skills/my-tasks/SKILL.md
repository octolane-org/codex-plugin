---
name: my-tasks
description: Show the user's open follow-ups (overdue, due today and due this week) with the deal each one belongs to, and complete, reschedule or add tasks. Use for "what do I owe people", "my tasks", "what's overdue", or "remind me to send the proposal Friday".
---

# My tasks

## Review

1. Overdue: `get_tasks` with `status: "open"` and `due_before` set to the start of today in UTC.
2. Today and this week: `get_tasks` with `status: "open"`, `due_on_or_after` the start of today and `due_before` the end of the week, converting the user's local days to UTC.
3. Group the tasks: overdue (oldest first), today, this week. Show the linked deal or company for each, and flag any task tied to a deal closing this month.
4. When the user picks a task, offer the skill that does the work: draft-follow-up-email for an email, prepare-for-call for a call.

## Change

- Complete or reschedule: `update_task`, after the user says which tasks.
- Add: `create_task` with a short title, full `content`, `due_date` in the user's timezone, and a link to the deal, contact or account when there is one. Use `tasks` rows for several at once.

## Rules

- The user's own instructions take priority over this skill.
- Confirm before completing or moving tasks the user did not name.
- Do not retry a batch that returned an unknown outcome; check with `get_tasks` first.
