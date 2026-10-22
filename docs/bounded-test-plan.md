# Proposed bounded live test plan — authorization pending

No live action is authorized by this worksheet. Keep workspace/account selection questions pending; do not request or put secrets in chat.

1. Identify an existing non-production subscribed workspace A, a separate synthetic workspace B, ChatGPT test account, role-test identities and a controlled test mailbox. Record their names/IDs privately. Confirm whether background enrichment, invitations, billing usage or automatic outreach could trigger; disable none without separate approval.
2. Present the exact connection target, requested OAuth scopes and account to Rafi for connection approval. This is separate from permission to create credentials, register clients or provision reviewer access.
3. After connection approval, list tools, reconcile the exact 72 names and schemas, and run bounded reads against synthetic fixtures only. Never enumerate unrelated customer records.
4. Before each write batch, present exact tool names, record IDs, fields, maximum record count, expected effects and cleanup steps. Use a unique OCT-4270-review prefix. Begin with one linked task and one reversible stage change on a synthetic deal. Do not infer deletion permission from creation permission.
5. For every deletion, request specific approval identifying the synthetic records and whether the action is reversible. Record IDs at creation. Never wildcard-delete by prefix alone.
6. For email/calendar/invitation tools, obtain explicit approval of sender, exact recipient addresses controlled by the tester, subject/body, date/timezone and maximum sends/invites. Scheduling can result in a real send; cancellation is not guaranteed. Do not send to arbitrary recipients or use real prospects. Unknown outcomes stop retries until checked.
7. Expand to remaining tools only through similarly bounded batches. Use `runtime-evidence.md`; record actual outcomes, negative input cases, role/subscription results, tenant denial, retry semantics and cleanup. Changing roles/subscriptions or provisioning fixtures/access requires its own permission where not already authorized.
8. Execute the five positive and three negative review scenarios, then record the actual successful flows. Keep secrets off camera. Verify the recording and proposed hosting access before uploading or sharing. Reviewer credentials go only into approved secure portal fields.

Existing local mock tests establish narrow contracts, not live authorization or end-to-end readiness. No production endpoint mutations, credential/access creation, deployment, public upload or submission are included in this plan.
