---
name: week-in-7-charts-rewrite
description: Turn the internal "The week in 7 charts" Word document into externally publishable English and French Word versions, with wording rewritten from scratch every time so the output never matches the source text. Use whenever the user supplies a "week in 7 charts" .docx (or similar weekly charts note) and asks for external publication, a rewrite, a reformulation, or EN/FR versions.
---

# Week in 7 charts: rewrite for external publication (EN + FR)

Goal: from the internal .docx, always deliver **two Word files** (English, French) that are
(1) suitable for publication outside the bank, and (2) **fully reworded**, so no sentence is
copied from the source document or from any earlier version.

## Workflow

1. **Extract** the source: `pandoc in.docx -t markdown --extract-media=media`. Look at every image
   (Read tool): check for hand-drawn annotations, watermarks, internal logos, and whether the image
   matches its text. Check headers/footers for internal content.
2. **Rewrite the English** from scratch (rules below). Never edit the source sentence by sentence;
   restructure, change vocabulary and sentence order, and rewrite headings, bullets and the disclaimer too.
3. **Translate the French from the new English** (not from the source), with French typography:
   decimal commas, non-breaking space before `: ; ! ? %`, "Graphique n°", "milliards de dollars", spaces in thousands (7 354).
4. **Build both .docx** with `scripts/build_docx.py content.json out.docx` (A4, 2 cm margins, Calibri 11,
   images kept with their captions). Write one JSON per language (schema in the script header).
5. **Render to PDF** (`soffice --headless --convert-to pdf`) and check the pages visually.
6. **Commit and push** both files to the designated branch, then send both to the user (SendUserFile, display render).
7. **Report** the caveats below. Offer, don't assume, anything beyond that.

## Rewrite rules (external audience)

- Facts, figures, dates, index names and source names stay exact; everything else is reworded. Do not change a number.
- Neutral, professional tone: no emojis, no hype ("wipeout", "party"), no first-person opinion that reads as advice,
  no partisan framing, no "keep printing"-style remarks. "We" only where the house view is intended; prefer impersonal wording.
- Attribute claims you cannot verify to their source ("according to the source below").
- Source lines: proper names (Zero Hedge, Citadel Securities, J.P. Morgan, U.S. Census Bureau...), not handles alone.
  If an image's real origin is visible in it (e.g. a TradingView heatmap), say so but flag it as inferred.
- Always end with an "Important notice" disclaimer (information only, not advice, past performance, third-party data,
  opinions may change). Keep it generic and tell the user compliance must replace it with the approved text.
- Reword each time with new phrasing: if a previous version exists, avoid its wording too, not only the original's.

## Caveats to always raise

- Image rights: screenshots of X posts and third-party charts (Zero Hedge, Citadel, J.P. Morgan, TradingView) may need permission.
- Images that do not support the text, or are partisan or hand-annotated (e.g. Biden/Trump labels), or are "traced"/not primary-source.
- Figures cannot be verified from the documents; ask the user to confirm against market data.
- Index mismatches (e.g. Nasdaq 100 vs Nasdaq Composite): name the index precisely.
- Disclaimer is generic and needs compliance wording.
- Plagiarism checkers can still match numbers, names and source lines; rewording does not replace attribution.
