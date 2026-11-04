"""Render the internal costing sheet from a costed case.

    python3 render.py costing work/case.json work/costing.json output/costing-sheet.html [--pdf]

The client quote is render-quote.py.
"""
import datetime
import html
import json
import pathlib
import sys

SKILL = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL / "scripts"))


def money(v):
    return f"${v:,.2f}"


def esc(v):
    return html.escape(str(v))


def page(title, company, case, body):
    c = company
    notice = esc(case["demo_notice"])
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{esc(title)}</title>
<style>
@page {{ size: A4; margin: 16mm 14mm; }}
* {{ box-sizing: border-box; }}
body {{ font-family: -apple-system, "Helvetica Neue", Arial, sans-serif; color: #1d1d1b; font-size: 10pt; margin: 0; }}
header {{ display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 3px solid {c['colour']}; padding-bottom: 8px; }}
.brand {{ font-size: 20pt; font-weight: 700; letter-spacing: .5px; }}
.brand small {{ display: block; font-size: 9pt; font-weight: 400; color: {c['accent']}; letter-spacing: 2px; text-transform: uppercase; }}
.demo {{ background: #fff4d6; border: 1px solid #e5c56b; padding: 6px 10px; margin: 10px 0; font-size: 8.5pt; }}
h1 {{ font-size: 15pt; margin: 14px 0 4px; }}
h2 {{ font-size: 11pt; margin: 18px 0 6px; color: {c['accent']}; text-transform: uppercase; letter-spacing: 1px; }}
table {{ width: 100%; border-collapse: collapse; }}
th, td {{ text-align: left; padding: 5px 6px; border-bottom: 1px solid #e3e3e0; vertical-align: top; }}
th {{ font-size: 8.5pt; text-transform: uppercase; color: #666; font-weight: 600; }}
td.n, th.n {{ text-align: right; white-space: nowrap; }}
.meta {{ display: grid; grid-template-columns: 1fr 1fr; gap: 4px 24px; margin-top: 10px; }}
.meta div span {{ color: #666; display: inline-block; width: 90px; }}
.total td {{ font-weight: 700; border-top: 2px solid #1d1d1b; border-bottom: none; }}
.note {{ color: #666; font-size: 8.5pt; }}
ul {{ margin: 4px 0 0 18px; padding: 0; }}
footer {{ margin-top: 18px; font-size: 8pt; color: #666; border-top: 1px solid #e3e3e0; padding-top: 6px; }}
</style></head><body>
<header><div class="brand">{esc(c['name'])}<small>{esc(c['tagline'])}</small></div>
<div class="note">{esc(c['website'])}<br>{esc(c['locations'])}</div></header>
<div class="demo">{notice}</div>
{body}
<footer>{esc(c['name'])} · {esc(c['website'])} · {notice}</footer>
</body></html>"""


def meta(case):
    q, cl, p = case["quote"], case["client"], case["project"]
    return f"""<div class="meta">
<div><span>Quote</span>{esc(q['number'])}</div><div><span>Date</span>{esc(q['date'])}</div>
<div><span>Client</span>{esc(cl['company'])}</div><div><span>Contact</span>{esc(cl.get('contact',''))}</div>
<div><span>Project</span>{esc(p['name'])}</div><div><span>Site</span>{esc(p['site'])}</div>
<div><span>Builder</span>{esc(p.get('builder',''))}</div><div><span>Start</span>{esc(p.get('start',''))}</div>
</div>"""


def costing(case, k):
    t, s = k["totals"], k["site"]
    rows = "".join(f"<tr><td>{esc(f['code'])}</td><td>{esc(f['description'])}"
                   f"{'<br><span class=note>'+esc(f['note'])+'</span>' if f['note'] else ''}</td>"
                   f"<td class=n>{f['qty']}</td><td class=n>{money(f['unit_cost'])}</td>"
                   f"<td class=n>{money(f['cost'])}</td><td class=n>{f['install_hours']}</td></tr>"
                   for f in k["furniture"])
    jrows = "".join(f"<tr><td>{esc(j['unit'])}</td><td class=n>{j['qty']}</td><td class=n>{j['parts']}</td>"
                    f"<td class=n>{j['board_m2']}</td><td class=n>{money(j['board_cost'])}</td>"
                    f"<td class=n>{j['edge_lm']} m · {money(j['edging_cost'])}</td>"
                    f"<td class=n>{j['cnc_min']} min · {money(j['cnc_cost'])}</td>"
                    f"<td class=n>{money(j['hardware_cost'])}</td>"
                    f"<td class=n>{j['assembly_hours']} h · {money(j['assembly_cost'])}</td>"
                    f"<td class=n>{money(j['cost'])}</td></tr>" for j in k["joinery"])
    srows = "".join(f"<tr><td>{esc(x['code'])}</td><td>{esc(x['description'])}</td><td class=n>{x['part_m2']}</td>"
                    f"<td class=n>{x['sheets']}</td><td class=n>{money(x['sheet_cost'])}</td>"
                    f"<td class=n>{money(x['cost'])}</td></tr>" for x in k["sheets"])
    hrows = "".join(f"<tr><td>{esc(h['code'])}</td><td>{esc(h['description'])}</td><td class=n>{h['qty']}</td></tr>"
                    for h in k["hardware"])
    ladder = "".join(f"<tr><td>{l['margin']:.0%}</td><td class=n>{money(l['price_ex_gst'])}</td></tr>"
                     for l in k["ladder"])
    assumptions = "".join(f"<li>{esc(a)}</li>" for a in case.get("assumptions", [])) or "<li>None</li>"
    body = f"""<h1>Costing sheet <span class="note">(internal, never sent to the client)</span></h1>{meta(case)}
<h2>Catalogue furniture</h2><table><tr><th>Code</th><th>Item</th><th class=n>Qty</th><th class=n>Unit cost</th><th class=n>Cost</th><th class=n>Install h</th></tr>{rows}
<tr class=total><td colspan=4>Furniture cost</td><td class=n>{money(t['furniture_cost'])}</td><td></td></tr></table>
<h2>Joinery, from the parts list</h2><table><tr><th>Unit</th><th class=n>Qty</th><th class=n>Parts</th><th class=n>m²</th><th class=n>Board</th><th class=n>Edging</th><th class=n>CNC</th><th class=n>Hardware</th><th class=n>Assembly</th><th class=n>Cost</th></tr>{jrows}
<tr class=total><td colspan=9>Joinery cost ({t['edge_lm']} m edging, {t['cnc_hours']} CNC hours)</td><td class=n>{money(t['joinery_cost'])}</td></tr></table>
<h2>Board order</h2><table><tr><th>Code</th><th>Board</th><th class=n>Part m²</th><th class=n>Sheets</th><th class=n>Per sheet</th><th class=n>Cost</th></tr>{srows}</table>
<h2>Hardware order</h2><table><tr><th>Code</th><th>Item</th><th class=n>Qty</th></tr>{hrows}</table>
<h2>Delivery and installation</h2><table>
<tr><td>Installation, {s['install_hours']} h at {money(s['install_rate'])}/h{' (after hours)' if s['after_hours'] else ''}</td><td class=n>{money(s['install_cost'])}</td></tr>
<tr><td>Deliveries, {s['deliveries']}</td><td class=n>{money(s['delivery_cost'])}</td></tr></table>
<h2>Price</h2><table>
<tr><td>Total cost</td><td class=n>{money(t['total_cost'])}</td></tr>
<tr><td>Margin</td><td class=n>{k['margin']:.0%}</td></tr>
<tr><td>Price ex GST</td><td class=n>{money(t['price_ex_gst'])}</td></tr>
<tr><td>Gross profit</td><td class=n>{money(t['gross_profit'])}</td></tr>
<tr class=total><td>Price inc GST</td><td class=n>{money(t['price_inc_gst'])}</td></tr></table>
<h2>Margin ladder (ex GST)</h2><table>{ladder}</table>
<h2>Assumed</h2><ul>{assumptions}</ul>"""
    return body



def main():
    args = [a for a in sys.argv[1:] if a != "--pdf"]
    if len(args) != 4 or args[0] != "costing":
        sys.exit(__doc__)
    kind, case_p, cost_p, out_p = args
    case = json.loads(pathlib.Path(case_p).read_text(encoding="utf-8"))
    k = json.loads(pathlib.Path(cost_p).read_text(encoding="utf-8"))
    company = json.loads((SKILL / "data/company.json").read_text(encoding="utf-8"))
    case["quote"]["date"] = case["quote"].get("date") or datetime.date.today().isoformat()
    body = costing(case, k)
    title = "Costing sheet " + case["quote"]["number"]
    out = pathlib.Path(out_p)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page(title, company, case, body), encoding="utf-8")
    print(out)
    if "--pdf" in sys.argv:
        from topdf import html_to_pdf
        ok, msg = html_to_pdf(out, out.with_suffix(".pdf"))
        print(msg if ok else f"PDF not made: {msg}")


if __name__ == "__main__":
    main()
