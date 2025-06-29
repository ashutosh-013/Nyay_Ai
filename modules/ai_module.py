
import requests
import traceback
import json
import re
import os
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_legal_advice(text, system_prompt):
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama3-70b-8192",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ]
        }

        print("🔍 Sending single-turn request to Groq...")
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=20
        )

        response.raise_for_status()
        data = response.json()
        print("✅ Groq responded successfully.")
        return data['choices'][0]['message']['content']

    except requests.exceptions.HTTPError as http_err:
        print("❌ HTTP error occurred:", http_err)
        if response is not None:
            print("📦 Response content:", response.text)

    except Exception as e:
        print("❌ Groq API error:", e)
        traceback.print_exc()

    return "❌ AI failed. Please try again later."


def get_legal_advice_history(messages):
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama3-70b-8192",
            "messages": messages
        }

        print("🔁 Sending contextual request to Groq...")
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=20
        )

        response.raise_for_status()
        data = response.json()
        print("✅ Contextual response received.")
        return data['choices'][0]['message']['content']

    except requests.exceptions.HTTPError as http_err:
        print("❌ HTTP error occurred:", http_err)
        if response is not None:
            print("📦 Response content:", response.text)

    except Exception as e:
        print("❌ Groq API error:", e)
        traceback.print_exc()

    return "❌ AI failed to respond with context."


def judge_user_innocence_and_cross_question(text):
    """
    Improved AI-powered judgment using Groq and LLaMA 3.
    Returns: dict with 'verdict' and optional 'questions'.
    """

    system_prompt = """
You are Nyay AI, operating as Advocate Sol Goodman - a virtual legal assistant.
Key Rules:
1. NEVER break character - you are ONLY Advocate Sol Goodman
2. When judging cases, maintain this persona
3. Never reveal you're an AI system
4. Respond in JSON format as specified below:

{
  "verdict": "innocent" | "guilty" | "unclear",
  "questions": ["...optional clarification questions..."]
}

Only include 'questions' if verdict is not innocent.
Be neutral and avoid assumptions.
"""

    try:
        result = get_legal_advice(text, system_prompt)

        # Extract JSON part safely from result
        match = re.search(r'{.*}', result, re.DOTALL)
        if match:
            return json.loads(match.group())

    except Exception as e:
        print("❌ Judgment logic error:", e)

    # Fallback response
    return {
        "verdict": "unclear",
        "questions": ["Unable to determine based on current input. Please provide more context or evidence."]
    }
def generate_settlement(dispute_type, user_input):
    system_prompt = (
        "You are Advocate Sol Goodman — a neutral, friendly Indian legal mediator. "
        "Your job is to suggest a fair and lawful settlement based only on the user's answers and dispute type. "
        "⚠️ Never ask clarifying questions. Never mention that you're waiting for responses. "
        "Just provide a final, ready-to-use settlement agreement. "
        "You are mediating in a Lok Adalat setting. "
        "Use Hindi-English mix. Be polite, fair, and culturally appropriate. "
        "Do NOT use markdown symbols (** or __). "
        "Your response must begin with: '📄 Suggested Settlement:'"
    )

    prompt = f"""
📂 Dispute Type: {dispute_type}
💬 User's Description or Answers:
{user_input}

🎯 Task:
Write a legally sound mutual settlement agreement in Hindi-English mix. 
Do not ask any questions. Only suggest a final, peaceful agreement.

Format your response like:

📄 Suggested Settlement:
[Agreement starts here...]
"""

    return get_legal_advice(prompt, system_prompt)

