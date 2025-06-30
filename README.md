# ⚡ Copilot Monitor

> Real-time AI-based evaluator for code suggestions using Gemini + Supabase + VS Code Extension

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Made with TypeScript](https://img.shields.io/badge/language-TypeScript-blue)
![Built with Flask](https://img.shields.io/badge/backend-Flask-red)
![VS Code Extension](https://img.shields.io/badge/editor-VSCode-purple)

---

## 🚀 Overview

Copilot Monitor is a developer tool that **captures code suggestions inside VS Code**, sends them to a **Gemini-powered AI model** for evaluation, and logs results in **Supabase**. It displays a live rating notification inside your editor and stores prompt history for feedback & training analysis.

---

## 🧱 Tech Stack

| Layer           | Tech                      |
|----------------|---------------------------|
| Frontend       | VS Code Extension (TypeScript) |
| Backend        | Flask + Gemini API        |
| Database       | Supabase (PostgreSQL)     |
| Model          | Gemini 1.5 Flash          |

---

## ⚙️ Features

- 🧠 AI-based scoring of code completions (1–10 scale)
- 🔁 Live interaction between VS Code, backend, and Supabase
- 📬 Pop-up notifications inside VS Code after each rating
- 📦 Prompt logging and analytics via Supabase
- 🚨 Error handling and fallback logic (planned)

---

## 📦 Installation & Setup

### 1. Clone & Setup Backend

```bash
git clone https://github.com/your-username/copilot-monitor-backend.git
cd copilot-monitor-backend
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
Create a .env file:

env
Copy
Edit
GOOGLE_API_KEY=your-gemini-api-key
SUPABASE_CME_URL=https://your-project.supabase.co
SUPABASE_CME_KEY=your-service-role-key
Start the Flask server:

bash
Copy
Edit
python app.py
2. VS Code Extension (Frontend)
bash
Copy
Edit
cd copilot-monitor
npm install
npm run compile
Then open the folder in VS Code, press F5 to launch a new Extension Development Host.

🔍 How It Works
Developer types code → VS Code captures prompt/suggestion

Request is sent to Flask API → Gemini scores it

Score is logged to Supabase (with metadata)

Notification appears: 💡 Copilot Monitor Score: 8/10

🛣️ Project Roadmap
Phase	Description	Status
✅ Phase 1	Flask + Gemini scoring backend	Complete
✅ Phase 2	VS Code extension to capture suggestions	Complete
🔄 Phase 3	Integration Test (extension → backend → Supabase)	In Progress
🔁 Phase 4	Retry/Error handling + acceptance tracking	Upcoming
📊 Phase 5	Optional Dashboard (Streamlit / React)	Optional
✅ Phase 6	Polish + README + Docs	Complete
🚀 Phase 7	(Advanced) RL fine-tuning from user acceptance feedback	Future

📁 Folder Structure
bash
Copy
Edit
copilot-monitor-backend/
├── app.py              # Flask backend
├── .env                # API keys
├── requirements.txt
└── ...

copilot-monitor/        # VS Code Extension
├── src/extension.ts
├── esbuild.js
├── package.json
└── ...
💬 Example CURL Test
bash
Copy
Edit
curl -X POST http://127.0.0.1:5000/score \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "def rev(",
    "suggestion": "def rev(s): return s[::-1]",
    "lang": "python",
    "file_path": "test.py"
  }'
✅ License
This project is licensed under the MIT License.
Feel free to fork, modify, or contribute.

🙏 Acknowledgements
Google Gemini API

Supabase Team

VS Code API & Community
