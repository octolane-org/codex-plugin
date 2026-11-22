---
name: send-notetaker
description: Send Octolane's notetaker to record a specific meeting, so its transcript and summary land on the right deal for follow-up. Use for "record my next call", "send the notetaker to this meeting", or "join my 3pm with the recorder".
---

# Send the notetaker

## Steps

1. Find the meeting: use the join link if the user pasted one. Otherwise call `search_meetings` with `start_date` now, `sort: "asc"` and `only_mine: true`, then `get_meeting_details` to read the invite for its Google Meet, Zoom or Teams link.
2. If several meetings could match, or there is no link, ask the user.
3. Confirm the meeting title, time and link, then call `send_meeting_recorder` with the link copied exactly.
4. Report the result: "accepted to join" means accepted, not yet recording. If the result is uncertain, say so.

## Rules

- The user's own instructions take priority over this skill.
- Never build, shorten or guess a meeting link.
- Do not resend automatically after a timeout or an unclear result.
