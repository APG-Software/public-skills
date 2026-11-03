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
5. **Organisation** (`wp-org`): an **org chart** drawn exactly as the org chart block in
   `references/page-template.html`. The business's top role sits at the top, with a line down to
   one box per department (`wp-team`). Each box holds the department's name, its leading role,
   and the other roles in it, stacked under it (`roles`). The **sites** sit under the chart as
   pins, with what happens at each. **Roles only: no names, no counts, and each role once**, so
   three estimators are one "Estimator". Offshore appears only as a place. Anything not yet
   confirmed is dashed. After Part 4, each department box also carries a short **every week**
   list. Use this same org chart on the live page in the room, so the leadership team can look
   at it and correct it.
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
- **Always light:** colours as CSS variables on `:root` with `color-scheme:light`, and an
  explicit `body` background. No dark set: a meeting-room laptop in dark mode must still show the
  light page, which reads best on a projector.
- **Calm colours.** One accent colour for structure. **Amber** only for waiting points. Never red:
  nothing on the page is an error or a fault.
- **Lightly branded APG Software.** Copy the `:root` colours, the `.brand` header (the APG mark,
  "APG Software", "Business walkthrough") and the `.foot` line ("Prepared with APG Software ·
  apgsoftware.com") from the examples exactly. Paper `#f7f7f3` background, ink `#0d0d0c`
  headings, green `#3f7a0e` for step boxes and hand-offs, lime `#90f23c` only as a fill (the
  current progress segment, the header's top edge), never as text on a light background. No
  gradients, no shadows, no navy. Fonts: `"Space Grotesk"` for headings and `"DM Sans"` for
  everything else, each with the system fallback, never loaded from outside. The business's own
  name stays the title; APG's branding stays in the header and footer.
- **No sideways scroll on the page.** Wide swimlanes sit in a box that scrolls sideways on its
  own. On a narrow screen, also show each flow's steps as stacked cards (team, step, system,
  hand-off).

## 3. Updating it

- **Update the same artifact** after each part, so the room always sees one page. Say what
  changed in one line: "Added the Dispatch team and the Brisbane yard."
- **Batch corrections** within a part: collect the fixes from one confirmation round, then redraw
  once, not after every sentence.
- After each redraw, **ask about the gaps, never "looks good?"**. Point at what's dashed or
  thin and ask openly: "Here's steps 1 to 3. What happens between 2 and 3 that I haven't got?"
  At each diamond: "Tell me what really decides which way this goes." At each waiting point:
  "What's the job waiting for here, and what happens in the meantime?" The page holds what you
  know; the chat asks about what you don't.

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

## 6. Drawn from a file

When someone brings a walkthrough file, **show the page before you say anything else**.

**Use `references/page-template.html` and copy it exactly**, so everyone who opens the file
sees the same page: the same styles, class names, section order and layout. Change only the
words. Repeat or drop the blocks its comments mark "one per": a service line, a journey, a
swimlane, a team, a site, a system. The swimlane in the template is a grid, not SVG:
- each lane sits at `grid-row`, and each step at its lane's `grid-row` and at
  `grid-column` = its order + 1, with `--cols` = the number of steps;
- the same steps go in the `wp-cards` list for phones;
- a waiting point is a `wp-wait` inside the `wp-handoff` line of the step it leaves.

Fill it from the file: every part in section 1, including the swimlanes (from the table under
"How a typical job moves", with the Mermaid block as the fallback), the waiting points, the
ideas and the parking list. If the file has an "About the business" section, keep that block;
otherwise drop it.

- Lines marked `confirmed in the room`, `added by …`, `from their documents` or
  `from the website` are **solid**. Lines marked `UNCONFIRMED` or `assumed` are **dashed**.
  An `Also said:` line sits beside the line it differs from, as a View A / View B fork.
- The progress bar becomes a **coverage bar**: the same seven segments, each filled (nothing
  open), half-filled (has gaps) or empty (nothing yet). It no longer shows where you are in
  the hour.
- A **Still open** panel (`wp-open`) sits under the parking list: the gaps grouped by part,
  the person's own parts first, at most eight shown, and one line saying how many more.
- Draw what the file says and nothing more. If a part of the file won't make sense, leave it
  off and list it as a gap: never fill it in by guessing.
- After each answer, update the same page, still from the template.
- The page they keep at the end of a carry-on is also made from the template, with section 5's
  rules applied. Take out the waiting points, ideas and repeat marks, the parking list, the
  Still open panel and the coverage bar.
- If the page won't show, use the fallbacks in section 4, in order.
