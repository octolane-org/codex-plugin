# Official brand assets — 23 October 2026

Source: [Octolane brand guidelines](https://www.octolane.com/brand).
The five public ZIP downloads (combined, wordmark, logo, mark, icon) and the
page-linked wallpaper image, preview and eight swatches are saved in the task's
sibling `brand-reference/downloads/` directory. `manifest.json` records source
URLs, sizes and SHA-256 hashes. The combined ZIP's 24 official files are safely
extracted into `brand-reference/extracted/all/`. Additional wallpaper selector
combinations are not claimed as downloaded; the published combined asset pack
contains the core identity assets, not wallpapers.

Use the brand as one word with a capital O. The guidelines prefer monochrome,
full logos where space permits, and the icon for chips/avatars. Both manifest
image slots are square plugin identity slots, so both use the official dark icon
PNG, unmodified, rather than squeezing a wide wordmark into a square. No custom
redrawing, recoloring or new theme variant was introduced. The official SVG's
black fill justifies replacing the old #111827 manifest brand color with #000000.

Source asset: `octolane-icon-dark@4x.png`, 528×528, 18,584 bytes.
SHA-256: `670720f96acbd1301dfdf6fdea2c46590e80a1b2729b3b904ec88174a8f03df3`.
The same original bytes are copied to icon.png and logo.png in the local and
public packages. The public ZIP still contains only four required files.
Reference ZIPs, SVG/JPG alternatives, wallpapers and browser files are excluded.

[Size/contrast screenshot](screenshots/asset-sizes-light-dark.png) shows the
actual asset rendered by Chrome at 16/24/48/96px on light and dark surfaces.
The mark is visible at each size, with the smallest view naturally losing some
edge detail. This is explicitly a local rendering, **not an installed-host
screenshot**. Native Plugins list, details and composer appearances must be
captured during the approved local installation described in
[local testing](local-testing.md). No account/plugin settings were changed here.
