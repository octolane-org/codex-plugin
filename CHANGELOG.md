# Changelog

## 1.0.1 — unpublished candidate, 2026-11-25

Follows 1.0.0, which was submitted for review on 21 November 2026. This record does not confirm its approval or publication (OCT-4407, item 6).

- Declare the `Interactive` capability beside `Read` and `Write` in the listing, and add two lines to the long description: the Octolane home in ChatGPT, and call briefs, website visitors and deal changes as cards that act only when the user clicks.
- Make four skills use the new Octolane tools when they are available, with the written flow as the fallback when they are not: `prepare-for-call` shows `show_call_brief`, `after-the-call` shows `show_deal_changes`, `website-visitors-to-pipeline` shows `show_website_visitors` once per request, and `get-started` offers `show_octolane_home`. Each says the action has not happened until the user clicks.
- Add four positive review cases, one per surface (the home and the three cards), and the four model-visible tools to the tool inventory (76). The four app-only tools the card buttons call are hidden from the model and are not listed.
- Keep the three starter prompts: OpenAI allows at most three. `end-of-day` is unchanged: the deal changes card covers one deal at a time.
- The validator now also checks the capabilities (up to 20 one-line entries of at most 120 characters, including Read, Write and Interactive) and the new inventory and case counts. The local Codex package carries the same version and listing. CI validates the 1.0.1 draft ZIP.

See [candidate evidence](docs/releases/1.0.1-candidate.md).

## 1.0.0 — unpublished candidate, 2026-11-21

Follows 0.2.1, which the ChatGPT listing showed as its live version on 21 November 2026 (OCT-4407).

- Add 17 skills under `submission/octolane/skills/`, each a `SKILL.md` and an `agents/openai.yaml` that points at the Octolane MCP server: get started, prepare for call, after the call, end of day, pipeline review, deals gone quiet, website visitors to pipeline, find missing deals, deal context, account brief, draft follow-up email, log activity, create deal, my tasks, teach Octolane, save accounts, send notetaker.
- Move the listing to the Sales category with a new description, three starter prompts, SVG composer icons for light and dark, `brandColorDark` and `get-started` as the onboarding skill. The local Codex package carries the same listing text and icons.
- Keep the OAuth declaration, the MIT license, `repository` and the five positive and three negative review cases from 0.2.1. The PNG logos are unchanged.
- `website-visitors-to-pipeline` reads each company's CRM status and most viewed pages from one `get_signal_visitors` call with `last_visited_after`, `min_intent` and `crm_status` (OCT-4456), instead of searching accounts and deals per company. Upload this version only after that backend change is live.
- The validator and tests cover the skills, the SVG icons, the category and the onboarding skill. CI validates the 1.0.0 draft ZIP.

## 0.2.1 — unpublished candidate, 2026-11-01

- Replace the inset rounded icon with Vitor’s supplied 1024px square PNGs.
- Share logo/composer assets and add matching dark-theme fields in both packages.
- Preserve OAuth/API-key configuration and the immutable 0.2.0 artifact.
- Enforce the exact four-file candidate inventory, dark-image parity and safe paths.

See [candidate checks and remaining gates](docs/releases/0.2.1-candidate.md).

## 0.2.0 — 2026-10-29

Published as **Octolane — Revenue Superintelligence** in the ChatGPT plugin directory.

- Add the portable OAuth submission package, official Octolane icons, listing copy, starter prompts and reviewer scenarios.
- Declare CRM read and write scopes for the existing hosted MCP endpoint, without embedding credentials or filtering its 72-tool surface.
- Rename the package to `octolane`; retain the `octolane` local marketplace and native `OCTOLANE_API_KEY` bearer binding.
- Add deterministic four-file ZIP builds, schema validation, package tests and reviewer/testing documentation.

The portal manages the registered App, reviewer access, demo URL and publication. The MCP backend implements the tools and authentication; those implementations are not shipped in this ZIP. No migration skill ships in this release.

See [the immutable artifact and publication record](docs/releases/0.2.0.md). Documentation-only reconciliation after publication does not increment the package version. The local 0.2.1 desktop compatibility experiment is not a release and is excluded from this PR.

## 0.1.0 — historical local package

Initial Codex marketplace package was committed on 10 June 2026; category and logo updates followed on 12 June. This is repository history, not evidence of an earlier public-directory release.
