from flask import Flask, render_template, request, jsonify
import json
import requests
from datetime import datetime

app = Flask(__name__)

API_KEY = "HERE YOUR GEMINI API KEY"
GEMINI_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

def load_json():
    with open("main.json", "r", encoding="utf-8") as f:
        return json.load(f)

def generate_advice(data, lang="ar"):
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M")

    if lang == "fr":
        title = f"<b>🔔 Conseil pour le {date_str} à {time_str}</b>"
        prompt = (
            "Tu es un assistant intelligent qui analyse la consommation d'eau horaire à partir d'un fichier JSON.\n"
            "Donne un seul conseil par jour en français pour aider l'utilisateur à réduire ou améliorer sa consommation.\n"
            "Le conseil doit être clair, bref et structuré avec des puces (•).\n"
            "Explique si une consommation excessive est détectée.\n\n"
            f"Données:\n{json.dumps(data, indent=2, ensure_ascii=False)}"
        )
    else:
        title = f"<b>🔔 النصيحة ليوم {date_str} الساعة {time_str}</b>"
        prompt = (
            "أنت مساعد ذكي تحلل استهلاك المياه من ملف JSON يحتوي على بيانات لكل ساعة.\n"
            "قم بتقديم نصيحة واحدة فقط، باللغة العربية، لمساعدة المستخدم في تقليل أو تحسين استهلاكه.\n"
            "يجب أن تكون النصيحة منسقة هكذا:\n"
            "• استخدم النقاط\n• اجعل النص مختصرًا وواضحًا\n• اشرح أي تجاوز في الاستهلاك\n\n"
            f"البيانات:\n{json.dumps(data, indent=2, ensure_ascii=False)}"
        )

    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    response = requests.post(GEMINI_ENDPOINT, headers=headers, json=payload)
    result = response.json()

    try:
        advice_text = result["candidates"][0]["content"]["parts"][0]["text"]
        formatted = f"{title}<br><br>" + advice_text.replace("•", "🔹").replace("\n", "<br>")
        return formatted
    except Exception:
        return f"❌ Error request <br><br><pre>{json.dumps(result, indent=2, ensure_ascii=False)}</pre>"

@app.route("/")
def home():
    return render_template("chat.html")

@app.route("/get_advice")
def get_advice():
    lang = request.args.get("lang", "ar") 
    data = load_json()
    advice = generate_advice(data, lang=lang)
    return jsonify({"advice": advice})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5005)

