
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# --- Simple mock logic ---
DISEASE_KEYWORDS = {
    "yellow": "Nitrogen deficiency or leaf blight risk",
    "spots": "Leaf spot or fungal infection",
    "holes": "Pest damage likely",
    "wilt": "Water stress or bacterial wilt",
}

def mock_disease_from_text(text):
    text_l = text.lower()
    for k, v in DISEASE_KEYWORDS.items():
        if k in text_l:
            return v
    return "No clear issue detected. Monitor for changes."

def mock_disease_from_image(filename):
    # Placeholder: a real model would analyze the image.
    # Use filename hash as deterministic choice.
    h = sum(ord(c) for c in filename) % 4
    return list(DISEASE_KEYWORDS.values())[h]

def mock_irrigation_advice():
    # Very simple time based advice
    hour = datetime.datetime.now().hour
    if 5 <= hour <= 9:
        return "Good time to irrigate in the early morning to reduce evaporation."
    elif 17 <= hour <= 19:
        return "Consider evening irrigation to minimize water loss."
    else:
        return "Avoid irrigating at mid day due to high evaporation."

def mock_market_tip(crop="tomato"):
    tips = {
        "tomato": "Local prices trend higher on weekends. Consider selling on Saturday morning market.",
        "paddy": "Check local mandi arrivals on Monday for better bargaining.",
        "chilli": "Dry quality lots fetch a premium mid month."
    }
    return tips.get(crop.lower(), "Watch local market arrivals and avoid peak supply days.")
# --- End mock logic ---

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        query_text = request.form.get("query_text", "").strip()
        crop = request.form.get("crop", "tomato").strip() or "tomato"
        if "image" in request.files and request.files["image"].filename != "":
            f = request.files["image"]
            fname = secure_filename(f.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], fname)
            f.save(path)
            disease = mock_disease_from_image(fname)
            result = {
                "mode": "image",
                "disease": disease,
                "irrigation": mock_irrigation_advice(),
                "market": mock_market_tip(crop),
                "note": "Demo classification using placeholder logic, not a medical grade diagnosis."
            }
        elif query_text:
            disease = mock_disease_from_text(query_text)
            result = {
                "mode": "text",
                "disease": disease,
                "irrigation": mock_irrigation_advice(),
                "market": mock_market_tip(crop),
                "note": "Demo text analysis using keyword heuristic."
            }
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
