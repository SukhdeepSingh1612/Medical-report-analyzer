# import os
# from PyPDF2 import PdfReader
# from medical_analyzer.crew import MedicalSummarizerCrew

# def extract_text_from_pdf(file_path):
#     reader = PdfReader(file_path)
#     return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

# def run():
#     os.makedirs("output", exist_ok=True)

#     file_path = "data/samples/sample_medical_report.pdf"
#     report_text = extract_text_from_pdf(file_path)

#     inputs = {
#         "report_text": report_text
#     }

#     result = MedicalSummarizerCrew().crew().kickoff(inputs=inputs)

#     print("\n=== FINAL OUTPUT (from last task, likely validator) ===\n")
#     print(result)

# if __name__ == "__main__":
#     run()

import os
from PyPDF2 import PdfReader
from medical_analyzer.crew import MedicalSummarizerCrew

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

def run():
    os.makedirs("output", exist_ok=True)

    file_path = "data/samples/sample_medical_report.pdf"
    report_text = extract_text_from_pdf(file_path)

    inputs = {
        "report_text": report_text
    }

    crew_instance = MedicalSummarizerCrew().crew()
    result = crew_instance.kickoff(inputs=inputs)

    print("\n=== FINAL OUTPUT (from last task, likely validator) ===\n")
    print(result)

    # Read validator output from file
    with open("output/validation_report.txt", "r") as f:
        validation = f.read()

    if "✅ Summary matches the extracted data. No issues found." not in validation:
        print("\n=== REVISING SUMMARY BASED ON VALIDATOR FEEDBACK ===\n")
        # Prepare inputs for revision
        with open("output/summary.txt", "r") as f:
            summary = f.read()
        revise_inputs = {
            "report_text": report_text,
            "read_task.output": open("output/summary.txt").read(),  # or however your framework expects
            "summarize_task.output": summary,
            "validate_summary_task.output": validation
        }
        # Run only the revise_summary_task
        # You may need to create a new Crew with just the revise task, or call it directly
        revise_result = MedicalSummarizerCrew().revise_summary_task().run(revise_inputs)
        print("\n=== REVISED SUMMARY ===\n")
        print(revise_result)
        # (Optional) Re-validate
        revalidate_inputs = {
            "read_task.output": open("output/summary.txt").read(),
            "summarize_task.output": revise_result
        }
        revalidate_result = MedicalSummarizerCrew().validate_summary_task().run(revalidate_inputs)
        print("\n=== RE-VALIDATION OUTPUT ===\n")
        print(revalidate_result)
    else:
        print("\n=== SUMMARY IS VALID. NO REVISION NEEDED. ===\n")

if __name__ == "__main__":
    run()