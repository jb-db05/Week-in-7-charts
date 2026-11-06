#!/usr/bin/env python3
"""Build a 'week in 7 charts' Word document from JSON.  Usage: build_docx.py content.json out.docx

content.json:
{ "lang": "en-GB", "title": "...", "date": "...",
  "charts": [ {"heading": "...", "subtitle": "(optional)", "paragraphs": ["..."],
               "bullets": ["(optional)"], "paragraphs_after": ["(optional)"],
               "image": "path.png", "image_width_in": 5.0, "source": "Source: ..."} ],
  "disclaimer_heading": "...", "disclaimer": "..." }
Requires python-docx.
"""
import json, sys
from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def border(p, pos="bottom"):
    b = OxmlElement("w:pBdr"); e = OxmlElement(f"w:{pos}")
    for k, v in (("val", "single"), ("sz", "6"), ("space", "4"), ("color", "808080")):
        e.set(qn(f"w:{k}"), v)
    b.append(e); p._p.get_or_add_pPr().append(b)

def build(c, out):
    d = Document(); s = d.sections[0]
    s.page_width, s.page_height = Cm(21), Cm(29.7)
    s.left_margin = s.right_margin = s.top_margin = Cm(2); s.bottom_margin = Cm(1.5)
    st = d.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(11)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri"); st.paragraph_format.space_after = Pt(6)
    d.core_properties.language = c.get("lang", "en-GB"); d.core_properties.title = c["title"]; d.core_properties.author = ""

    def para(text, bold=False, size=None, align=None, italic=False, after=None, before=None, keep=False, color=None):
        p = d.add_paragraph(); r = p.add_run(text); r.bold = bold; r.italic = italic
        if size: r.font.size = Pt(size)
        if color: r.font.color.rgb = RGBColor(*color)
        if align is not None: p.alignment = align
        if after is not None: p.paragraph_format.space_after = Pt(after)
        if before is not None: p.paragraph_format.space_before = Pt(before)
        if keep: p.paragraph_format.keep_with_next = True
        return p

    J, C, GREY = WD_ALIGN_PARAGRAPH.JUSTIFY, WD_ALIGN_PARAGRAPH.CENTER, (0x55, 0x55, 0x55)
    para(c["title"], True, 16, C, after=2)
    border(para(c["date"], True, 12, C, after=10))
    for ch in c["charts"]:
        para(ch["heading"], True, 12, before=12, after=4, keep=True)
        if ch.get("subtitle"): para(ch["subtitle"], italic=True, keep=True)
        for t in ch.get("paragraphs", []): para(t, align=J)
        for b in ch.get("bullets", []):
            d.add_paragraph(b, style="List Bullet").paragraph_format.space_after = Pt(2)
        for t in ch.get("paragraphs_after", []): para(t, before=4, align=J)
        if ch.get("image"):
            ip = d.add_paragraph(); ip.alignment = C
            ip.paragraph_format.keep_with_next = True; ip.paragraph_format.space_after = Pt(2)
            ip.add_run().add_picture(ch["image"], width=Inches(min(ch.get("image_width_in", 5.0), 6.5)))
        para(ch["source"], italic=True, size=9, align=C, color=GREY)
    border(para(c["disclaimer_heading"], True, 10, before=14, after=2, keep=True), "top")
    para(c["disclaimer"], size=8.5, color=GREY, align=J)
    d.save(out)

if __name__ == "__main__":
    build(json.load(open(sys.argv[1], encoding="utf-8")), sys.argv[2])
