/* Real waveform peaks, keyed by episode slug.
 *
 * Written by tools/generate_waveforms.py, which decodes the actual audio with
 * ffmpeg and stores a few hundred peak values per episode, a couple of KB each.
 * The player draws the shape only when an entry exists here, because a
 * plausible looking squiggle that is not the audio would be invented data.
 *
 * Empty until the script is run on a machine that can reach the audio host. The
 * player works fully without it; the bar is a plain track instead of a shape. */
window.ATLAS_WAVEFORMS = {};
