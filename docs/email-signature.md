# Email signature images (owner, 30 Oct 2026)

The owner's email signature loads two images straight from the site:

- https://paraglidingatlas.com/assets/email/portrait.png (336 x 336, shown at 112 x 112)
- https://paraglidingatlas.com/assets/email/atlas-mark-dark.png (336 x 65, shown at 112 x 22)

**Never delete, rename or move `assets/email/`, and keep it in any host move.** Every email already sent points
at these two addresses for good; if they stop answering, the images break in old emails too. To change an image,
replace the file under the same name.

They sit in the root `assets/` folder (not under `prototypes/v4/`) on purpose, so no site version or rebuild
moves them. `tools/v2_switch.py --apply` copies the root `assets/` folder into the published site as it is.
The live-untouched gate in `tools/v4_gates.py` flags any change there: for these two files that is expected
(owner, 30 Oct 2026).

Made from the owner's originals: the portrait cut-out in a circle over the orange gradient of the first
version, and the logo's arc and letters (no tagline) in black on a transparent ground.
