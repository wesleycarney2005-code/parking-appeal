"""Generate a formatted PDF from the appeal letter text."""
from fpdf import FPDF
import io


def _safe(text: str) -> str:
    """Replace characters outside latin-1 range with ASCII equivalents."""
    return (text
        .replace("—", "--").replace("–", "-")
        .replace("‘", "'").replace("’", "'")
        .replace("“", '"').replace("”", '"')
        .replace("…", "...").replace(" ", " ")
        .encode("latin-1", errors="replace").decode("latin-1"))


def make_pdf(letter_text: str, pcn_ref: str = "APPEAL") -> bytes:
    pdf = FPDF()
    pdf.set_margins(25, 25, 25)
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=25)

    # Header bar
    pdf.set_fill_color(26, 22, 18)
    pdf.rect(0, 0, 210, 14, "F")
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(253, 251, 247)
    pdf.set_xy(0, 4)
    pdf.cell(210, 6, "PARKING FINE APPEAL LETTER", align="C")

    pdf.set_text_color(26, 22, 18)
    pdf.set_xy(25, 22)

    # Body
    pdf.set_font("Times", "", 11)

    for line in letter_text.split("\n"):
        stripped = line.strip()
        safe_line = _safe(line)
        safe_stripped = _safe(stripped)

        if stripped.startswith("RE:") or stripped.startswith("PCN Ref") or stripped.startswith("Vehicle") or stripped.startswith("Date of") or stripped.startswith("Location:"):
            pdf.set_font("Times", "B", 11)
            pdf.multi_cell(160, 6, safe_line)
            pdf.set_font("Times", "", 11)

        elif stripped.startswith("GROUNDS OF APPEAL") or stripped.startswith("CONCLUSION"):
            pdf.ln(3)
            pdf.set_font("Times", "B", 11)
            pdf.multi_cell(160, 6, safe_stripped)
            pdf.set_font("Times", "", 11)
            pdf.ln(1)

        elif stripped == "---":
            pdf.ln(2)
            pdf.set_draw_color(196, 184, 154)
            pdf.line(25, pdf.get_y(), 185, pdf.get_y())
            pdf.ln(4)

        elif stripped == "":
            pdf.ln(4)

        else:
            pdf.multi_cell(160, 6, safe_line)

    # Footer
    pdf.set_y(-20)
    pdf.set_font("Helvetica", "", 7)
    pdf.set_text_color(150, 130, 110)
    pdf.cell(160, 5, f"Generated via ParkingAppeal.co.uk | {pcn_ref}", align="C")

    return bytes(pdf.output())
