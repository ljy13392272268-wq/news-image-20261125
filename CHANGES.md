# news-image-20261125 - v3 changes

26 November 2026. Owner review pass on the entry; nothing was submitted.

## Where this pass concentrated

The weakest point against the criteria was the smallest text at about 300 px
across - criterion 5 (craft: legible at about 300 pixels, no smears or garbled
text), which also drags down criterion 3 (a viewer who missed the day can tell
what happened from the image alone).

At 1024 px the v2 image was clean. At 300 px the scale factor is 0.293, so:

- the 23 px detail lines became about 6.7 px and collapsed into grey bars;
- the 20 px region labels became about 5.9 px;
- the 21 px one-line footer became about 6.2 px;
- five headlines ran at 36 px (about 10.5 px), but the lead card had dropped to
  31 px (about 9.1 px) because "Two tankers hit mines, ablaze in Hormuz" needed
  three lines at 36 - so the most important story was the smallest headline on
  the page. The 40 px date (about 11.7 px) survived.

So the pass is a type-scale and small-text pass. The composition, the six
stories and the date are unchanged.

## What changed

1. Type scale, all six cards uniform (criterion 5, criterion 3).
   - Headlines: 40 px bold on every card (v2: 36 px on five cards, 31 px on the
     lead). Liberation Sans Bold is narrower than DejaVu, so all six headlines
     fit two lines at 40 px in a 469 px card, including the lead.
   - Details: 28 px (v2 23 px), two lines.
   - Region labels: 25 px (v2 20 px).
   - Date: 42 px (v2 40 px).
   - Masthead: 64 px serif nameplate instead of sans; the serif is used only
     here, because serif body text has a smaller x-height and would hurt the
     300 px view.
   - The 20 px subtitle "THE DAY'S WORLD NEWS, IN ONE IMAGE" was removed: at
     300 px it was unreadable, and the 30 px it took went to the cards. The
     date line still names the day unmistakably.
   - Grid stays 2 columns x 3 rows; cards are 469 x 236 with a 14 px gutter
     and a 20 px gap above the footer.

2. Footer (criterion 3, criterion 5, and breadth under criterion 2).
   - v2 put both extra stories on one 21 px line (about 6 px at 300).
   - v3 gives each its own line at 27 px: "AFRICA - RSF drone strikes kill 19
     civilians, wound 20 in two cities" and "CLIMATE - COP31 ends without a
     deal; Pope Leo XIV voices concern". Both read at 300 px, and both keep
     their region/field label for breadth.

3. Wording (criterion 3 and 4: nothing false, no speculation as fact).
   - Markets: v2's "Asia stocks plunge as chip shares sink" asserted a cause
     the verified items do not carry (the handover lists index moves only).
     Now: "Asia stocks plunge; KOSPI falls 6.2%", detail "Nikkei -2.8%,
     Taiwan -5%; Dow holds above 50,000." "Holds" is kept deliberately: the
     first close above 50,000 was 24 November, not the 25th.
   - Huawei: the detail now records the partial verdict: "Guilty on 10 of 12
     counts; not guilty of racketeering." v2 listed charge types but dropped
     the acquittal.
   - Space: headline stays "Pakistani astronaut reaches Tiangong"; detail
     "Shenzhou-24 docked 3.5 hours after launch; first Pakistani aboard."
     "Pakistan's first astronaut reaches Tiangong" needs 36 px to fit two
     lines, which would break the uniform 40 px, so "first" moved to the
     detail.
   - Ukraine: "torch" became "set two refineries ablaze" - same fact, plainer
     verb.

## What did not change

- The six stories, their order, their facts and the date "WEDNESDAY, 25
  NOVEMBER 2026". No story was swapped; no unverified replacement was used.
- `main.py`: unchanged, standard library only, decodes `entry.png.b64` to the
  exact PNG bytes. The base64 file was regenerated as one line from the new
  entry.png.
- README, LICENSE and .makefun/owner.json are untouched (and are not in this
  archive of changed files).
- No network, no links in the image or the code, no submission, no transcripts,
  no keys or secrets.

## Ideas tried and set aside

- A full-width lead card for Hormuz. It would leave five stories to tile into
  two columns, which means either a hole in the grid or one story pushed into
  the tiny footer; the equal 2 x 3 front page is cleaner.
- Eight cards in a 2 x 4 grid (moving Sudan and COP31 into the grid). Card
  height would fall to about 170 px and the type would drop below 30 px, which
  makes the 300 px view worse, not better.
- A 48 px date. It would still fit the width, but it starts to compete with the
  64 px masthead; 42 px already reads at 300 px (about 12.3 px) and keeps the
  hierarchy.
- Serif body text for a stronger newspaper feel. Rejected: the serif's smaller
  x-height costs more at 300 px than the style gains.
- 64 px icons. Measured against the 40 px headline: the first headline line
  would run under the icon on cards 1 and 2. Kept 54 px; it sits in the label
  row and ends at y+64, above the headline at y+66, so a long first line cannot
  collide with it.
- First v3 draft used "Pakistan's first astronaut; Shenzhou-24 docked 3.5 hours
  after launch." It wrapped to three lines, so the fitter dropped that one card
  to 24 px - the only card with small text. Reworded to the current line, which
  fits two lines at 28 px. Recorded rather than forced.

## Verification

- Reference files: all five sizes and sha256 match the handover; decoded
  entry.png is 124,395 bytes, 1024x1024.
- `main.py` run twice in separate output directories: identical bytes,
  150,266 bytes, mode 644, sha256 70c2fde6...f3bd7fe6, identical to the
  repository entry.png.
- `generate_image.py` run twice: identical sha256, 150,266 bytes each.
- PNG: IHDR 1024x1024, 8-bit RGB, three IDAT chunks, IEND, every chunk CRC32
  OK, PIL verify and reopen OK. 150,266 bytes is well under 1,048,576.
- Visual check at 1024 px and at 300 px; see `verification/verify.txt`,
  `verification/preview_300.png` and `verification/compare_v2_v3_300.png`.
  At 300 px the masthead, date, all six headlines and both footer lines read
  without zoom; the 28 px details are small but resolve as words; the 25 px
  labels are the smallest text.

If a different balance is preferred - for example a slightly smaller footer
band in exchange for more air above it - that is a small change in `render()`,
where the grid constants are grouped and the footer offsets sit beside them.

## Muse verification note (2026-11-26)

- main.py is byte-identical to v2; entry.png.b64 decodes to entry.png byte
  for byte (sha256 70c2fde6df2ed439dcea0639c472621978a1de82b2a51401f568f287f3bd7fe6).
- All six headlines fit at 40 px / 2 lines and all six details at 28 px /
  2 lines on this machine (Liberation fonts present); footer at 27 px.
- A local re-render of generate_image.py on this machine produces the same
  layout but 155,366 bytes (vs 150,266 here): the pixels differ only by
  font antialiasing between machines. The shipped image is Doubao's
  verified bytes; main.py serves those bytes deterministically.
