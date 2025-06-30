**Copilot Monitor
A VS Code extension + Flask backend system that monitors AI code suggestions (like from GitHub Copilot), rates them using Google Gemini, and logs everything to Supabase for analytics.

📦 Features
⚡ Real-Time Prompt Scoring
VS Code captures the prompt and suggestion, sends it to a local Flask server.

🤖 Google Gemini Evaluation
Gemini (via the Generative AI API) evaluates the suggestion for accuracy, relevance, and style (1–10 score).

🧾 Supabase Logging
Prompt, suggestion, language, score, and file path are logged to a Supabase table (prompt_log) for later analysis.

🧠 Optional Feedback Loop
Accept/reject handling and retry logic (in future phases).

🧱 Project Structure
bash
Copy
Edit
copilot-monitor-backend/
├── app.py                  # Flask server + Gemini + Supabase logger
├── .env                    # API keys and URLs
├── requirements.txt        # Python dependencies
└── venv/                   # Python virtual environment

copilot-monitor/
├── src/
│   └── extension.ts        # Main logic of the VS Code extension
├── esbuild.js              # Build tool for bundling extension
├── package.json            # VS Code extension config + dependencies
└── out/                    # Compiled output
🔧 Setup Instructions
1. Backend (Flask + Gemini + Supabase)
bash
Copy
Edit
cd copilot-monitor-backend
python -m venv venv
.\venv\Scripts\activate     # For Windows
pip install -r requirements.txt
Create a .env file:

ini
Copy
Edit
GOOGLE_API_KEY=your_gemini_key
SUPABASE_CME_URL=https://your-project.supabase.co
SUPABASE_CME_KEY=your_supabase_anon_key
Then run:

bash
Copy
Edit
python app.py
It should run on:
➡️ http://127.0.0.1:5000/score

2. Frontend (VS Code Extension)
bash
Copy
Edit
cd copilot-monitor
npm install
npm run compile
Then press F5 in VS Code to open the Extension Development Host.

🧪 How It Works
You start typing in a .py, .js, etc. file.

AI (e.g., Copilot) gives a suggestion.

Extension sends { prompt, suggestion, lang, file_path } to the Flask backend.

Flask uses Gemini to rate it (1–10).

Response is shown in a VS Code popup.

Data is logged to Supabase.

🛠 Example CURL Test
bash
Copy
Edit
curl -X POST http://127.0.0.1:5000/score \
  -H "Content-Type: application/json" \
  -d "{\"prompt\":\"def rev(\", \"suggestion\":\"def rev(s): return s[::-1]\", \"lang\":\"python\", \"file_path\":\"test.py\"}"
Expected response:

json
Copy
Edit
{ "score": 9 }
📊 Supabase Table Schema (prompt_log)
Field	Type
prompt	text
suggestion	text
score	integer
lang	text
file_path	text
accepted	boolean
created_at	timestamp

🚦 Roadmap
✅ AI scoring backend with Gemini

✅ VS Code extension + popup

🔄 Live testing and reliability fixes

🔜 Retry logic, error handling

🔜 Dashboard (React/Streamlit)

🔮 Feedback-based model tuning

⚠️ Disclaimer
This is a local dev project for experimentation. Do not use the development Flask server or store sensitive data in Supabase without securing your keys.

🙌 Credits
Built using:

Google Generative AI

Supabase

VS Code Extension API

TypeScript

Flask

