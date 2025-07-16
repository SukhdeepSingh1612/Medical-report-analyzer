import streamlit as st
import os
import sys
from PyPDF2 import PdfReader

# Add src to path for imports
sys.path.append(os.path.abspath("src"))
from src.medical_analyzer.crew import MedicalSummarizerCrew


def extract_text_from_pdf(file):
    reader = PdfReader(file)
    return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])


def analyze_report(uploaded_file):
    output_dir = os.path.join("output")
    os.makedirs(output_dir, exist_ok=True)

    report_text = extract_text_from_pdf(uploaded_file)

    with st.expander("📄 Extracted Report Text", expanded=True):
        st.code(report_text, language="text")

    st.markdown("---")
    st.info("Running summarization and validation...")

    inputs = {"report_text": report_text}
    crew_instance = MedicalSummarizerCrew().crew()
    crew_instance.kickoff(inputs=inputs)

    summary_path = os.path.join(output_dir, "summary.txt")
    validation_path = os.path.join(output_dir, "validation_report.txt")

    summary = ""
    validation = ""

    if os.path.exists(summary_path):
        with open(summary_path, "r") as f:
            summary = f.read()

    if os.path.exists(validation_path):
        with open(validation_path, "r") as f:
            validation = f.read()

    st.markdown("### 📝 Generated Summary")
    st.success(summary)

    st.markdown("### ✅ Validator Feedback")
    st.warning(validation if "✅" not in validation else "✅ Summary matches the extracted data. No issues found.")

    if "✅ Summary matches the extracted data. No issues found." not in validation:
        st.markdown("---")
        st.info("Running revision based on validator feedback...")

        revise_inputs = {
            "report_text": report_text,
            "read_task.output": summary,
            "summarize_task.output": summary,
            "validate_summary_task.output": validation
        }

        revision_crew = MedicalSummarizerCrew().revision_crew()
        revision_crew.kickoff(inputs=revise_inputs)

        with open(summary_path, "r") as f:
            revised_summary = f.read()

        st.markdown("### ✏️ Revised Summary")
        st.success(revised_summary)

        # Re-validate again
        revalidate_inputs = {
            "read_task.output": summary,
            "summarize_task.output": revised_summary
        }

        revalidate_crew = MedicalSummarizerCrew().revision_crew()
        revalidate_crew.kickoff(inputs=revalidate_inputs)

        with open(validation_path, "r") as f:
            revalidation = f.read()

        st.markdown("### 🔁 Re-Validation Report")
        st.warning(revalidation if "✅" not in revalidation else "✅ Revised summary is now valid.")
    else:
        st.balloons()
        st.success("No revision required. The summary is already accurate!")


def main():
    st.set_page_config(page_title="Medical Report Analyzer", layout="centered")
    st.title("🧠 Medical Report Analyzer")
    st.caption("Powered by CrewAI - Analyze, Summarize, Validate.")

    uploaded_file = st.file_uploader("📥 Upload a PDF Medical Report", type=["pdf"])

    if uploaded_file is not None:
        if st.button("🔍 Analyze Report"):
            analyze_report(uploaded_file)


if __name__ == "__main__":
    main()
