# FieldForm AI

## 🚀 Overview

FieldForm AI is an offline-first, CPU-powered AI application that transforms unstructured field inspection notes into structured JSON records.

The application is designed for government officers, NGOs, inspectors, survey teams, and organizations working in environments with limited or no internet connectivity.

All AI inference runs locally on the user's device without relying on cloud APIs, making the system privacy-friendly, reliable, and suitable for remote field operations.

## 🏆 Hackathon Highlights

FieldForm AI was developed for the **CPU-First Offline AI Hackathon** with the objective of demonstrating that powerful AI applications can run efficiently on ordinary laptops without relying on GPUs or cloud services.

### Highlights

- ✅ Fully Offline AI Processing
- ✅ CPU-Only Inference
- ✅ Local Ollama Language Model
- ✅ Offline Faster-Whisper Speech Recognition
- ✅ Structured JSON Extraction
- ✅ Automatic Data Validation
- ✅ SQLite Local Storage
- ✅ Interactive Analytics Dashboard
- ✅ Search & Filter Reports
- ✅ JSON & PDF Export
- ✅ Privacy-First Architecture

## ❗ Problem Statement

Field inspectors and survey teams often record observations as free-form text during inspections. These notes are later manually converted into structured reports, resulting in repetitive work, inconsistent formatting, and increased chances of human error.

In many remote locations, reliable internet connectivity is unavailable, making cloud-based AI solutions impractical. There is a need for a lightweight, offline-first system that can automatically convert inspection notes into structured data directly on the user's device.

## 💡 Solution

FieldForm AI provides an offline-first solution that transforms unstructured field inspection notes into structured JSON records using a lightweight local AI model running entirely on the CPU.

The generated structured records are validated and stored in a local SQLite database, enabling efficient search, reporting, and future analysis without requiring an internet connection or external cloud services.

## ✨ Features

- 🔒 Offline-first architecture (No cloud APIs)
- 💻 CPU-only AI inference using Ollama
- 🎤 Offline speech-to-text using Faster-Whisper
- 📝 Convert unstructured inspection notes into structured JSON
- ✅ Automatic schema validation and normalization
- 💾 Local SQLite database for report storage
- 📊 Interactive analytics dashboard
- 🔍 Search and filter inspection reports
- 📄 Export reports as JSON and PDF
- 📈 Severity and inspection trend visualization
- 🛡 Privacy-first processing (all data stays on-device)

## 🛠️ Technology Stack

| Component | Technology |
|------------|------------|
| Programming Language | Python 3.11+ |
| Frontend | Streamlit |
| AI Runtime | Ollama |
| Local Language Model | Qwen2.5 / Phi-3 Mini (GGUF) |
| Speech-to-Text | Faster-Whisper |
| Database | SQLite |
| Data Processing | Pandas |
| Data Visualization | Plotly |
| PDF Generation | ReportLab |
| Schema Validation | Pydantic |
| Version Control | Git & GitLab |
| Operating Mode | Offline-First |
| AI Execution | CPU-Only |
| Platform | Web Application |

## 🏗️ System Architecture

```text
                  User
          (Text / Voice Input)
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
 Text Inspection Notes   Voice Recording
                                │
                                ▼
               Faster-Whisper (Offline STT)
                                │
                                ▼
                     Unified Inspection Text
                                │
                                ▼
                 Ollama Local Language Model
                    (CPU-Only Inference)
                                │
                                ▼
              Structured JSON Extraction
                                │
                                ▼
         Validation & AI Output Normalization
                                │
                                ▼
               SQLite Local Database Storage
                                │
          ┌─────────────┼──────────────┐
          ▼             ▼              ▼
  Dashboard Analytics  Report Explorer  Search & Filters
          │
          ▼
     JSON Export / PDF Export
```

## 🔄 Application Workflow

### Text-Based Workflow

1. User enters unstructured field inspection notes.
2. Notes are sent to the local Ollama language model.
3. The AI extracts structured inspection information.
4. Output is normalized and validated against the inspection schema.
5. The validated report is stored in the local SQLite database.
6. Dashboard statistics and analytics update automatically.
7. Reports can be searched, filtered, viewed, edited, and exported as JSON or PDF.

---

### Voice-Based Workflow

1. User records inspection notes using the built-in microphone.
2. Faster-Whisper performs offline speech-to-text transcription.
3. The generated transcript is displayed for review and editing.
4. The corrected transcript follows the same AI processing pipeline.
5. The structured report is validated and stored locally.
6. Dashboard analytics update automatically.
7. Reports remain available offline for future access and export.

---

### Offline Processing Pipeline

```text
Text / Voice
      │
      ▼
Faster-Whisper (Voice Only)
      │
      ▼
Ollama Local AI
      │
      ▼
Schema Validation
      │
      ▼
SQLite Database
      │
      ▼
Dashboard → Search → PDF / JSON Export
```
## 📁 Project Structure

```text
fieldform-ai/
│
├── app/
│   ├── app.py              # Streamlit application
│   ├── database.py         # SQLite operations
│   ├── llm.py              # Local AI model integration
│   ├── parser.py           # JSON extraction logic
│   └── schema.py           # JSON schema definition
│
├── data/
│   └── sample_reports.json
│
├── docs/
│   ├── specification.md
│   ├── architecture.md
│   └── work-division.md
│
├── screenshots/
│
├── tests/
│   └── test_parser.py
│
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── CHANGELOG.md
├── requirements.txt
└── .gitlab-ci.yml
```

## ⚙️ Installation

### Prerequisites

* Python 3.10 or later
* Ollama installed locally
* A lightweight local language model (GGUF format)

## 🚀 Quick Start

```bash
git clone <repository-url>

cd fieldform-ai

pip install -r requirements.txt

streamlit run app/app.py
```

Open your browser at:

```
http://localhost:8501
```

Start by:

1. Entering or recording inspection notes.
2. Generate a structured report.
3. Review AI-normalized data.
4. Save to SQLite.
5. Explore analytics.
6. Export as JSON or PDF.

### Clone the repository

```bash
git clone <repository-url>
cd fieldform-ai
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Start the application

```bash
streamlit run app/app.py
```

## 📌 Key Capabilities

| Feature | Status |
|----------|--------|
| Offline AI Inference | ✅ |
| CPU-Only Processing | ✅ |
| Voice Input | ✅ |
| Faster-Whisper Speech-to-Text | ✅ |
| Local SQLite Storage | ✅ |
| AI Output Normalization | ✅ |
| Dashboard Analytics | ✅ |
| Search & Filter | ✅ |
| Report Explorer | ✅ |
| JSON Export | ✅ |
| PDF Export | ✅ |
| Offline Operation | ✅ |

## 🔮 Future Scope

- 🖼️ Image-based inspection analysis using OCR or Vision Language Models.
- 🌍 Multi-language speech recognition and report generation.
- 📱 Progressive Web App (PWA) support for offline installation.
- 📍 GPS and geotag integration for inspection sites.
- 👥 Multi-user authentication and role-based access.
- ☁️ Optional synchronization with a central server when internet connectivity becomes available.
- 📊 Advanced analytics and predictive safety insights.
- 📧 Automatic email notifications and report sharing.


## 📌 Key Capabilities

| Feature | Status |
|----------|--------|
| Offline AI Inference | ✅ |
| CPU-Only Processing | ✅ |
| Voice Input | ✅ |
| Faster-Whisper Speech-to-Text | ✅ |
| Local SQLite Storage | ✅ |
| AI Output Normalization | ✅ |
| Dashboard Analytics | ✅ |
| Search & Filter | ✅ |
| Report Explorer | ✅ |
| JSON Export | ✅ |
| PDF Export | ✅ |
| Offline Operation | ✅ |

## 📜 License

This project is released under the GNU General Public License v3.0 (GPL-3.0).

It is developed as part of the CPU-First Offline AI Hackathon and follows the requirement of using a strong copyleft open-source license.

## License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0). See the LICENSE file for details.

