# Reviewer walkthrough — not recorded or executed

The five positive and three negative cases in the public `plugin.json` are draft review instructions based on the existing tool inventory. **All eight cases are Not run.** No fixtures, reviewer accounts, grants or credentials have been created by this task.

## Fixture preparation for a later authorized test run

Use two synthetic Octolane workspaces, a subscribed test user and a restricted-role user. Provide one pipeline with known totals and stages, two similarly named deals, known notes, and a deal suitable for a reversible stage change. Set an explicit timezone. Use an isolated test mailbox and a recipient controlled by the reviewer for scheduling; never use real prospects. Include a note containing an unrelated invitation instruction to test prompt-injection handling.

Obtain the actual deployed schemas before running cases. Resolve every required field and relationship; fixture labels are not fabricated UUIDs. For task dates and scheduled emails, record the test clock/timezone and expected saved date. Control pending scheduled emails and clean them up in the test environment after capture.

## Recording order

1. Show package version and host. Connect using Octolane's hosted key-paste page with the secret entry off camera; show successful workspace context afterwards.
2. Ask for workspace/pipeline overview and compare results with known fixtures.
3. Find the renewal deal, clarify duplicate matches and show its notes.
4. Create one linked task and verify the actual saved association/date.
5. Move the chosen deal to the requested valid stage, showing any required confirmation and the resulting state.
6. Schedule the approved email to the controlled test recipient with explicit content/date/timezone. Show the actual outcome and avoid uncertain retries.
7. Demonstrate foreign-workspace denial, ambiguous deletion clarification, and treating instructions embedded in a note as data.
8. Show a concise completion summary and correct record links. Stop the recording before any secret or unrelated customer content is visible.

Review the actual saved video for playback, readability, case coverage and exposed secrets. Host it at a reviewer-accessible URL, verify access and then populate the manifest's demo URL. Do not substitute a mockup or this script for the recording.

## Evidence to retain privately

For each case, record case ID, fixture version, host/build, prompt, selected tools/arguments, actual result, confirmation behavior and Passed/Failed/Blocked/Not run status. Verify all 72 tools separately, including role and negative input cases. Redact tokens and customer data; use a private approved evidence location. Reference sanitized evidence from `docs/release-gates.json` after completion.

## Reviewer access

Assign an owner for a dedicated sample-data account with needed subscription/service entitlements. Reviewers must be able to sign in without private-network access or a human mailbox/phone handoff. Do not change real customer authentication to achieve this. Put credentials and exact access steps only in secure dashboard review fields; never in manifests, this repository, fixtures, the video or the ZIP.
