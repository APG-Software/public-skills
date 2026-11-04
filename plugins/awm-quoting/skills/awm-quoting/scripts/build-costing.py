"""Cost a fit-out case: catalogue furniture plus joinery from a parts list.

    python3 build-costing.py work/case.json work/costing.json

Every price comes from data/. Anything unknown stops the run with a plain message,
so a guessed rate never reaches a quote.
"""
import csv
import json
import math
import pathlib
import re
import sys

SKILL = pathlib.Path(__file__).resolve().parent.parent
DATA = SKILL / "data"


def table(name, key):
    with open(DATA / name, newline="", encoding="utf-8") as f:
        return {r[key]: r for r in csv.DictReader(f)}


def fail(msg):
    sys.exit(f"STOP: {msg}")


def edges_lm(edges, length, width):
    """'2L2W' -> metres of edging on one part."""
    edges = (edges or "").strip().upper()
    if not edges:
        return 0.0
    m = re.fullmatch(r"(?:(\d)L)?(?:(\d)W)?", edges)
    if not m:
        fail(f"edges '{edges}' not understood (use e.g. 2L2W, 1L, 1L2W)")
    return (int(m.group(1) or 0) * length + int(m.group(2) or 0) * width) / 1000.0


def norm(row):
    return {k.strip().lower(): ("" if v is None else str(v)).strip() for k, v in row.items() if k}


def read_rows(src, case_dir):
    p = pathlib.Path(src)
    if not p.is_absolute():
        p = (SKILL / src) if (SKILL / src).exists() else (case_dir / src)
    if not p.exists():
        fail(f"parts list {src} not found")
    if p.suffix.lower() in (".xlsx", ".xlsm"):
        try:
            import openpyxl
        except ImportError:
            fail("reading .xlsx needs openpyxl; save the export as CSV instead")
        ws = openpyxl.load_workbook(p, read_only=True, data_only=True).active
        it = ws.iter_rows(values_only=True)
        head = [str(h or "") for h in next(it)]
        return [norm(dict(zip(head, r))) for r in it]
    with open(p, newline="", encoding="utf-8-sig") as f:
        return [norm(r) for r in csv.DictReader(f)]


def load_units(case, case_dir):
    """Joinery units from case['joinery'] plus any parts_list CSV/XLSX."""
    units = {}
    for u in case.get("joinery", []):
        units[u["unit"]] = {"unit": u["unit"], "type": u["unit_type"],
                            "qty": int(u.get("unit_qty", 1)),
                            "parts": [norm(p) for p in u.get("parts", [])]}
    if case.get("parts_list"):
        for r in read_rows(case["parts_list"], case_dir):
            if not r.get("unit"):
                continue
            u = units.setdefault(r["unit"], {"unit": r["unit"], "type": r.get("unit_type", ""),
                                             "qty": int(float(r.get("unit_qty") or 1)), "parts": []})
            u["parts"].append(r)
    return list(units.values())


def main(case_path, out_path):
    case_path = pathlib.Path(case_path)
    case = json.loads(case_path.read_text(encoding="utf-8"))
    if not case.get("demo_notice"):
        fail("demo_notice missing from the case")
    rates = {k: float(v["value"]) for k, v in table("rates.csv", "key").items()}
    catalogue = table("catalogue.csv", "code")
    boards = table("boards.csv", "code")
    hardware = table("hardware.csv", "code")
    types = table("unit-types.csv", "type")
    margin = float(case.get("margin") or 0)
    if not 0 < margin < 0.9:
        fail("margin must be between 0 and 0.9, e.g. 0.32 for 32%")
    project = case.get("project", {})
    after_hours = bool(project.get("after_hours"))
    install_rate = rates["install_per_hour"] * (rates["after_hours_loading"] if after_hours else 1)

    # Catalogue furniture
    furniture, install_hours = [], 0.0
    for it in case.get("items", []):
        c = catalogue.get(it["code"])
        if not c:
            fail(f"catalogue code {it['code']} is not in data/catalogue.csv")
        qty = int(it["qty"])
        hrs = qty * float(c["install_hours"])
        install_hours += hrs
        furniture.append({"code": it["code"], "description": c["description"], "qty": qty,
                          "unit_cost": float(c["unit_cost"]),
                          "cost": round(qty * float(c["unit_cost"]), 2),
                          "install_hours": round(hrs, 2), "note": it.get("note", "")})

    # Joinery: first pass measures every part.
    units = load_units(case, case_path.parent)
    board_area, hw_totals = {}, {}
    for u in units:
        if u["type"] not in types:
            fail(f"unit type '{u['type']}' for {u['unit']} is not in data/unit-types.csv")
        u["area_by_board"] = {}
        u["edge_lm"] = u["edge_cost"] = u["cnc_min"] = u["hw_cost"] = 0.0
        u["part_count"] = 0
        for p in u["parts"]:
            mat = p.get("material", "")
            q = float(p.get("qty") or 0) * u["qty"]
            if mat in hardware:
                u["hw_cost"] += q * float(hardware[mat]["unit_cost"])
                hw_totals[mat] = hw_totals.get(mat, 0) + q
                continue
            if mat not in boards:
                fail(f"material '{mat}' on {u['unit']} / {p.get('part')} is not a board or hardware code")
            try:
                L, W = float(p["length_mm"]), float(p["width_mm"])
            except (KeyError, ValueError):
                fail(f"{u['unit']} / {p.get('part')} has no length or width")
            a = L * W / 1e6 * q
            u["area_by_board"][mat] = u["area_by_board"].get(mat, 0) + a
            board_area[mat] = board_area.get(mat, 0) + a
            e = edges_lm(p.get("edges"), L, W) * q
            u["edge_lm"] += e
            u["edge_cost"] += e * (float(boards[mat]["edge_per_lm"]) + rates["edgebander_per_lm"])
            u["cnc_min"] += q * rates["cnc_min_per_part"] + a * rates["cnc_min_per_m2"]
            u["part_count"] += int(q)

    # Board sheets are ordered whole, per material, after nesting yield.
    sheets = []
    for code, a in sorted(board_area.items()):
        b = boards[code]
        sheet_m2 = float(b["sheet_length_mm"]) * float(b["sheet_width_mm"]) / 1e6
        n = math.ceil(a / (sheet_m2 * rates["board_yield"]))
        sheets.append({"code": code, "description": b["description"], "part_m2": round(a, 2),
                       "sheets": n, "sheet_cost": float(b["sheet_cost"]),
                       "cost": round(n * float(b["sheet_cost"]), 2)})
    sheet_cost = {s["code"]: s["cost"] for s in sheets}

    # Second pass: each unit carries its share of the board order, by area.
    joinery = []
    for u in units:
        t = types[u["type"]]
        board = sum(sheet_cost[m] * a / board_area[m] for m, a in u["area_by_board"].items())
        asm_h = u["qty"] * float(t["assembly_hours"])
        inst_h = u["qty"] * float(t["install_hours"])
        install_hours += inst_h
        j = {"unit": u["unit"], "type": t["description"], "qty": u["qty"], "parts": u["part_count"],
             "board_m2": round(sum(u["area_by_board"].values()), 2),
             "edge_lm": round(u["edge_lm"], 1), "cnc_min": round(u["cnc_min"], 1),
             "board_cost": round(board, 2), "edging_cost": round(u["edge_cost"], 2),
             "cnc_cost": round(u["cnc_min"] * rates["cnc_per_min"], 2),
             "hardware_cost": round(u["hw_cost"], 2), "assembly_hours": round(asm_h, 2),
             "assembly_cost": round(asm_h * rates["assembly_per_hour"], 2),
             "install_hours": round(inst_h, 2)}
        j["cost"] = round(j["board_cost"] + j["edging_cost"] + j["cnc_cost"]
                          + j["hardware_cost"] + j["assembly_cost"], 2)
        joinery.append(j)

    deliveries = int(project.get("deliveries") or 1)
    install_cost = round(install_hours * install_rate, 2)
    delivery_cost = round(deliveries * rates["delivery_each"], 2)
    site = {"install_hours": round(install_hours, 1), "install_rate": round(install_rate, 2),
            "after_hours": after_hours, "install_cost": install_cost,
            "deliveries": deliveries, "delivery_cost": delivery_cost,
            "cost": round(install_cost + delivery_cost, 2)}

    furniture_cost = round(sum(f["cost"] for f in furniture), 2)
    joinery_cost = round(sum(j["cost"] for j in joinery), 2)
    total_cost = round(furniture_cost + joinery_cost + site["cost"], 2)

    def sell(c):
        return round(c / (1 - margin), 2)

    # The quote total is the sum of the rounded sell lines, so every document reconciles.
    for f in furniture:
        f["sell"] = sell(f["cost"])
        f["sell_each"] = round(f["sell"] / f["qty"], 2)
    for j in joinery:
        j["sell"] = sell(j["cost"])
    site["sell"] = sell(site["cost"])
    price_ex = round(sum(f["sell"] for f in furniture) + sum(j["sell"] for j in joinery)
                     + site["sell"], 2)
    gst = round(price_ex * rates["gst"], 2)

    out = {
        "margin": margin, "furniture": furniture, "joinery": joinery, "sheets": sheets,
        "hardware": [{"code": k, "description": hardware[k]["description"], "qty": int(v)}
                     for k, v in sorted(hw_totals.items())],
        "site": site,
        "totals": {"furniture_cost": furniture_cost, "joinery_cost": joinery_cost,
                   "site_cost": site["cost"], "total_cost": total_cost,
                   "edge_lm": round(sum(j["edge_lm"] for j in joinery), 1),
                   "cnc_hours": round(sum(j["cnc_min"] for j in joinery) / 60, 1),
                   "price_ex_gst": price_ex, "gst": gst,
                   "price_inc_gst": round(price_ex + gst, 2),
                   "gross_profit": round(price_ex - total_cost, 2)},
        "ladder": [{"margin": m, "price_ex_gst": round(total_cost / (1 - m), 2)}
                   for m in (0.25, 0.30, 0.35, 0.40)],
    }
    out_path = pathlib.Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    t = out["totals"]
    print(f"cost ${t['total_cost']:,.2f}  price ex GST ${t['price_ex_gst']:,.2f}  "
          f"inc GST ${t['price_inc_gst']:,.2f}  ({margin:.0%} margin)")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
