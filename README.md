# ⚡ Copilot Monitor

> Real-time AI-based evaluator for code suggestions using Gemini + Supabase + VS Code Extension

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Made with TypeScript](https://img.shields.io/badge/language-TypeScript-blue)
![Built with Flask](https://img.shields.io/badge/backend-Flask-red)
![VS Code Extension](https://img.shields.io/badge/editor-VSCode-purple)

---

## 🚀 Overview

Copilot Monitor is a developer tool that **captures code suggestions inside VS Code**, sends them to a **Gemini-powered AI model** for evaluation, and logs results in **Supabase**.  
It displays a live rating notification inside your editor and stores prompt history for feedback & analysis.

---

## 🧱 Tech Stack

| Layer     | Tech                      |
|-----------|---------------------------|
| Frontend  | VS Code Extension (TypeScript) |
| Backend   | Flask + Gemini API        |
| Database  | Supabase (PostgreSQL)     |
| Model     | Gemini 1.5 Flash          |

---

## ⚙️ Features

- 🧠 AI-based scoring of code completions (1–10 scale)
- 🔁 Real-time interaction between VS Code, backend, and Supabase
- 💡 Live popup notifications inside your editor
- 📦 Prompt logging & analytics via Supabase
- 🔁 Retry logic & user acceptance tracking (planned)

---

## 📊 Analytics Dashboard (Streamlit)

This project includes a Streamlit dashboard to view analytics from the collected data.

### Prerequisites

- Python 3.8+
- Pip (Python package installer)

### Setup & Running the Dashboard

1.  **Environment Variables:**
    Ensure you have a `.env` file in the project root directory (where `app.py` and `dashboard.py` are located) with the following variables set:
    ```
    GOOGLE_API_KEY=your_google_api_key
    SUPABASE_CME_URL=your_supabase_url
    SUPABASE_CME_KEY=your_supabase_service_role_key
    ```
    Replace `your_google_api_key`, `your_supabase_url`, and `your_supabase_service_role_key` with your actual credentials.

2.  **Install Dependencies:**
    Navigate to the project's root directory in your terminal and install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Dashboard:**
    Once dependencies are installed, you can run the Streamlit dashboard using the following command:
    ```bash
    streamlit run dashboard.py
    ```
    This will typically open the dashboard in your default web browser.

---


## 🗺 Project Roadmap

Phase	Description	Status
- ✅ Phase 1	Flask backend + Gemini scoring	Done
- ✅ Phase 2	VS Code Extension setup	Done
- ✅ Phase 3	Integrated flow testing	Done 
- ⏳ Phase 4	Retry logic + accepted suggestions tracking	(Pending)
- ⏳ Phase 5	Dashboard (Streamlit/React) for analytics	(Pending)
- ✅ Phase 6	Final polish + docs	Done
- 🚀 Phase 7	Reinforcement learning based on user behavior	Advanced

