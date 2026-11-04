"""Render the client quote: cover, scope and investment, next steps and acceptance, terms.

    python3 render-quote.py work/case.json work/costing.json output/quote.html [--pdf]

The client sees items and sell prices. Costs, rates, machine time and margin never appear.
Until the case carries an approval (reviewer and approved_at), every page says DRAFT.
"""
import base64
import datetime
import html
import json
import pathlib
import sys

SKILL = pathlib.Path(__file__).resolve().parent.parent


def esc(v):
    return html.escape(str(v)) if v is not None else ""


def money(v):
    return f"${v:,.2f}"


def long_date(text):
    try:
        d = datetime.date.fromisoformat(text)
    except (TypeError, ValueError):
        return esc(text)
    return f"{d.day} {d.strftime('%B %Y')}"


def main():
    args = [a for a in sys.argv[1:] if a != "--pdf"]
    if len(args) != 3:
        sys.exit(__doc__)
    case = json.loads(pathlib.Path(args[0]).read_text(encoding="utf-8"))
    k = json.loads(pathlib.Path(args[1]).read_text(encoding="utf-8"))
    company = json.loads((SKILL / "data/company.json").read_text(encoding="utf-8"))
    terms = json.loads((SKILL / "data/terms.json").read_text(encoding="utf-8"))

    INK = company["colours"]["ink"]
    ACCENT = company["colours"]["accent"]
    WASH = company["colours"]["wash"]
    q, client, project, t, site = case["quote"], case["client"], case["project"], k["totals"], k["site"]
    qdate = q.get("date") or datetime.date.today().isoformat()
    valid = (datetime.date.fromisoformat(qdate)
             + datetime.timedelta(days=int(q.get("valid_days", company["validity_days"])))).isoformat()
    approval = case.get("approval") or {}
    approved = bool(approval.get("reviewer") and approval.get("approved_at"))
    photo = SKILL / "assets/cover-photo.jpg"
    cover = ("data:image/jpeg;base64," + base64.b64encode(photo.read_bytes()).decode()) if photo.exists() else ""

    positions = sum(f["qty"] * 4 for f in k["furniture"] if f["code"].startswith("WS-") and f["code"].endswith("-4"))
    badge_big = f"{positions}" if positions else f"{len(k['furniture']) + len(k['joinery'])}"
    badge_small = (f"workstation positions, plus {len(k['joinery'])} joinery item{'s' if len(k['joinery']) != 1 else ''}"
                   if positions else "items supplied and installed")

    def row(i, title, sub, qty, total):
        return (f'<div class="line"><div class="line-n">{i:02d}</div><div class="line-b"><h4>{esc(title)}</h4>'
                f'{f"<p>{esc(sub)}</p>" if sub else ""}</div><div class="line-q">{qty}</div>'
                f'<div class="line-m">{money(total)}</div></div>')

    n = 0
    furn = ""
    for f in k["furniture"]:
        n += 1
        furn += row(n, f["description"], f["note"], f"{f['qty']} &times;", f["sell"])
    join = ""
    for j in k["joinery"]:
        n += 1
        title = j["unit"].split(" ", 1)[1] if " " in j["unit"] else j["unit"]
        join += row(n, title, f"{j['type']}, made to the drawings in the confirmed finishes",
                    f"{j['qty']} &times;", j["sell"])
    n += 1
    when = "after hours" if site["after_hours"] else "in normal working hours"
    site_row = row(n, "Delivery and installation",
                   f"{site['deliveries']} deliveries to site, installed and assembled {when}", "", site["sell"])

    def ticks(values, kind):
        icon = "&#10003;" if kind == "in" else "&#10005;"
        return f"<ul class='ticks {kind}'>" + "".join(
            f"<li><i>{icon}</i><span>{esc(v)}</span></li>" for v in values) + "</ul>"

    includes = case.get("includes") or company["standard_includes"]
    excludes = case.get("exclusions") or []
    first = (client.get("contact") or "").split(" ")[0] or "there"
    gate = ("" if approved else '<div class="gate"><b>DRAFT &middot; ESTIMATOR REVIEW REQUIRED</b>'
            '<span>Not approved for issue. No named person has signed off the scope and price.</span></div>')
    notice = f'<div class="demo">{esc(case["demo_notice"])}</div>'
    foot = (f'<div class="pfoot"><span>{esc(company["name"])}</span><span>{esc(company["tagline"])}</span>'
            f'<span>{esc(company["website"])}</span></div>')

    def head(right):
        return (f'<div class="phead"><div class="wm"><b>{esc(company["short_name"])}</b>'
                f'<span>{esc(company["descriptor"])}</span></div>'
                f'<div class="ref"><b>Quote {esc(q["number"])}</b>{right}</div></div>')

    steps = [("Accept", "Sign below or send a purchase order."),
             ("Confirm", "We site-measure and confirm finishes, colours and dates in writing."),
             ("Make", "Joinery is made in our factory; furniture is ordered and checked."),
             ("Install", "Delivered and installed by our team, then a walk-through together.")]
    steps_html = "".join(f'<div class="step"><div class="dot">{i}</div><h4>{esc(a)}</h4><p>{esc(b)}</p></div>'
                         for i, (a, b) in enumerate(steps, 1))
    why = "".join(f"<div><b>{esc(a)}</b><span>{esc(b)}</span></div>" for a, b in company["promises"])
    glance = [("Site", project.get("site")), ("Builder", project.get("builder")),
              ("Proposed start", project.get("start")),
              ("Installation", "After hours" if site["after_hours"] else "Normal working hours"),
              ("Payment", company["payment"]), ("Lead time", company["lead_time"])]
    glance_html = "".join(f"<dt>{esc(a)}</dt><dd>{esc(b)}</dd>" for a, b in glance if b)
    terms_html = "".join(f'<div class="clause"><b>{i}.</b><p>{esc(c)}</p></div>'
                         for i, c in enumerate(terms["clauses"], 1))
    signer = (f'<div class="sig-name">{esc(approval["reviewer"])}</div><div class="sig-role">{esc(company["name"])}</div>'
              if approved else '<div class="sig-name unsigned">[ Estimator not yet named &mdash; may not be issued ]</div>')

    doc = f'''<!doctype html><html lang="en-AU"><head><meta charset="utf-8">
<title>Quote {esc(q["number"])} &middot; {esc(client["company"])}</title>
<style>
@page {{ size: A4; margin: 0; }}
@media print {{ html, body {{ background: #fff !important; }} .page {{ margin: 0 !important; box-shadow: none; break-after: page; }}
  .page:last-child {{ break-after: auto; }} }}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; }}
body {{ font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; color: {INK}; background: #dcdad5;
  -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.page {{ width: 210mm; height: 297mm; margin: 10mm auto; background: #fff; position: relative; overflow: hidden;
  box-shadow: 0 6px 24px rgba(0,0,0,.12); display: flex; flex-direction: column; }}
.wm b {{ display: block; font-size: 15pt; letter-spacing: .02em; line-height: 1; }}
.wm span {{ display: block; font-size: 7pt; letter-spacing: .26em; text-transform: uppercase; color: {ACCENT}; margin-top: 1.4mm; }}
.eyebrow {{ font-size: 7.5pt; letter-spacing: .24em; text-transform: uppercase; color: {ACCENT}; font-weight: 700; }}
.cover {{ background: {WASH}; }}
.cover .left {{ position: absolute; left: 0; top: 0; bottom: 0; width: 56%; padding: 18mm 13mm 14mm 18mm; display: flex; flex-direction: column; }}
.cover .wm b {{ font-size: 19pt; }}
.cover .right {{ position: absolute; right: 0; top: 0; bottom: 0; width: 44%; background: {INK}; }}
.cover .right img {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
.cover .right::after {{ content: ""; position: absolute; left: 0; right: 0; bottom: 0; height: 45%;
  background: linear-gradient(to top, rgba(20,18,15,.85), rgba(20,18,15,0)); }}
.cover .title {{ margin-top: 42mm; }}
.cover h1 {{ font-family: Georgia, "Times New Roman", serif; font-weight: 400; font-size: 32pt; line-height: 1.06; margin: 5mm 0 4mm; }}
.cover h2 {{ font-weight: 300; font-size: 14pt; margin: 0; opacity: .85; line-height: 1.35; }}
.cover .rule {{ width: 18mm; height: 1.2mm; background: {ACCENT}; margin: 9mm 0; }}
.cover dl {{ display: grid; grid-template-columns: 27mm 1fr; gap: 2.4mm 4mm; margin: 0; font-size: 9pt; }}
.cover dt {{ opacity: .6; text-transform: uppercase; letter-spacing: .12em; font-size: 7pt; padding-top: .6mm; }}
.cover dd {{ margin: 0; font-weight: 600; }}
.cover .bottom {{ margin-top: auto; font-size: 8pt; line-height: 1.6; opacity: .75; }}
.cover .badge {{ position: absolute; right: 8mm; bottom: 10mm; z-index: 2; color: #fff; text-align: right; font-size: 8pt;
  letter-spacing: .06em; line-height: 1.5; max-width: 70mm; }}
.cover .badge b {{ display: block; font-size: 26pt; font-family: Georgia, serif; font-weight: 400; }}
.phead {{ display: flex; justify-content: space-between; align-items: center; padding: 11mm 16mm 6mm; border-bottom: .5pt solid #e4e1db; }}
.phead .ref {{ text-align: right; font-size: 8pt; line-height: 1.5; opacity: .7; }}
.phead .ref b {{ display: block; font-size: 9pt; opacity: 1; }}
.body {{ flex: 1; min-height: 0; padding: 7mm 16mm 5mm; display: flex; flex-direction: column; }}
.pfoot {{ flex: none; display: flex; justify-content: space-between; padding: 4mm 16mm 8mm; font-size: 6.8pt;
  letter-spacing: .04em; opacity: .6; border-top: .5pt solid #e4e1db; }}
h3 {{ font-size: 8pt; letter-spacing: .2em; text-transform: uppercase; margin: 0 0 3mm; color: {ACCENT}; }}
.gate {{ flex: none; background: #9f2a1e; color: #fff; padding: 2.6mm 16mm; font-size: 7.8pt; display: flex; gap: 3mm; }}
.demo {{ flex: none; background: #f3d36b; color: #3a2f00; padding: 2mm 16mm; font-size: 7.5pt; font-weight: 700; }}
.hello {{ font-family: Georgia, serif; font-size: 15pt; margin-bottom: 2.5mm; }}
.intro p {{ font-size: 9.6pt; line-height: 1.55; margin: 0 0 2mm; max-width: 160mm; }}
.intro {{ margin-bottom: 4mm; }}
.group {{ font-size: 7pt; letter-spacing: .18em; text-transform: uppercase; opacity: .55; margin: 3mm 0 1mm; }}
.lines {{ border-top: .5pt solid #e4e1db; margin-bottom: 5mm; }}
.line {{ display: grid; grid-template-columns: 9mm 1fr 14mm 28mm; align-items: center; padding: 1.7mm 0; border-bottom: .5pt solid #e4e1db; }}
.line-n {{ font-family: Georgia, serif; font-size: 11pt; color: {ACCENT}; }}
.line h4 {{ margin: 0; font-size: 9pt; font-weight: 600; }}
.line p {{ margin: .5mm 0 0; font-size: 7.6pt; opacity: .65; }}
.line-q {{ font-size: 8.5pt; opacity: .7; text-align: right; padding-right: 3mm; }}
.line-m {{ text-align: right; font-size: 10pt; font-weight: 300; }}
.invest {{ background: {INK}; color: #fff; border-radius: 3mm; padding: 6mm 8mm; display: grid; grid-template-columns: 1fr auto;
  align-items: end; gap: 4mm; margin-top: auto; }}
.invest h3 {{ color: #c9a874; }}
.invest .sum {{ font-size: 9pt; line-height: 1.9; opacity: .85; }}
.invest .sum span {{ display: inline-block; min-width: 26mm; opacity: .7; }}
.invest .big {{ text-align: right; }}
.invest .big small {{ display: block; font-size: 7.5pt; letter-spacing: .18em; text-transform: uppercase; opacity: .7; }}
.invest .big b {{ font-family: Georgia, serif; font-weight: 400; font-size: 30pt; }}
.inex {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8mm; margin-bottom: 5mm; }}
.ticks {{ list-style: none; margin: 0; padding: 0; }}
.ticks li {{ display: grid; grid-template-columns: 6mm 1fr; font-size: 8.8pt; line-height: 1.4; margin-bottom: 1.3mm; }}
.ticks i {{ font-style: normal; font-weight: 700; }}
.ticks.in i {{ color: #2f7d5b; }} .ticks.out i {{ color: #9f2a1e; }}
.glance {{ display: grid; grid-template-columns: 30mm 1fr; gap: 1.5mm 5mm; margin: 0 0 5mm; font-size: 9pt; }}
.glance dt {{ opacity: .6; text-transform: uppercase; letter-spacing: .12em; font-size: 7pt; padding-top: .7mm; }}
.glance dd {{ margin: 0; line-height: 1.45; }}
.steps {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 5mm; margin: 2mm 0 5mm; position: relative; }}
.steps::before {{ content: ""; position: absolute; left: 5mm; right: 5mm; top: 5mm; height: .6pt; background: #d8d4cc; }}
.step {{ position: relative; }}
.step .dot {{ width: 10mm; height: 10mm; border-radius: 50%; background: {ACCENT}; color: #fff; display: flex; align-items: center;
  justify-content: center; font-weight: 700; font-size: 10pt; margin-bottom: 3mm; }}
.step h4 {{ margin: 0 0 1.5mm; font-size: 10pt; }}
.step p {{ margin: 0; font-size: 8.3pt; line-height: 1.5; opacity: .75; }}
.why {{ background: {WASH}; border-radius: 3mm; padding: 5mm 7mm; margin-bottom: 5mm; display: grid; grid-template-columns: repeat(3, 1fr); gap: 6mm; }}
.why b {{ display: block; font-size: 9.5pt; margin-bottom: 1mm; }}
.why span {{ font-size: 8.3pt; line-height: 1.5; opacity: .75; }}
.accept {{ border: .6pt solid #d8d4cc; border-radius: 3mm; padding: 6mm 8mm; }}
.accept p {{ font-size: 9pt; line-height: 1.55; margin: 0 0 6mm; }}
.sigs {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12mm; }}
.sigrow {{ display: grid; grid-template-columns: 2fr 1fr; gap: 8mm; margin-top: 9mm; }}
.sig {{ border-top: .6pt solid {INK}; padding-top: 2mm; font-size: 7.5pt; letter-spacing: .1em; text-transform: uppercase; opacity: .7; }}
.from {{ margin-top: auto; padding-top: 4mm; font-size: 9pt; }}
.sig-name {{ font-family: Georgia, serif; font-size: 14pt; margin-top: 2mm; }}
.sig-name.unsigned {{ font-family: inherit; font-size: 9pt; color: #9f2a1e; font-weight: 700; }}
.sig-role {{ font-size: 8pt; opacity: .65; }}
.clauses {{ column-count: 2; column-gap: 9mm; }}
.clause {{ break-inside: avoid; margin-bottom: 3.6mm; display: grid; grid-template-columns: 6mm 1fr; }}
.clause b {{ font-size: 8.8pt; color: {ACCENT}; }}
.clause p {{ margin: 0; font-size: 8.4pt; line-height: 1.5; opacity: .85; }}
</style></head><body>

<section class="page cover">
  <div class="left">
    <div class="wm"><b>{esc(company["short_name"])}</b><span>{esc(company["tagline"])}</span></div>
    <div class="title">
      <div class="eyebrow">Quotation &middot; Furniture &amp; joinery</div>
      <h1>{esc(client["company"])}</h1>
      <h2>{esc(project["name"])}</h2>
    </div>
    <div class="rule"></div>
    <dl>
      <dt>Quote no.</dt><dd>{esc(q["number"])}</dd>
      <dt>Date</dt><dd>{long_date(qdate)}</dd>
      <dt>Prepared for</dt><dd>{esc(client.get("contact", ""))}</dd>
      <dt>Prepared by</dt><dd>{esc(approval.get("reviewer") or company["estimator"])}</dd>
      <dt>Valid until</dt><dd>{long_date(valid)}</dd>
    </dl>
    <div class="bottom">{esc(company["name"])}<br>{esc(company["locations"])}<br>{esc(company["website"])}</div>
  </div>
  <div class="right">{f'<img src="{cover}" alt="Commercial office fit-out">' if cover else ""}
    <div class="badge"><b>{badge_big}</b>{esc(badge_small)}</div></div>
</section>

<section class="page">
  {head(long_date(qdate))}{gate}{notice}
  <div class="body">
    <div class="intro"><div class="hello">Hi {esc(first)},</div>
      <p>Thank you for the opportunity to quote the {esc(project["name"])} at {esc(project["site"])}. Everything below is
      supplied or made by {esc(company["name"])}, delivered and installed.</p></div>
    <h3>Scope of works</h3>
    <div class="lines">
      <div class="group">Workstations and furniture</div>{furn}
      <div class="group">Joinery</div>{join}
      <div class="group">On site</div>{site_row}
    </div>
    <div class="invest">
      <div><h3>Your investment</h3><div class="sum"><div><span>Subtotal</span>{money(t["price_ex_gst"])} ex GST</div>
        <div><span>GST 10%</span>{money(t["gst"])}</div></div></div>
      <div class="big"><small>Total inc GST</small><b>{money(t["price_inc_gst"])}</b></div>
    </div>
  </div>
  {foot}
</section>

<section class="page">
  {head("Next steps")}{gate}{notice}
  <div class="body">
    <div class="inex"><div><h3>Included</h3>{ticks(includes, "in")}</div><div><h3>Not included</h3>{ticks(excludes, "out")}</div></div>
    <h3>Your project at a glance</h3><dl class="glance">{glance_html}</dl>
    <h3>What happens next</h3><div class="steps">{steps_html}</div>
    <div class="why">{why}</div>
    <h3>Acceptance</h3>
    <div class="accept"><p>I accept this quote ({esc(q["number"])}, {money(t["price_inc_gst"])} inc GST) and the terms on the
      next page, and authorise {esc(company["name"])} to proceed.</p>
      <div class="sigs"><div class="sig">Name</div><div class="sig">Position</div></div>
      <div class="sigrow"><div class="sig">Signature</div><div class="sig">Date</div></div></div>
    <div class="from">Kind regards,{signer}</div>
  </div>
  {foot}
</section>

<section class="page">
  {head("Terms")}{notice}
  <div class="body"><h3>{esc(terms["title"])}</h3><div class="clauses">{terms_html}</div></div>
  {foot}
</section>
</body></html>'''
    out = pathlib.Path(args[2])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")
    print(out)
    import csv
    rec = out.with_name("job-record.csv")
    with open(rec, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["Quote Number", "Project", "Client", "Contact", "Site", "Builder", "Status", "Estimator",
                    "Quote Date", "Valid Until", "Quote Value ex GST", "Workstation Positions", "Joinery Items",
                    "Board Sheets", "CNC Hours", "Install Hours", "Proposed Start", "Order Date", "Production Start",
                    "Delivery Date", "Install Date", "Invoiced", "Paid"])
        w.writerow([q["number"], project["name"], client["company"], client.get("contact", ""), project["site"],
                    project.get("builder", ""), "Quote sent" if approved else "Quote draft",
                    approval.get("reviewer", ""), qdate, valid, f"{t['price_ex_gst']:.2f}", positions,
                    len(k["joinery"]), sum(x["sheets"] for x in k["sheets"]), t["cnc_hours"],
                    site["install_hours"], project.get("start", ""), "", "", "", "", "", ""])
    print(rec)
    if "--pdf" in sys.argv:
        sys.path.insert(0, str(SKILL / "scripts"))
        from topdf import html_to_pdf
        ok, msg = html_to_pdf(out, out.with_suffix(".pdf"))
        print(msg if ok else f"PDF not made: {msg}")


if __name__ == "__main__":
    main()
