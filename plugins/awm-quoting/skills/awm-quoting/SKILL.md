---
name: awm-quoting
description: Quoting demo for AWM Amaroo, a commercial furniture and joinery manufacturer. Turns a fit-out furniture schedule and a joinery parts list (a CSV or Excel export from the design program) into an internal costing sheet with the board, edging, machining, hardware and labour worked out, then a client quote. Use when someone says "AWM quote", "quote this fit-out", "price this parts list", "quoting demo", "run the example" or drops in a parts list or furniture schedule. Start straight away with the opening message; never ask what they want first. Every rate is invented for the demo.
metadata:
  version: 0.2.0
---

# AWM quoting demo: schedule and parts list to quote

**This is a demonstration for a sales call.** The company details come from AWM Amaroo's public
website. Every rate, price and product line in `data/` is invented, and the demo uses generic
product descriptions, not AWM's range names. Keep the case's `demo_notice`; every document
prints it.

Someone is watching this live. Keep chat replies short and let the documents carry the detail.

`references/quoting-process.md` describes the quoting process this demo assumes. Bring it up if
they ask how the demo thinks their quoting works, and invite corrections.

## 1. Open: send this first, before any tool

If the first message already has a job, a schedule or a parts list in it, skip to step 2.

```markdown
**Quoting demo · AWM Amaroo** _(demo rates, not real prices)_

Give me the job in any of these ways:

1. **A parts list** exported from your design program (CSV or Excel): one row per panel with material, size, quantity and edging, plus hardware.
2. **A furniture schedule**: the workstations, tables, chairs and storage, with quantities.
3. **Both**, which is how most fit-outs arrive.

Then tell me the client, the site, whether installation is after hours, and the margin you want.

Or say **use the example**: a 24-person legal office fit-out with a kitchen, a reception counter and lockers.
```

## 2. Take the job

- **"use the example"** → copy `references/example-case.json` to `work/case.json`. Its
  `parts_list` already points at `references/example-parts-list.csv`. Go to step 3.
- **A parts list** → save it into `work/` and set `parts_list` in the case to its path. Real
  exports name their columns their own way: map them onto the columns in
  `references/quoting-process.md` (write a cleaned CSV into `work/` if needed) and say in one
  line which columns you mapped. Board and hardware codes must match `data/boards.csv` and
  `data/hardware.csv`. Map a real material name onto the nearest demo code, and list each
  mapping as an assumption.
- **A furniture schedule** → map each line onto a `data/catalogue.csv` code in `items`.
- Build the rest of the case like `references/example-case.json`: client, project, `margin`
  (a fraction, e.g. 0.32), `after_hours`, `deliveries`, `exclusions`.

Defaults when not said, each recorded as a sentence in `assumptions`: margin 32%, installation in
normal hours, one delivery per 10 workstation pods (minimum one), the example's exclusions.
Ask only when there is nothing to quote at all.

Never invent a cost or a rate. Prices come only from `data/`; if a code is missing, the script
stops and says which. Tell the presenter, and either map to an existing code or leave the line
out and say so.

## 3. Cost it and show the costing sheet

Set `SKILL_DIR` to the folder holding this SKILL.md. Write `work/` and `output/` in the working
folder, never inside the skill.

```bash
SKILL_DIR="<absolute path of the folder containing this SKILL.md>"
python3 "$SKILL_DIR/scripts/build-costing.py" work/case.json work/costing.json
python3 "$SKILL_DIR/scripts/render.py" costing work/case.json work/costing.json output/costing-sheet.html --pdf
```

Share `output/costing-sheet.pdf` and reply in a few lines:

- total cost, price ex GST and inc GST at the margin, and gross profit;
- a small table of the **board order** (board, m² of parts, sheets) and the edging metres and
  CNC hours. This is the moment that shows the parts list was really read;
- the "Assumed:" line, if anything was defaulted;
- then ask: **"Anything to change? Otherwise say go and I'll build the client quote."** Show
  the margin ladder in the same line if no margin was given.

Take corrections (a quantity, a margin, after-hours on or off, another delivery), edit the case,
re-run and show it again.

## 4. "Go": the client quote

"Go" is the estimator's approval. Apply anything said with it, set `approval.reviewer` (the
estimator's name, or "Estimator" if none was given) and `approval.approved_at` to today, then
always re-cost before rendering:

```bash
python3 "$SKILL_DIR/scripts/build-costing.py" work/case.json work/costing.json
python3 "$SKILL_DIR/scripts/render-quote.py" work/case.json work/costing.json output/quote.html --pdf
```

This makes two things:

- `output/quote.pdf`: the client quote. A photo cover, the scope with a price per line and the
  investment panel, what is and is not included with next steps and acceptance, then terms.
- `output/job-record.csv`: the row that goes into their project or job system. It holds the quote
  number, client, value, workstation positions, board sheets, CNC and install hours, plus empty
  columns for order, production, delivery, install, invoiced and paid.

Share both. Reply with the total inc GST, and the job record as a two-column table of the fields
that have values. Close with one line on what a real setup would do next: the row is pushed into
their job system, and the same parts list goes on to production when the quote is accepted.

## Rules that hold in a demo

1. **Prices only from `data/`.** Never guess a rate, a margin or a product.
2. **The client never sees costs.** The quote shows items and sell prices only; costs, rates,
   machine time and margin stay on the costing sheet.
3. **Costing sheet first.** No client quote until the presenter has seen the costing and said go.
4. **It says it is a demo.** `demo_notice` stays on the case.
5. **The totals reconcile.** The quote total is the sum of its lines and equals the costing
   sheet's price. GST is 10%.

If no PDF renderer is found, share the HTML and say the PDF was not made.

## Files

| Path | Holds |
| --- | --- |
| `data/catalogue.csv` | Catalogue furniture: demo unit costs and install hours |
| `data/boards.csv` | Board sheets: sizes, demo sheet prices, edging per metre |
| `data/hardware.csv` | Hinges, runners, handles, locks: demo prices |
| `data/unit-types.csv` | Assembly and install hours per joinery unit type |
| `data/rates.csv` | Nesting yield, CNC, edgebander, labour, after-hours loading, delivery, GST |
| `data/company.json` | Public company details used on the documents |
| `data/terms.json` | Example terms, demo only |
| `references/example-case.json` | The example job, and the case format by example |
| `references/example-parts-list.csv` | The example joinery parts list |
| `references/quoting-process.md` | The assumed quoting process and the parts list columns |
| `assets/cover-photo.jpg` | The quote cover photo (AI-generated for this demo) |

Swap `data/` for the business's real price file and rates, and the same skill quotes for real.
