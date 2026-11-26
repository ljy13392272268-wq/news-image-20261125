# news-image-20261125 - v3 changes

26 November 2026. Owner review pass on the entry; nothing was submitted.
This file now covers two passes: round 1 (v3) below, round 2 (v4) at the end.

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

---

# Round 2 - v4 changes

26 November 2026. Second owner review pass on the same entry; nothing was
submitted. Round 1 (v3) above is unchanged.

## Where this pass concentrated

The 300 px view was still limited by the smallest text, and the footer band
sat bottom-heavy. The pass takes the three type levers noted at the end of
round 1 - detail size, label size, footer band - and keeps only the ones that
read better.

## What changed

1. Details 28 -> 30 px on all six cards (criterion 5, criterion 3).
   - At 300 px a 30 px line is about 8.8 px, against 8.2 px for 28.
   - Every card still fits two lines. The space detail keeps its full
     verified wording and breaks after "docked in", so "3.5 hours" is not
     split: "Shenzhou-24 docked in / 3.5 hours; first Pakistani aboard."
     This is the only copy change in the pass; the facts are unchanged.
   - Leading 32 -> 34 px, so the 30 px lines do not touch. The block still
     starts at y+160 and its last ink row is y+228, 8 px above the card edge.
2. Region labels 25 -> 27 px (criterion 5).
   - The chip stays 36 px tall; the widest label, SCIENCE & SPACE, is 274 px
     wide and still ends 105 px left of the icon at x+397. No collision, no
     clipped chip text.
3. Footer band 76 -> 72 px and moved down 948 -> 952 (criterion 5).
   - The gap above the band grows 20 -> 24 px; the two 27 px lines sit at
     954 and 986 with 32 px leading. Ink runs 959..1016, so the band now has
     7 px of navy above and 8 px below, instead of 13 above and 5 below.
   - The type stays 27 px; no shrink is needed (line widths 872 and 900 px
     against the 968 px limit).

## What did not change

- The six stories, their order, the verified facts and the date
  "WEDNESDAY, 25 NOVEMBER 2026". No story swapped, no claim added.
- Headlines stay 40 px bold on two lines, the date 42 px, the masthead 64 px
  serif, the icons 54 px, the 2 x 3 grid and 236 px cards.
- `main.py` unchanged; `entry.png.b64` regenerated as one line from the new
  `entry.png`.
- README, LICENSE and .makefun/owner.json untouched; no submission, no
  transcripts, no keys or secrets, no links in the image or the code.

## Ideas tried and set aside

- 30 px details on the old space wording. It needs 464 px for the second
  line against 433, so the fitter would drop that one card to 28 or split
  "3.5 / hours". The manual break after "docked in" keeps both 30 px and the
  whole phrase; the short first line is the price and it reads cleanly.
- "a Pakistani first", "Pakistani aboard" or "docked 3.5 hours after
  launch" at 30 px. Each fits without a manual break but gives up "first
  Pakistani aboard", "aboard" or "Shenzhou-24" respectively; not worth the
  smaller rag. Set aside.
- 64 px icons. Round 1 measured a collision with the first headline line on
  cards 1 and 2 at 40 px; nothing in this pass changes the label row, so it
  was not retried.
- A 70 px footer band. It would leave 6 px of navy inside; 72 px is the
  balance between a smaller band and air around the type.
- A darker detail grey (58, 70, 83). It is crisper at 300 px, but at 1024 px
  it reads heavier than the v3 grey and starts to compete with the headlines;
  kept (74, 85, 96).
- Detail 30 px with the automatic wrap. It breaks between "3.5" and "hours"
  on the space card; rejected for the manual break.

## Verification

- Reference files (v3, downloaded from the reference branch): all five sizes
  and sha256 match the handover; decoded `entry.png` is 150,266 bytes,
  1024x1024, sha256 70c2fde6...f3bd7fe6.
- `main.py` run twice in separate output directories: identical bytes,
  154,580 bytes, mode 644, sha256 efdcbce9...c83c91f6d, identical to the new
  `entry.png`.
- `generate_image.py` run twice: identical sha256, 154,580 bytes each.
- PNG: IHDR 1024x1024, 8-bit RGB, IDAT 65536 + 65536 + 23427, IEND; every
  chunk CRC32 OK; PIL verify and reopen OK. 154,580 bytes is well under
  1,048,576.
- Type check from the rendered image: all six headlines 40 px on two lines,
  all six details 30 px on two lines, labels 27 px, footer 27 px; no text
  outside a card, no chip/icon or headline/icon collision.
- Visual check at 1024 px and at 300 px; see `verification/verify.txt`,
  `verification/preview_300.png`, `verification/compare_v3_v4_300.png` and
  `verification/compare_details_300.png`. At 300 px the masthead, date and
  all six headlines read without zoom; the details now resolve as words
  (about 8.8 px); the 27 px labels read with their colour and icon.

## Muse verification note, round 1 (2026-11-26)

- main.py is byte-identical to v2; entry.png.b64 decodes to entry.png byte
  for byte (sha256 70c2fde6df2ed439dcea0639c472621978a1de82b2a51401f568f287f3bd7fe6).
- All six headlines fit at 40 px / 2 lines and all six details at 28 px /
  2 lines on this machine (Liberation fonts present); footer at 27 px.
- A local re-render of generate_image.py on this machine produces the same
  layout but 155,366 bytes (vs 150,266 here): the pixels differ only by
  font antialiasing between machines. The shipped image is Doubao's
  verified bytes; main.py serves those bytes deterministically.

## Muse verification note, round 2 (2026-11-27)

- main.py is byte-identical to v3; entry.png.b64 decodes to entry.png byte
  for byte (sha256 efdcbce94f9a467a5c384310976820570bf9497edcf78458143027cd83c91f6d).
- All six headlines fit at 40 px / 2 lines and all six details at 30 px /
  2 lines on this machine (Liberation fonts present); tags at 27 px, footer
  at 27 px; the space detail breaks after "docked in" as written.
- A local re-render of generate_image.py on this machine produces the same
  layout but 159,133 bytes (vs 154,580 here): the pixels differ only by
  font antialiasing between machines. The shipped image is Doubao's
  verified bytes; main.py serves those bytes deterministically.
