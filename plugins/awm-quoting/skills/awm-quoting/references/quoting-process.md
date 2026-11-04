# How a fit-out quote probably runs at a commercial furniture and joinery maker

This is an assumed process, built from what any workplace furniture and joinery manufacturer
does. It is here to make the demo feel real. The business confirms or corrects it.

1. **Brief arrives.** A fit-out builder, designer or tenant sends a furniture schedule, floor
   plans and joinery drawings, often as part of a tender.
2. **Catalogue furniture is counted.** Workstations, tables, chairs, storage and accessories
   come off the schedule or the plans.
3. **Joinery is modelled.** Custom items (kitchens, reception counters, lockers, storage) are
   drawn in the design program, which can export a parts list: every panel with its material,
   size, quantity and edging, plus the hardware.
4. **The estimator prices it.** Board sheets from the parts list, edging, machine time,
   hardware, assembly hours, delivery and installation, then the margin.
5. **Quote goes out.** A client quote with items and prices, never the costs.
6. **On approval it becomes a job.** The same parts list feeds production.

Step 4 is the slow part this demo speeds up: the parts list goes straight into a costing sheet.

## Parts list format

One row per part, as a CSV or Excel export. Columns (any order, case does not matter):

| Column | Means |
|---|---|
| `unit` | The built item the part belongs to, e.g. `K1 Kitchen base cabinet 600` |
| `unit_type` | One of the types in `data/unit-types.csv` (sets assembly and install hours) |
| `unit_qty` | How many of that unit are being made |
| `part` | Part name |
| `material` | A board code from `data/boards.csv`, or a hardware code from `data/hardware.csv` |
| `length_mm`, `width_mm` | Finished part size (blank for hardware) |
| `qty` | Quantity **per unit** |
| `edges` | Edges banded, e.g. `2L2W` (both long and both short), `1L` (one long edge), blank for none |

A real export will have its own column names. Map them onto these, and say which you mapped.
