# FieldForm AI

## 🚀 Overview

FieldForm AI is an offline-first, CPU-powered AI application that transforms unstructured field inspection notes into structured JSON records.

The application is designed for government officers, NGOs, inspectors, survey teams, and organizations working in environments with limited or no internet connectivity.

All AI inference runs locally on the user's device without relying on cloud APIs, making the system privacy-friendly, reliable, and suitable for remote field operations.

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

| Component            | Technology                                          |
| -------------------- | --------------------------------------------------- |
| Programming Language | Python 3                                            |
| Frontend             | Streamlit                                           |
| AI Runtime           | Ollama (CPU)                                        |
| Local Language Model | Lightweight GGUF Model (e.g., Qwen2.5 / Phi-3 Mini) |
| Database             | SQLite                                              |
| Version Control      | Git & GitLab                                        |
| Operating Mode       | Offline-First                                       |
| Platform             | Web Application                                     |

## 🏗️ System Architecture

```text
                User
                  │
                  ▼
      Enter Field Inspection Notes
                  │
                  ▼
      Local CPU-based Language Model
        (Offline AI Inference)
                  │
                  ▼
      Structured JSON Extraction
                  │
                  ▼
          SQLite Local Database
                  │
                  ▼
      Search • View • Export Reports
```

### Workflow

1. The user enters field inspection notes.
2. The application processes the text using a local CPU-based AI model.
3. The AI extracts structured information into a predefined JSON schema.
4. The extracted data is validated.
5. The validated record is stored in a local SQLite database.
6. Users can search and view stored inspection reports without requiring an internet connection.

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

## 🔮 Future Scope

* Support voice input using Whisper.cpp.
* Support image-based inspection reports using OCR.
* Export reports to CSV and PDF.
* Advanced dashboard with analytics and visualizations.
* Multi-language support for regional field workers.
* Synchronization with a central server when internet becomes available.

## 📜 License

This project is released under the GNU General Public License v3.0 (GPL-3.0).

It is developed as part of the CPU-First Offline AI Hackathon and follows the requirement of using a strong copyleft open-source license.

