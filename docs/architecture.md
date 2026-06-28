# FieldForm AI Architecture

## System Flow

```text
                 User
                   │
                   ▼
        Field Inspection Notes
                   │
                   ▼
        Local Language Model
         (CPU-only Inference)
                   │
                   ▼
      Structured JSON Generation
                   │
                   ▼
          JSON Validation Layer
                   │
                   ▼
         SQLite Local Database
                   │
                   ▼
      Streamlit Dashboard / Search
```

## Components

### 1. User Interface

* Streamlit-based web application
* Accepts inspection notes as text input

### 2. AI Processing

* Runs locally using a lightweight language model
* No cloud APIs or internet required

### 3. Data Processing

* Extracts predefined fields
* Produces structured JSON

### 4. Storage

* SQLite database
* Local storage only

### 5. Dashboard

* View saved inspection reports
* Search and browse records
