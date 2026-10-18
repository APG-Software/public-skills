# The living page: drawing the business as you go

The room must **see** their business drawn out and confirm it, part by part. People spot a
missing step on a drawing that they'd nod through in a list. Everything goes onto **one page**
that grows through the hour, titled **"How [Business] works"**.

Two worked examples for the made-up _Ridgeline Steel_ sit beside this file:
`example-working-page.html` (mid-session, with waiting points) and `example-keep-page.html` (the
clean page they keep). Copy their structure and class names. Never copy their content.

## 1. What the page holds, top to bottom

1. **Title** "How [Business] works", and one line under it: "Check each part. Tell me what's
   missing or needs changing."
2. **Progress bar** (`wp-progress`): five segments, Open · What you make · Teams and sites ·
   How a job moves · Where work waits. Done segments filled, the current one outlined.
3. **What you make**: the range as short chips, grouped by flow.
4. **A value-chain strip for each flow** (`wp-strip`): the stages left to right as chevrons,
   in their words, with the flow's name on the left ("Made to order from drawings").
5. **Teams and sites** (`wp-teams`): one box per team (`wp-team`) with the leading role under the
   name, and a row of sites, each with what happens there. **No names, no counts, no reporting
   lines.** Offshore appears only as a place.
6. **A swimlane for each flow** (`wp-lane`), drawn in inline SVG:
   - one lane per team, plus a "Systems" note on each step: the step (`wp-step`) on line one, the
     system on line two ("Log the job / CRM and job system");
   - numbered steps; side branches get a letter (3a);
   - decisions as diamonds, **both branches labelled**;
   - **hand-offs** between lanes (`wp-handoff`) as arrows;
   - **waiting points** (`wp-wait`): an **amber** dot with a short label, only ever on a
     hand-off arrow, **never on a team box or a person**;
   - **View A / View B** (`wp-fork`): a dashed fork wherever the room disagreed, both views
     labelled, and the same item on the parking list;
   - about 12 steps at most per flow. More than that, group small steps.
7. **Parking list**: numbered, short, with who could answer each.
8. **A legend**: box = step, diamond = decision, arrow between lanes = hand-off, amber dot =
   where work waits, dashed = View A / View B.

Build up only what's been covered: after Part 1 the page has the title, progress bar, range and
strips; Part 2 adds teams and sites; Part 3 adds the swimlanes; Part 4 adds the waiting points.

## 2. How it must look

- **Self-contained HTML with inline SVG.** No external scripts, fonts, stylesheets or images.
- **For a projector:** body text at least 20px, step text at least 16px in the SVG, strong
  contrast, generous spacing. Someone at the back of the room must be able to read it.
- **Light and dark:** colours as CSS variables on `:root`, a dark set under
  `@media (prefers-color-scheme: dark)`, and an explicit `body` background.
- **Calm colours.** One accent colour for structure. **Amber** only for waiting points. Never red:
  nothing on the page is an error or a fault.
- **No sideways scroll on the page.** Wide swimlanes sit in a box that scrolls sideways on its
  own. On a narrow screen, also show each flow's steps as stacked cards (team, step, system,
  hand-off).

## 3. Updating it

- **Update the same artifact** after each part, so the room always sees one page. Say what
  changed in one line: "Added the Dispatch team and the Brisbane yard."
- **Batch corrections** within a part: collect the fixes from one confirmation round, then redraw
  once, not after every sentence.
- Confirm **step by step**, never "looks good?": "Steps 1 to 3: is that right? Anything missing
  between 3 and 4?" At each diamond: "Is 'builder signs off' really what decides it?" At each
  waiting point: "Is that the right hand-off?"

## 4. If the page won't update or show

In this order:

1. **One new artifact per part.** If updating the same artifact fails or loses content, make a
   fresh page at the end of each part holding everything so far.
2. **A numbered list grouped by team**, every decision and hand-off spelled out, then the Mermaid
   source in a block, with the line: "To see it drawn, paste this into mermaid.live." Confirm the
   same way.

### Mermaid rules (for the fallback and for the file)

- `flowchart LR`, one `subgraph` per team, steps `S1`, `S3a` and so on, labels in double quotes,
  `<br>` before the system name.
- Diamonds `{"..."}` for decisions; every branch labelled with `-->|"..."|`.
- `classDef wait stroke:#d48806,stroke-width:3px` on steps either side of a waiting point;
  `classDef fork stroke-dasharray:6 4` for View A / View B.
- Keep it in step with the page. The final version of each flow goes in the file.

## 5. The page they keep

At the very end, make a **new** artifact, titled "How [Business] works", that holds the range, the
flows and their strips, the teams and sites, and the swimlanes with systems. Then **remove**:

- every waiting point and its label;
- every View A / View B fork (use the view the room settled on; if none, leave the step plain and
  say so in the file);
- the parking list;
- any name, count or email that slipped in.

Under the title: "As checked by the leadership team on [date]." This page is theirs to share.
