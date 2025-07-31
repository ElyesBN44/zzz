from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def generate_pdf(filename: str):
    """Generate a PDF summarizing the AI Value Stream Mapping Generator Agent."""
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Title
    title_text = "AI Value Stream Mapping Generator Agent"
    c.setFont("Helvetica-Bold", 20)
    text_width = c.stringWidth(title_text, "Helvetica-Bold", 20)
    c.drawString((width - text_width) / 2.0, height - 72, title_text)

    # Body text settings
    c.setFont("Helvetica", 12)
    text_object = c.beginText(40, height - 108)
    lines = [
        "Purpose:",
        "The AI Value Stream Mapping Generator Agent assists in creating, analyzing, and improving value stream maps, which are critical tools in optimising business processes.",
        "It helps users visualise their processes to identify waste, inefficiencies, and opportunities for improvement.",
        "Capabilities:",
        "• Generate detailed value stream maps for various business processes,",
        "• Analyse existing processes for efficiency and identify bottlenecks and waste,",
        "• Propose comprehensive improvement plans based on data-driven insights,",
        "• Export maps and reports into shareable formats (e.g., PDF) for easy collaboration.",
        "Benefits:",
        "By utilising this agent, users can significantly enhance their operational efficiency and productivity, leading to streamlined workflows and increased value delivery.",
    ]

    # Write each line, add spacing
    for line in lines:
        text_object.textLine(line)
        if line.endswith(":"):
            text_object.moveCursor(0, -6)  # extra spacing after headings

    c.drawText(text_object)

    # Footer
    c.setFont("Helvetica-Oblique", 10)
    footer_text = "Generated automatically by the AI Value Stream Mapping Generator Agent"
    text_width = c.stringWidth(footer_text, "Helvetica-Oblique", 10)
    c.drawString((width - text_width) / 2.0, 30, footer_text)

    c.showPage()
    c.save()


if __name__ == "__main__":
    generate_pdf("AI_Value_Stream_Mapping_Generator_Agent.pdf")