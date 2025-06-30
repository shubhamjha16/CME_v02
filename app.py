from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Supabase if using it (optional for now)
SUPABASE_URL = os.getenv("SUPABASE_CME_URL")
SUPABASE_KEY = os.getenv("SUPABASE_CME_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Scoring function
def score_prompt(prompt, suggestion):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(
            f"Rate the code suggestion from 1 to 10 for correctness, style, and relevance.\n\nPrompt:\n{prompt}\n\nSuggestion:\n{suggestion}"
        )
        print("🔍 Gemini raw response:", response.text)
        content = response.text.strip()
        score = int(''.join(filter(str.isdigit, content.split('.')[0])))
        return min(score, 10)
    except Exception as e:
        print("❌ Gemini scoring error:", e)
        return 0

# API endpoint
@app.route('/score', methods=['POST'])
def score():
    data = request.json
    prompt = data.get('prompt', '')
    suggestion = data.get('suggestion', '')
    lang = data.get('lang', '')
    file_path = data.get('file_path', '')

    score = score_prompt(prompt, suggestion)

    # Optional: log to Supabase
    try:
        supabase.table("prompt_log").insert({
            "prompt": prompt,
            "suggestion": suggestion,
            "score": score,
            "lang": lang,
            "file_path": file_path,
            "accepted": score >= 6,
            "created_at": datetime.utcnow().isoformat()
        }).execute()
    except Exception as e:
        print("❌ Supabase logging error:", e)

    return jsonify({'score': score})

if __name__ == '__main__':
    app.run(debug=True)