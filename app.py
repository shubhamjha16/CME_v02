from flask import Flask, request, jsonify
import google.generativeai as genai
import os
import time # Added for retry delay
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

# Retry parameters
MAX_GEMINI_RETRIES = 3
GEMINI_RETRY_DELAY_SECONDS = 2
MAX_SUPABASE_RETRIES = 3
SUPABASE_RETRY_DELAY_SECONDS = 2

# Scoring function
def score_prompt(prompt, suggestion):
    model = genai.GenerativeModel('gemini-1.5-flash')
    attempts = 0
    while attempts < MAX_GEMINI_RETRIES:
        try:
            response = model.generate_content(
                f"Rate the code suggestion from 1 to 10 for correctness, style, and relevance.\n\nPrompt:\n{prompt}\n\nSuggestion:\n{suggestion}"
            )
            print("🔍 Gemini raw response:", response.text)
            content = response.text.strip()
            # Extract the first number found as score
            score_str = ''.join(filter(str.isdigit, content.split('.')[0].split(',')[0].split(' ')[0]))
            if score_str:
                score = int(score_str)
                return min(score, 10) # Ensure score is not > 10
            else: # Handle cases where no digit is found in the expected part
                print(f"⚠️ Gemini response did not yield a clear score number from: {content.split('.')[0]}")
                # Attempt to find any number in the response as a fallback
                all_digits_in_response = ''.join(filter(str.isdigit, content))
                if all_digits_in_response:
                    score = int(all_digits_in_response[0:2]) # take first two digits if many
                    print(f"⚠️ Fallback score extraction: {score} from {all_digits_in_response}")
                    return min(score,10)
                else:
                    print("⚠️ No digits found anywhere in Gemini response for scoring.")
                    return 0


        except Exception as e:
            attempts += 1
            print(f"❌ Gemini scoring error (Attempt {attempts}/{MAX_GEMINI_RETRIES}): {e}")
            if attempts < MAX_GEMINI_RETRIES:
                print(f"Retrying in {GEMINI_RETRY_DELAY_SECONDS} seconds...")
                time.sleep(GEMINI_RETRY_DELAY_SECONDS)
            else:
                print("Max retries reached for Gemini scoring.")
                return 0
    return 0 # Should be unreachable if loop logic is correct, but as a safeguard

# API endpoint
@app.route('/score', methods=['POST'])
def score():
    print(f"[APP] Received request for /score")
    try:
        data = request.json
        print(f"[APP] Request data: {data}")
    except Exception as e:
        print(f"[APP] Error getting JSON data: {e}")
        return jsonify({'error': 'Invalid JSON data'}), 400

    prompt = data.get('prompt', '')
    suggestion = data.get('suggestion', '')
    lang = data.get('lang', '')
    file_path = data.get('file_path', '')

    print(f"[APP] Processing: prompt='{prompt[:50]}...', suggestion='{suggestion[:50]}...', lang='{lang}', file_path='{file_path}'")

    current_score = score_prompt(prompt, suggestion)
    print(f"[APP] Score calculated: {current_score}")

    # Log to Supabase with retry
    supabase_attempts = 0
    while supabase_attempts < MAX_SUPABASE_RETRIES:
        try:
            print(f"[APP] Attempting to log to Supabase (Attempt {supabase_attempts + 1}/{MAX_SUPABASE_RETRIES})...")
            supabase.table("prompt_log").insert({
                "prompt": prompt,
                "suggestion": suggestion,
                "score": current_score,
                "lang": lang,
                "file_path": file_path,
                "accepted": current_score >= 6,
                "created_at": datetime.utcnow().isoformat()
            }).execute()
            print("[APP] Successfully logged to Supabase.")
            break # Exit loop on success
        except Exception as e:
            supabase_attempts += 1
            print(f"❌ Supabase logging error (Attempt {supabase_attempts}/{MAX_SUPABASE_RETRIES}): {e}")
            if supabase_attempts < MAX_SUPABASE_RETRIES:
                print(f"Retrying Supabase log in {SUPABASE_RETRY_DELAY_SECONDS} seconds...")
                time.sleep(SUPABASE_RETRY_DELAY_SECONDS)
            else:
                print("[APP] Max retries reached for Supabase logging. Data for this request may not be saved.")

    print(f"[APP] Returning score: {current_score}")
    return jsonify({'score': current_score})

if __name__ == '__main__':
    app.run(debug=True)