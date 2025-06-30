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

## 📦 Installation & Setup

### 🔧 Backend (Flask + Gemini + Supabase)

```bash
git clone https://github.com/your-username/copilot-monitor-backend.git
cd copilot-monitor-backend
python -m venv venv
venv\Scripts\activate   # On Windows
pip install -r requirements.txt

Create a .env file in root:

GOOGLE_API_KEY=your-gemini-api-key
SUPABASE_CME_URL=https://yourproject.supabase.co
SUPABASE_CME_KEY=your-service-role-key

Run the server:

python app.py

💻 Frontend (VS Code Extension)

cd copilot-monitor
npm install
npm run compile

To launch:





Open this folder in VS Code.



Press F5 to open an Extension Development Host.



In the new window, open a file like test.py.



Start typing something like:

def rev(

It should trigger Copilot → Gemini scores the suggestion → you'll see a VS Code popup:
💡 Copilot Monitor Score: 9/10



🔍 Example API Call

curl -X POST http://127.0.0.1:5000/score \
  -H "Content-Type: application/json" \
  -d '{"prompt":"def rev(","suggestion":"def rev(s): return s[::-1]","lang":"python","file_path":"test.py"}'

Response:

{
  "score": 9
}



📁 Folder Structure

copilot-monitor-backend/
├── app.py
├── .env
├── requirements.txt

copilot-monitor/
├── src/extension.ts
├── esbuild.js
├── package.json



📊 Roadmap







Phase



Description



Status





✅



Phase 1: Flask + Gemini scoring API



Completed





✅



Phase 2: VS Code extension captures suggestions



Completed





⏳



Phase 3: Integration Test (extension → backend → Supabase)



In Progress





⏳



Phase 4: Retry logic, error handling, acceptance tracking



Upcoming





⏳



Phase 5: Optional dashboard (Streamlit/React)



Optional





✅



Phase 6: Final polish, cleanup, documentation



Completed





🚀



Phase 7: Reinforcement learning from user feedback



Advanced



🧪 Testing Tips





Open a test file (test.py)



Trigger a suggestion (def rev()



You should see:





🔍 Gemini raw response: I rate this 8 out of 10... (in app.py terminal)



Popup: 💡 Copilot Monitor Score: 8/10



Entry logged in Supabase under prompt_log table
