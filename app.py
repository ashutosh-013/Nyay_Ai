from flask import Flask, render_template, request, jsonify, session
import os
import re
import uuid
import logging
from werkzeug.utils import secure_filename
from datetime import timedelta
from modules.ocr_module import extract_text_from_pdf, extract_text_from_image
from modules.ai_module import get_legal_advice_history, judge_user_innocence_and_cross_question, generate_settlement
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "nyay-secret-key"
app.permanent_session_lifetime = timedelta(minutes=30)

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/mediate", methods=["POST"])
def mediate():
    dispute_type = request.form.get("dispute_type")
    user_input = request.form.get("user_input")

    result = generate_settlement(dispute_type, user_input)

    # ✅ Return only the AI-generated HTML content (for frontend to inject)
    return f"""
    <strong>📄 Suggested Settlement:</strong><br><br>{result.replace('\n', '<br>')}
    """

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")

    try:
        user_text = request.form.get("query", "").strip()
        language = request.form.get("language", "en")
        extracted_text = ""

        abuse_keywords = ["kill", "rape", "terrorist", "bomb", "attack", "hate", "abuse"]
        if any(word in user_text.lower() for word in abuse_keywords):
            return jsonify({"error": "❌ Inappropriate or harmful content detected."}), 400

        user_text = re.sub(r"[<>\"';]", "", user_text)

        if 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                unique_filename = f"{uuid.uuid4()}_{secure_filename(file.filename)}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(filepath)

                ext = unique_filename.rsplit('.', 1)[1].lower()
                try:
                    if ext == 'pdf':
                        extracted_text = extract_text_from_pdf(filepath)
                    else:
                        extracted_text = extract_text_from_image(filepath)
                except Exception as e:
                    logging.error(f"OCR failed: {e}")
                    return jsonify({"error": "❌ Could not read file content."}), 400
            else:
                return jsonify({"error": "❌ Unsupported file type."}), 400

        combined_input = extracted_text + "\n\nUser query:\n" + user_text if user_text and extracted_text else extracted_text or user_text

        if not combined_input.strip():
            return jsonify({"error": "❌ No valid input provided."}), 400

        session.permanent = True
        if 'chat_history' not in session:
            session['chat_history'] = []

        cross_q_result = judge_user_innocence_and_cross_question(combined_input)
        if cross_q_result.get("verdict") == "guilty":
            guilty_msg_en = "⚠️ Based on your inputs and documents, Nyay AI detects contradictions or signs of guilt. We support only truthful and innocent individuals. Please consult a human lawyer."
            guilty_msg_hi = "⚠️ आपके इनपुट और दस्तावेजों के आधार पर, Nyay AI में विरोधाभास या दोष के संकेत पाए गए हैं। हम केवल सच्चे और निर्दोष व्यक्तियों का समर्थन करते हैं। कृपया किसी मानव वकील से परामर्श करें।"
            return jsonify({"answer": guilty_msg_hi if language == "hi" else guilty_msg_en})

        lang_instruction = "आपका उत्तर हिंदी में दें।" if language == "hi" else "Please respond in English."

        system_prompt = (
            lang_instruction + " "
            "IMPORTANT: You MUST identify as 'Advocate Sol Goodman' at all times. "
            "Never use any other name , ONLY 'Advocate Sol Goodman'. "
            "If the user calls you anything else, politely correct them. "
            "You are a virtual legal assistant specializing in Indian law. "
            "Your responses should be professional, compassionate, and culturally appropriate. "
            "Format reminders:\n"
            "- Never use markdown (**, _ etc.)\n"
            "- Never reveal you're an AI unless asked directly\n"
            "- Always maintain your persona\n"
            "Example correct introduction:\n"
            "'Hello, I am Advocate Sol Goodman. How can I assist you with your legal matter today?'"
        )

        messages = [{"role": "system", "content": system_prompt}]
        for turn in session['chat_history'][-4:]:
            messages.append({"role": "user", "content": turn["user"]})
            messages.append({"role": "assistant", "content": turn["ai"]})
        messages.append({"role": "user", "content": combined_input})

        answer = get_legal_advice_history(messages)
        if not answer or answer.strip() == "":
            raise ValueError("Empty AI response")

        session['chat_history'].append({"user": combined_input, "ai": answer})
        logging.info(f"AI response generated: {answer[:200]}...")

        return jsonify({"answer": answer})

    except Exception as e:
        logging.error(f"AI error: {e}")
        return jsonify({"error": "❌ Could not get advice. Please try again later."}), 500

if __name__ == "__main__":
    app.run(debug=True)
@app.route("/healthz")
def health():
    return "OK", 200
