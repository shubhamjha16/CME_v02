# ⚡ Copilot Monitor

> Real-time AI-based evaluator for code suggestions using Gemini + Supabase + VS Code Extension

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Made with TypeScript](https://img.shields.io/badge/language-TypeScript-blue)
![Built with Flask](https://img.shields.io/badge/backend-Flask-red)
![VS Code Extension](https://img.shields.io/badge/editor-VSCode-purple)

---

## 🚀 Overview

Copilot Monitor is a developer tool that **captures code suggestions inside VS Code**, sends them to a **Gemini-powered AI model** for evaluation, logs results in **Supabase**, and provides a **Streamlit dashboard for analytics**.
It displays a live rating notification inside your editor and stores prompt history, which can be visualized and analyzed using the provided dashboard.

---

## 🧱 Tech Stack

| Layer     | Tech                        |
|-----------|-----------------------------|
| Editor    | VS Code Extension (TypeScript) |
| Backend   | Flask + Gemini API (Python) |
| Database  | Supabase (PostgreSQL)       |
| Dashboard | Streamlit (Python)          |
| Model     | Gemini 1.5 Flash            |

---

## ✨ Features

- 🧠 AI-based scoring of code completions (1–10 scale).
- 🔁 Real-time interaction between VS Code, backend, and Supabase.
- 💡 Live popup notifications inside your editor for suggestion scores.
- 📦 Prompt logging & data persistence via Supabase.
- 🔁 Robust client-side (VS Code extension) and server-side (Flask backend) retry logic for API calls.
- 📊 Analytics dashboard (Streamlit) to view usage trends, average scores per file/language, and other insights.

---

## 🏁 Getting Started

Follow these steps to set up and run the complete Copilot Monitor system.

### Prerequisites

- Python 3.8+
- Pip (Python package installer)
- Node.js and npm (for the VS Code extension, if you need to modify or build it from source)
- VS Code Editor

### Setup Instructions

1.  **Clone the Repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Environment Variables:**
    Create a `.env` file in the project root directory. This file is used by both the Flask backend (`app.py`) and the Streamlit dashboard (`dashboard.py`). Add your credentials:
    ```dotenv
    GOOGLE_API_KEY=your_google_api_key
    SUPABASE_CME_URL=your_supabase_url
    SUPABASE_CME_KEY=your_supabase_service_role_key
    ```
    Replace placeholders with your actual keys.
    - `GOOGLE_API_KEY`: For Gemini model access (used by `app.py`).
    - `SUPABASE_CME_URL` & `SUPABASE_CME_KEY`: For connecting to your Supabase project.

3.  **Install Python Dependencies:**
    These are for the Flask backend and the Streamlit dashboard.
    ```bash
    pip install -r requirements.txt
    ```

4.  **VS Code Extension Setup:**
    - The pre-built extension might be available (check project releases or `.vsix` files).
    - To run from source or develop:
        - Navigate to the `copilot-monitor` sub-directory.
        - Install npm dependencies: `npm install`
        - Compile the extension: `npm run compile` (or use the watch script `npm run watch` during development).

### Running the System

1.  **Start the Flask Backend:**
    In your terminal, from the project root directory:
    ```bash
    python app.py
    ```
    Keep this terminal running. You should see output indicating the Flask server is running (e.g., on `http://127.0.0.1:5000/`).

2.  **Run the VS Code Extension:**
    - Open the `copilot-monitor` subfolder in a VS Code window.
    - Press `F5` or go to "Run and Debug" and select "Run Extension". This will open a new "Extension Development Host" (EDH) window.
    - In the EDH window, open or create a supported file (e.g., Python, TypeScript) and start typing to trigger Copilot suggestions. Accept suggestions to have them scored and logged.

3.  **Run the Streamlit Dashboard:**
    In a new terminal, from the project root directory:
    ```bash
    streamlit run dashboard.py
    ```
    This will typically open the dashboard in your default web browser (e.g., `http://localhost:8501`).
    *Note: The dashboard will display data collected by the backend and extension. Ensure you have generated some data by using Copilot in the EDH window while the backend is running.*


## 🗺 Project Roadmap

Phase	Description	Status
- ✅ Phase 1	Flask backend + Gemini scoring	Done
- ✅ Phase 2	VS Code Extension setup	Done
- ✅ Phase 3	Integrated flow testing	Done 
- ✅ Phase 4	Retry logic + accepted suggestions tracking	Done
- ✅ Phase 5	Dashboard (Streamlit) for analytics	Done
- ✅ Phase 6	Final polish + docs	Done
- 🚀 Phase 7	Reinforcement learning based on user behavior	Advanced

