# MCP tool inventory

72 statically registered tools from 70 registration calls, plus the four model-visible Octolane app tools added for 1.0.1 (76). Runtime verification: **Not run**.

Source: local backend checkout at `8dfd3c748335f268e9201654b84b7479c3e4f9ae`; this is not proof of production exposure or approval.

| Tool | Annotation group | Handler |
| --- | --- | --- |
| `search_deals` | `READ` | `apps/mcp/src/mcp/tools/handlers/search/searchOpportunities.ts` |
| `get_deal_details` | `READ` | `apps/mcp/src/mcp/tools/handlers/search/getOpportunityDetails.ts` |
| `search_contacts` | `READ` | `apps/mcp/src/mcp/tools/handlers/search/searchContacts.ts` |
| `get_contact_details` | `READ` | `apps/mcp/src/mcp/tools/handlers/search/getContactDetails.ts` |
| `search_accounts` | `READ` | `apps/mcp/src/mcp/tools/handlers/search/searchCompanies.ts` |
| `get_account_details` | `READ` | `apps/mcp/src/mcp/tools/handlers/search/getAccountDetails.ts` |
| `get_record_history` | `READ` | `apps/mcp/src/mcp/tools/handlers/search/getRecordHistory.ts` |
| `get_pipeline_overview` | `READ` | `apps/mcp/src/mcp/tools/handlers/search/getPipelineOverview.ts` |
| `search_emails` | `SYNC_READ` | `apps/mcp/src/mcp/tools/handlers/search/searchEmails.ts` |
| `get_email_thread` | `READ` | `apps/mcp/src/mcp/tools/handlers/search/getEmailThread.ts` |
| `schedule_bulk_emails` | `EXTERNAL_CREATE` | `apps/mcp/src/mcp/tools/handlers/create/scheduleBulkEmails.ts` |
| `update_scheduled_email` | `EXTERNAL_IDEMPOTENT_WRITE` | `apps/mcp/src/mcp/tools/handlers/update/updateScheduledEmail.ts` |
| `search_meetings` | `READ` | `apps/mcp/src/mcp/tools/handlers/search/searchMeetings.ts` |
| `get_meeting_details` | `READ` | `apps/mcp/src/mcp/tools/handlers/search/getMeetingDetails.ts` |
| `create_account` | `CREATE` | `apps/mcp/src/mcp/tools/handlers/create/createAccount.ts` |
| `create_contact` | `CREATE` | `apps/mcp/src/mcp/tools/handlers/create/createContact.ts` |
| `create_deal` | `CREATE` | `apps/mcp/src/mcp/tools/handlers/create/createOpportunity.ts` |
| `bulk_update_accounts` | `IDEMPOTENT_WRITE` | `apps/mcp/src/mcp/tools/handlers/update/bulkUpdateRecords.ts` |
| `bulk_update_contacts` | `IDEMPOTENT_WRITE` | `apps/mcp/src/mcp/tools/handlers/update/bulkUpdateRecords.ts` |
| `bulk_update_deals` | `IDEMPOTENT_WRITE` | `apps/mcp/src/mcp/tools/handlers/update/bulkUpdateRecords.ts` |
| `bulk_create_accounts` | `IDEMPOTENT_WRITE` | `apps/mcp/src/mcp/tools/handlers/create/bulkCreateAccounts.ts` |
| `bulk_create_contacts` | `IDEMPOTENT_WRITE` | `apps/mcp/src/mcp/tools/handlers/create/bulkCreateContacts.ts` |
| `bulk_create_deals` | `CREATE` | `apps/mcp/src/mcp/tools/handlers/create/bulkCreateOpportunities.ts` |
| `get_notes` | `READ` | `apps/mcp/src/mcp/tools/handlers/notes/getNotes.ts` |
| `create_note` | `CREATE` | `apps/mcp/src/mcp/tools/handlers/notes/createNote.ts` |
| `update_note` | `IDEMPOTENT_WRITE` | `apps/mcp/src/mcp/tools/handlers/notes/updateNote.ts` |
| `get_tasks` | `READ` | `apps/mcp/src/mcp/tools/handlers/tasks/getTasks.ts` |
| `create_task` | `CREATE` | `apps/mcp/src/mcp/tools/handlers/tasks/createTask.ts` |
| `update_task` | `IDEMPOTENT_WRITE` | `apps/mcp/src/mcp/tools/handlers/tasks/updateTask.ts` |
| `log_activity` | `CREATE` | `apps/mcp/src/mcp/tools/handlers/activities/logActivity.ts` |
| `update_activity` | `IDEMPOTENT_WRITE` | `apps/mcp/src/mcp/tools/handlers/activities/updateActivity.ts` |
| `get_current_user` | `READ` | `apps/mcp/src/mcp/tools/handlers/identity/whoami.ts` |
| `list_workspace_members` | `READ` | `apps/mcp/src/mcp/tools/handlers/identity/listWorkspaceMembers.ts` |
| `invite_team_member` | `EXTERNAL_CREATE` | `apps/mcp/src/mcp/tools/handlers/identity/inviteTeamMember.ts` |
| `get_signal_script` | `READ` | `apps/mcp/src/mcp/tools/handlers/signal/getSignalScript.ts` |
| `get_signal_visitors` | `READ` | `apps/mcp/src/mcp/tools/handlers/signal/getVisitors.ts` |
| `get_account_fields` | `READ` | `apps/mcp/src/mcp/tools/handlers/attributes/accountAttributes.ts` |
| `get_contact_fields` | `READ` | `apps/mcp/src/mcp/tools/handlers/attributes/contactAttributes.ts` |
| `get_deal_fields` | `READ` | `apps/mcp/src/mcp/tools/handlers/attributes/pipelineAttributes.ts` |
| `create_account_field` | `CREATE` | `apps/mcp/src/mcp/tools/handlers/attributes/createAccountField.ts` |
| `update_account_field` | `IDEMPOTENT_WRITE` | `apps/mcp/src/mcp/tools/handlers/attributes/updateAccountField.ts` |
| `delete_account_field` | `IDEMPOTENT_WRITE` | `apps/mcp/src/mcp/tools/handlers/attributes/deleteAccountField.ts` |
| `bulk_delete_account_fields` | `IDEMPOTENT_WRITE` | `apps/mcp/src/mcp/tools/handlers/attributes/bulkDeleteAccountFields.ts` |
| `create_contact_field` | `CREATE` | `apps/mcp/src/mcp/tools/handlers/attributes/createContactField.ts` |
| `update_contact_field` | `IDEMPOTENT_WRITE` | `apps/mcp/src/mcp/tools/handlers/attributes/updateContactField.ts` |
| `delete_contact_field` | `IDEMPOTENT_WRITE` | `apps/mcp/src/mcp/tools/handlers/attributes/deleteContactField.ts` |
| `bulk_delete_contact_fields` | `IDEMPOTENT_WRITE` | `apps/mcp/src/mcp/tools/handlers/attributes/bulkDeleteContactFields.ts` |
| `create_pipeline_field` | `CREATE` | `apps/mcp/src/mcp/tools/handlers/attributes/createPipelineField.ts` |
| `update_pipeline_field` | `IDEMPOTENT_WRITE` | `apps/mcp/src/mcp/tools/handlers/attributes/updatePipelineField.ts` |
| `delete_pipeline_field` | `IDEMPOTENT_WRITE` | `apps/mcp/src/mcp/tools/handlers/attributes/deletePipelineField.ts` |
| `bulk_delete_pipeline_fields` | `IDEMPOTENT_WRITE` | `apps/mcp/src/mcp/tools/handlers/attributes/bulkDeletePipelineFields.ts` |
| `create_pipeline` | `CREATE` | `apps/mcp/src/mcp/tools/handlers/pipeline/createPipeline.ts` |
| `delete_pipeline` | `IDEMPOTENT_WRITE` | `apps/mcp/src/mcp/tools/handlers/pipeline/deletePipeline.ts` |
| `rename_pipeline` | `IDEMPOTENT_WRITE` | `apps/mcp/src/mcp/tools/handlers/pipeline/renamePipeline.ts` |
| `list_pipeline_stages` | `READ` | `apps/mcp/src/mcp/tools/handlers/pipeline/listPipelineStages.ts` |
| `list_pipelines` | `READ` | `apps/mcp/src/mcp/tools/handlers/pipeline/listPipelines.ts` |
| `find_stale_deals` | `READ` | `apps/mcp/src/mcp/tools/handlers/search/findStaleDeals.ts` |
| `update_deal_stage` | `IDEMPOTENT_WRITE` | `apps/mcp/src/mcp/tools/handlers/pipeline/updateDealStage.ts` |
| `move_deal_to_next_stage` | `CREATE` | `apps/mcp/src/mcp/tools/handlers/pipeline/moveDealToNextStage.ts` |
| `bulk_upsert_stages` | `CREATE` | `apps/mcp/src/mcp/tools/handlers/pipeline/bulkUpsertStages.ts` |
| `bulk_delete_stages` | `IDEMPOTENT_WRITE` | `apps/mcp/src/mcp/tools/handlers/pipeline/bulkDeleteStages.ts` |
| `bulk_delete_deals` | `IDEMPOTENT_WRITE` | `apps/mcp/src/mcp/tools/handlers/delete/bulkDeleteOpportunities.ts` |
| `bulk_delete_accounts` | `IDEMPOTENT_WRITE` | `apps/mcp/src/mcp/tools/handlers/delete/bulkDeleteAccounts.ts` |
| `bulk_delete_contacts` | `IDEMPOTENT_WRITE` | `apps/mcp/src/mcp/tools/handlers/delete/bulkDeleteContacts.ts` |
| `bulk_delete_notes` | `IDEMPOTENT_WRITE` | `apps/mcp/src/mcp/tools/handlers/delete/bulkDeleteNotes.ts` |
| `bulk_delete_tasks` | `IDEMPOTENT_WRITE` | `apps/mcp/src/mcp/tools/handlers/delete/bulkDeleteTasks.ts` |
| `restore_deal` | `IDEMPOTENT_WRITE` | `apps/mcp/src/mcp/tools/handlers/delete/restoreOpportunity.ts` |
| `update_calendar_event` | `EXTERNAL_IDEMPOTENT_WRITE` | `apps/mcp/src/mcp/tools/handlers/calendar/updateCalendarEvent.ts` |
| `memory_list` | `READ` | `apps/mcp/src/mcp/tools/handlers/memory/listMemory.ts` |
| `memory_get` | `READ` | `apps/mcp/src/mcp/tools/handlers/memory/getMemory.ts` |
| `memory_upsert` | `IDEMPOTENT_WRITE` | `apps/mcp/src/mcp/tools/handlers/memory/upsertMemory.ts` |
| `memory_delete` | `IDEMPOTENT_WRITE` | `apps/mcp/src/mcp/tools/handlers/memory/deleteMemory.ts` |

## Added for 1.0.1

Registered by the Octolane app modules (OCT-4460, OCT-4490) in the backend `dev` branch from the merge of the home (`849fee102`), read from source, not from a production `tools/list`. Each is read-only and shows a card; none saves or sends anything until the user clicks a button on the card. The cards' own buttons call four more tools (`apply_deal_changes`, `create_visitor_deal`, `send_call_notetaker`, `set_home_task_done`). Those are hidden from the model (app-only) and are not listed. OpenAI holds new and changed tool definitions for manual review, and the three card tools register only where `MCP_APPS_CARDS_ENABLED` is on.

| Tool | Annotation group | Handler |
| --- | --- | --- |
| `show_octolane_home` | `READ` | `apps/mcp/src/mcp/apps/home/showOctolaneHome.ts` |
| `show_call_brief` | `READ` | `apps/mcp/src/mcp/apps/callBrief/showCallBrief.ts` |
| `show_website_visitors` | `READ` | `apps/mcp/src/mcp/apps/websiteVisitors/showWebsiteVisitors.ts` |
| `show_deal_changes` | `READ` | `apps/mcp/src/mcp/apps/dealChanges/showDealChanges.ts` |
