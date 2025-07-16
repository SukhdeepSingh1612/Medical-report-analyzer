# 🧠 Medical Report Analyzer

A Streamlit application powered by [CrewAI](https://docs.crewai.com/) that reads, summarizes, and validates medical reports from PDF files using a team of AI agents.

## 🚀 Features

- 📄 Extracts text from uploaded PDF medical reports
- 📝 Summarizes the medical report using CrewAI agents
- ✅ Validates the summary for accuracy
- ✏️ Automatically revises the summary if validation fails
- 🔁 Re-validates the revised summary
- 💻 Built with Python, Streamlit, and CrewAI

## 📂 Project Structure

```
your-project-root/
├── app.py                          # Streamlit app entry point
├── src/
│   └── medical_analyzer/
│       ├── __init__.py
│       ├── crew.py                # Crew definition and task handling
│       ├── config/
│       │   ├── agents.yaml        # Agent configuration
│       │   └── tasks.yaml         # Task configuration
│       └── output/                # Output files (summary.txt, validation_report.txt)
├── data/
│   └── samples/
│       └── sample_medical_report.pdf
├── requirements.txt
```

## 🛠️ Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/medical-report-analyzer.git
cd medical-report-analyzer
```

2. **Create a virtual environment** (optional but recommended)

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the app**

```bash
streamlit run app.py
```

## 🧪 Requirements

- Python 3.10+
- Streamlit
- CrewAI
- PyPDF2

## 📄 License

MIT License
