"""Rebuild the one-page PDF résumé from its editable, reviewed content."""

import argparse
import json
import shutil
from html import escape
from pathlib import Path

from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
NAME = "Juan_Hernandez_Guizar_Resume.pdf"
WIDTH, HEIGHT = 612, 792
MARGIN = 36
CONTENT_WIDTH = WIDTH - 2 * MARGIN
BODY = ParagraphStyle(
    "Body", fontName="ResumeSerif", fontSize=11, leading=12.25,
    spaceBefore=0, spaceAfter=0,
)
RIGHT = ParagraphStyle("Right", parent=BODY, alignment=TA_RIGHT)
BULLET = ParagraphStyle(
    "Bullet", parent=BODY, leftIndent=18, firstLineIndent=0, bulletIndent=0,
    bulletFontName="ResumeSerif", bulletFontSize=11,
)
HEADING = ParagraphStyle("Heading", parent=BODY, fontName="ResumeSerif-Bold")
TITLE = ParagraphStyle(
    "Name", parent=HEADING, fontSize=13, leading=14.5,
)
TABLE_STYLE = TableStyle([
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ("TOPPADDING", (0, 0), (-1, -1), 0),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
])


def register_fonts(font_dir=None):
    """Embed installed serif fonts; never depend on a viewer's substitution."""
    candidates = [font_dir] if font_dir else [
        Path("/System/Library/Fonts/Supplemental"),
        Path("/usr/share/fonts/truetype/liberation2"),
        Path("/usr/share/fonts/truetype/liberation"),
        Path("C:/Windows/Fonts"),
    ]
    filenames = [
        ("Times New Roman.ttf", "Times New Roman Bold.ttf",
         "Times New Roman Italic.ttf", "Times New Roman Bold Italic.ttf"),
        ("LiberationSerif-Regular.ttf", "LiberationSerif-Bold.ttf",
         "LiberationSerif-Italic.ttf", "LiberationSerif-BoldItalic.ttf"),
        ("times.ttf", "timesbd.ttf", "timesi.ttf", "timesbi.ttf"),
    ]
    for directory in candidates:
        for family in filenames:
            paths = [directory / filename for filename in family]
            if all(path.is_file() for path in paths):
                for suffix, path in zip(("", "-Bold", "-Italic", "-BoldItalic"), paths):
                    pdfmetrics.registerFont(TTFont("ResumeSerif" + suffix, str(path)))
                pdfmetrics.registerFontFamily(
                    "ResumeSerif", normal="ResumeSerif", bold="ResumeSerif-Bold",
                    italic="ResumeSerif-Italic", boldItalic="ResumeSerif-BoldItalic",
                )
                return
    raise FileNotFoundError(
        "Install Times New Roman or Liberation Serif, or supply --font-dir."
    )


def para(text, style=BODY):
    return Paragraph(text, style, bulletText="\u2022" if style is BULLET else None)


def row(left, right, *, right_width=97, left_style=BODY, right_url=None):
    right_text = escape(right)
    if right_url:
        right_text = f'<link href="{escape(right_url, quote=True)}">{right_text}</link>'
    if left_style is BULLET:
        table = Table(
            [[para("\u2022"), para(left), para(right_text, RIGHT)]],
            colWidths=[18, CONTENT_WIDTH - right_width - 18, right_width],
        )
    else:
        table = Table(
            [[para(left, left_style), para(right_text, RIGHT)]],
            colWidths=[CONTENT_WIDTH - right_width, right_width],
        )
    table.setStyle(TABLE_STYLE)
    return table


def bullets(items):
    return [Paragraph(text, BULLET, bulletText="\u2022") for text in items]


def section(title):
    return [
        Spacer(1, 8), para(title, HEADING),
        HRFlowable(width="100%", thickness=0.65, color=colors.black),
        Spacer(1, 2),
    ]


def make_story(data):
    story = [row(
        escape(data["name"]),
        data["linkedin_label"],
        right_width=260,
        left_style=TITLE,
        right_url=data["linkedin"],
    )]
    # Keep the original compact header while preserving working contact links.
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.black))
    contacts = Table([[
        para(escape(data["location"])),
        para(escape(data["phone"])),
        para(f'<link href="mailto:{escape(data["email"], quote=True)}">'
             f'{escape(data["email"])}</link>', RIGHT),
    ]], colWidths=[235, 100, CONTENT_WIDTH - 335])
    contacts.setStyle(TABLE_STYLE)
    story.append(contacts)
    story.extend(section("EXPERIENCE"))
    blue = data["blue_origin"]
    story.append(row(
        f'<b><i>{escape(blue["role"])}</i></b>, '
        f'{escape(blue["company"])}, {escape(blue["location"])}',
        blue["role_dates"],
    ))
    story.append(para(
        f'<b>{escape(blue["level"])}</b>'
        + (f' (since {escape(blue["level_start"])})' if blue["level_start"] else "")
        + ' | Blue Origin: '
        f'{escape(blue["company_dates"])}'
    ))
    story.append(para(escape(blue["earlier_roles"])))
    story.extend(bullets(blue["bullets"]))
    for job in data["experience"]:
        story.append(Spacer(1, 7))
        heading = row(
            f'<b><i>{escape(job["role"])}</i></b>, '
            f'{escape(job["company"])}, {escape(job["location"])}',
            job["dates"],
        )
        story.append(KeepTogether([heading, *bullets(job["bullets"])]))
    story.extend(section("SPECIALIZED SKILLS &amp; AWARDS"))
    story.extend(bullets(data["skills"]))
    story.extend(section("PROFESSIONAL AFFILIATIONS"))
    for affiliation in data["affiliations"]:
        story.append(row(escape(affiliation["text"]), affiliation["dates"], left_style=BULLET))
    story.extend(section("EDUCATION"))
    for index, school in enumerate(data["education"]):
        if index:
            story.append(Spacer(1, 7))
        label = f'<b><i>{escape(school["degree"])}</i></b>'
        if school["school"]:
            label += ", " + escape(school["school"])
        story.append(KeepTogether([
            row(label, school["date"]),
            para(escape(school["institution"])),
            *bullets(school["bullets"]),
        ]))
    return story


def build(output, font_dir=None):
    register_fonts(font_dir)
    data = json.loads((ROOT / "resume_files/resume-content.json").read_text())
    output.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        # SimpleDocTemplate's frame adds 6 pt of padding inside these margins.
        str(output), pagesize=(WIDTH, HEIGHT), leftMargin=MARGIN - 6,
        rightMargin=MARGIN - 6, topMargin=29, bottomMargin=24,
        title="Juan Hernandez Guizar - Resume",
        author="Juan Hernandez Guizar", subject="Professional resume",
        pageCompression=1,
    )
    doc.build(make_story(data))
    reader = PdfReader(output)
    if len(reader.pages) != 1:
        raise ValueError(f"Expected one page, generated {len(reader.pages)}; review layout.")
    text = reader.pages[0].extract_text()
    for expected in (data["blue_origin"]["role"], data["blue_origin"]["level"], "10/2022 - Present"):
        if expected not in text:
            raise ValueError(f"Missing expected résumé text: {expected}")
    expected_bullets = (
        len(data["blue_origin"]["bullets"])
        + sum(len(job["bullets"]) for job in data["experience"])
        + len(data["skills"]) + len(data["affiliations"])
        + sum(len(school["bullets"]) for school in data["education"])
    )
    if text.count("\u2022") != expected_bullets:
        raise ValueError("Missing or malformed bullet points; review PDF text extraction.")
    # The dated PDFs remain unchanged archives. Only this stable URL is current.
    for target in (ROOT / "resume_files" / NAME, ROOT / "docs/resume_files" / NAME):
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.resolve() != output.resolve():
            shutil.copy2(output, target)
    print(f"Generated and checked: {output} (1 page)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "output/pdf" / NAME)
    parser.add_argument("--font-dir", type=Path, help="Installed Times New Roman / Liberation Serif fonts")
    args = parser.parse_args()
    build(args.output, args.font_dir)
