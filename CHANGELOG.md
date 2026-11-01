# Changelog

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
