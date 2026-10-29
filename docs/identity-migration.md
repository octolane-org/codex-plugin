# Octolane package identity migration

The unpublished package is now `octolane`, with marketplace `octolane` and selector `octolane@octolane`. Display name remains Octolane; subtitle remains Revenue Superintelligence. Version remains 0.2.0 for this newly named draft.

Sources moved from `plugins/octolane-ai-crm/` to `plugins/octolane/` and from `submission/octolane-ai-crm/` to `submission/octolane/`. Catalog, validation, tests and active setup documentation use the new paths. Previous ZIPs and checksums are retained in dist unchanged.

## Existing local installation

This source change does not rename an installed `octolane-ai-crm@octolane`, migrate its connection or remove its cache. Before recording, inspect `codex plugin marketplace list` and `codex plugin list` and identify the existing entry. Add this repository's marketplace if needed, restart the desktop app, then install Octolane from that source (CLI equivalent: `codex plugin add octolane@octolane`). This is a separate installation and may request authentication because the catalog policy remains ON_INSTALL. Verify the new identity and intended test workspace before using it. Do not activate both entries in a test conversation.

Keep the old installation until the replacement is verified. Removal is a separate explicit user decision; do not uninstall, delete cache or disconnect it as an automatic rename step. Git marketplace upgrade is not a verified local-folder cache refresh.

## Portal replacement

Upload `dist/octolane-0.2.0-draft.zip` only to the newly authorized replacement draft. Do not upload it as a rename of an existing portal identity: the portal previously enforced name matching. Preserve the old draft until the replacement is verified. Its credentials, domain challenge, validation and review state are not presumed transferred; use values and requirements from the replacement itself. No private App binding belongs in this ZIP.

The local package retains OCTOLANE_API_KEY native bearer binding. The portable package retains OAuth with baseScopes [crm:read, crm:write] and defaultScopes [], with no key headers. Both retain the same endpoint, listing and assets. This rename does not authorize installation, OAuth grants, writes or submission. Repository release gates remain pending until evidence is recorded; user-reported reviewer-form completion alone is not runtime verification.
