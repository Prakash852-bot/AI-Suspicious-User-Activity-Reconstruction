import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from rag_ai_explanation import generate_rag_explanation
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from pathlib import Path
from datetime import datetime

OUTPUT_FOLDER = Path("output")
OUTPUT_FOLDER.mkdir(exist_ok=True)


def generate_forensic_report(timeline, findings, integrity_data):

    report_path = OUTPUT_FOLDER / "forensic_investigation_report.pdf"

    document = SimpleDocTemplate(
        str(report_path),
        pagesize=A4
    )

    styles = getSampleStyleSheet()
    content = []

    # Report title
    content.append(
        Paragraph(
            "<b>AI-BASED SUSPICIOUS USER ACTIVITY RECONSTRUCTION</b>",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 15))

    content.append(
        Paragraph(
            "DIGITAL FORENSIC INVESTIGATION REPORT",
            styles["Heading2"]
        )
    )

    content.append(Spacer(1, 10))

    # Investigation information
    content.append(
        Paragraph(
            f"Report Generated: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 15))

    # Investigation summary
    content.append(
        Paragraph("1. Investigation Summary", styles["Heading2"])
    )

    summary = f"""
    Total activity events analyzed: {len(timeline)}<br/>
    Correlated activity findings: {len(findings)}<br/>
    Evidence files processed: {len(integrity_data)}
    """

    content.append(Paragraph(summary, styles["Normal"]))
    content.append(Spacer(1, 15))

    # Timeline section
    content.append(
        Paragraph("2. User Activity Timeline", styles["Heading2"])
    )

    timeline_data = [
        ["Event ID", "Timestamp", "User", "Action", "Source"]
    ]

    for _, row in timeline.iterrows():
        timeline_data.append([
            str(row["event_id"]),
            str(row["timestamp"]),
            str(row["user"]),
            str(row["action"]),
            str(row["source"])
        ])

    timeline_table = Table(
        timeline_data,
        repeatRows=1,
        colWidths=[0.55*inch, 1.35*inch, 0.65*inch, 1.65*inch, 0.65*inch]
    )

    timeline_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6)
    ]))

    content.append(timeline_table)
    content.append(Spacer(1, 15))

    # Findings section
    content.append(
        Paragraph("3. Correlated Activity Findings", styles["Heading2"])
    )

    if findings.empty:
        content.append(
            Paragraph(
                "No matching activity sequence was detected.",
                styles["Normal"]
            )
        )
    else:
        for index, row in findings.iterrows():

            finding_text = f"""
            Finding {index + 1}<br/>
            User: {row['user']}<br/>
            File: {row['file_name']}<br/>
            USB Device: {row['usb_device']}<br/>
            Result: {row['finding']}<br/>
            Status: {row['status']}
            """

            content.append(
                Paragraph(finding_text, styles["Normal"])
            )
            content.append(Spacer(1, 8))

    content.append(Spacer(1, 15))

    # Evidence integrity section
    content.append(
        Paragraph("4. Evidence Integrity Information", styles["Heading2"])
    )

    integrity_table_data = [
        ["Evidence File", "SHA-256 Hash"]
    ]

    for _, row in integrity_data.iterrows():
        integrity_table_data.append([
            str(row["file_name"]),
            str(row["sha256_hash"])
        ])

    integrity_table = Table(
        integrity_table_data,
        colWidths=[1.5*inch, 5.0*inch]
    )

    integrity_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("VALIGN", (0, 0), (-1, -1), "TOP")
    ]))

    content.append(integrity_table)
    content.append(Spacer(1, 15))

    # Conclusion
    content.append(
        Paragraph("5. Investigation Conclusion", styles["Heading2"])
    )

    conclusion = """
    The system processed the supplied activity logs, reconstructed
    the chronological event timeline, and identified matching activity
    sequences for further investigation. SHA-256 hash values were
    generated for the supplied evidence files.

    A correlated activity sequence is an investigation lead and does
    not independently establish unauthorized activity or wrongdoing.
    """

    content.append(
        Paragraph(conclusion, styles["Normal"])
    )
    
    # AI + RAG Explanation
    activity_details = f"""
    TIMELINE:
    {timeline}

    FINDINGS:
    {findings}
    """

    ai_explanation = generate_rag_explanation(activity_details)

    content.append(Spacer(1, 15))
    content.append(
        Paragraph("5. AI-Based Forensic Analysis", styles["Heading2"])
    )

    from xml.sax.saxutils import escape

    for line in ai_explanation.splitlines():
        if line.strip():
            content.append(
                Paragraph(escape(line), styles["Normal"])
            )
        else:
            content.append(Spacer(1, 6))

    # Generate PDF
    document.build(content)

    print("\nForensic PDF report generated successfully!")
    print("Report location:", report_path)

    return report_path
