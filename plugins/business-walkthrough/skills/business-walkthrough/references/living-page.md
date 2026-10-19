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
2. **Progress bar** (`wp-progress`): seven segments, Open · What you sell · Journey ·
   Organisation · How work moves · Systems · Stuck and ideas. Done segments filled, the current
   one outlined.
3. **What you sell** (`wp-lines`): one group per **service line** ("Made to order from
   drawings"), the products as cards inside it, and who buys and how they reach you underneath.
4. **The customer's journey** (`wp-strip`): one journey strip per service line (the audit's value-chain strip), the stages left to
   right as chevrons in their words, and a **behind the scenes** row under them for the
   supporting work (buying, hiring, systems, finance).
5. **Organisation** (`wp-teams`): an org chart by department, one box per department
   (`wp-team`) with the leading role under the name, and the **sites** as pins with what
   happens at each. **No names, no counts, no reporting lines.** Offshore appears only as a
   place. After Part 4, each department box also carries a short **every week** list.
6. **How the work moves** (`wp-lane`): a swimlane per service line, under its journey strip,
   drawn in inline SVG:
   - one lane per department, the journey's stages as columns;
   - numbered steps (`wp-step`): the step on line one, the system on line two ("Log the job /
     CRM and job system"); side branches get a letter (3a);
   - decisions as diamonds, **both branches labelled**;
   - **hand-offs** between lanes (`wp-handoff`) as arrows;
   - about 12 steps at most per line. More than that, group small steps.
7. **Systems**: a row under the journey, each system spanning the stages it's used in, with a
   two-way arrow wherever the same thing is typed into two systems.
8. **Stuck and ideas** (Part 6):
   - **waiting points** (`wp-wait`): an **amber** lettered dot, only ever on a hand-off arrow,
     **never on a team box or a person**, explained in a list under the drawing;
   - a **repeat badge** (`wp-repeat`): a small circular-arrows mark on a step the room says is
     done the same way over and over;
   - **idea notes** (`wp-idea`): a short note pinned to the **stage** it's about, in the room's
     own words ("Idea · Won stage: one place for the latest drawings"), plus one note for what
     they'd spend more time on;
   - **View A / View B** (`wp-fork`): a dashed fork wherever the room disagreed, both views
     labelled, and the same item on the parking list.
9. **Parking list**: numbered, short, with who could answer each.
10. **A legend**: box = step, diamond = decision, arrow between lanes = hand-off, amber dot =
    where work waits, circular arrows = repeated, note = idea, dashed = not yet confirmed or
    View A / View B.

**Starting from the bundle.** If the context bundle has a `draft-page.json`, draw it first, in
Part 0, with every item **dashed** until the room confirms it. As each part is confirmed, its
items turn solid. Anything the room removes disappears; anything they add is drawn solid.

Build up only what's been covered: each part adds its own section, and the progress bar moves on.

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

At the very end, make a **new** artifact, titled "How [Business] works", that holds what they
sell, the journeys, the organisation and sites, the swimlanes with systems, and the every-week
lists. Then **remove**:

- every waiting point and its label;
- every idea note and repeat badge (those go to Adam in the file);
- every View A / View B fork (use the view the room settled on; if none, leave the step plain and
  say so in the file);
- the parking list;
- any name, count or email that slipped in.

Under the title: "As checked by the leadership team on [date]." This page is theirs to share.
