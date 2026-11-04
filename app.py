from flask import Flask, render_template, request, send_file
from pathlib import Path
import traceback

from rag_ai_explanation import generate_rag_explanation
from data_ingestion import load_all_logs
from data_normalization import normalize_events
from timeline_reconstruction import reconstruct_timeline
from activity_correlation import detect_suspicious_activity
from database_storage import create_database, save_dataframe
from evidence_integrity import verify_evidence_integrity
from report_generation import generate_forensic_report

app = Flask(__name__)

INPUT_FOLDER = Path("input_logs")
OUTPUT_FOLDER = Path("output")

INPUT_FOLDER.mkdir(exist_ok=True)
OUTPUT_FOLDER.mkdir(exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    try:
        uploaded_files = {
            "login_logs.csv": request.files.get("login_logs"),
            "file_activity.csv": request.files.get("file_activity"),
            "usb_logs.csv": request.files.get("usb_logs")
        }

        for filename, file in uploaded_files.items():

            if not file or not file.filename:
                return "Please upload all three CSV files."

            if not filename.endswith(".csv"):
                return "Only CSV files are allowed."

            file.save(INPUT_FOLDER / filename)

        login, files, usb = load_all_logs()

        events = normalize_events(login, files, usb)

        timeline = reconstruct_timeline(events)

        findings = detect_suspicious_activity(timeline)

        create_database()

        save_dataframe(events, "normalized_events")
        save_dataframe(timeline, "activity_timeline")
        save_dataframe(findings, "suspicious_findings")

        integrity_data = verify_evidence_integrity()

        ai_explanation = generate_rag_explanation({
                "timeline": timeline.to_dict(orient="records"),
                "findings": findings.to_dict(orient="records")
        })

        generate_forensic_report(
            timeline,
            findings,
            integrity_data
        )

        
        total_events = len(timeline)
        total_findings = len(findings)

        if total_findings > 0:
            status = "Review Needed"
        else:
            status = "No Findings"

        return render_template(
            "result.html",
            timeline=timeline.to_html(
                classes="data-table",
                index=False
            ),
            findings=findings.to_html(
                classes="data-table",
                index=False
            ),
            total_events=total_events,
            total_findings=total_findings,
            status=status,
            ai_explanation=ai_explanation,
            report_exists=True
        )


    except Exception:
        traceback.print_exc()
        return "Analysis failed. Check the VS Code terminal for details."
@app.route("/download-report")
def download_report():
    report_path = OUTPUT_FOLDER / "forensic_investigation_report.pdf"

    if report_path.exists():
        return send_file(
            report_path,
            as_attachment=True,
            download_name="forensic_investigation_report.pdf"
        )

    return "PDF report not found. Please run the analysis first.", 404


if __name__ == "__main__":
    app.run(debug=True)