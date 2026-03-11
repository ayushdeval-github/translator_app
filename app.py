from flask import Flask, render_template, request, jsonify
from deep_translator import GoogleTranslator
import time

app = Flask(__name__)

LANGUAGES = {
    "en": "English", "hi": "Hindi", "fr": "French", "de": "German",
    "es": "Spanish", "zh-CN": "Chinese", "ar": "Arabic", "ru": "Russian",
    "it": "Italian", "pt": "Portuguese", "nl": "Dutch", "tr": "Turkish",
    "ja": "Japanese", "ko": "Korean", "bn": "Bengali", "ur": "Urdu",
    "pa": "Punjabi", "gu": "Gujarati", "ta": "Tamil", "te": "Telugu",
}

# Build all valid pairs (Google supports all combos)
PAIRS = [
    {"src": s, "tgt": t}
    for s in LANGUAGES
    for t in LANGUAGES
    if s != t
]

def translate(text: str, src: str, tgt: str) -> str:
    if src == tgt:
        return text
    translator = GoogleTranslator(source=src, target=tgt)
    return translator.translate(text)


@app.route("/")
def home():
    # Show a curated list of pairs in the UI chips
    curated = [
        {"src": "en", "tgt": "hi"}, {"src": "en", "tgt": "fr"},
        {"src": "en", "tgt": "de"}, {"src": "en", "tgt": "es"},
        {"src": "en", "tgt": "zh-CN"}, {"src": "en", "tgt": "ar"},
        {"src": "en", "tgt": "ru"}, {"src": "en", "tgt": "ja"},
        {"src": "en", "tgt": "ko"}, {"src": "en", "tgt": "it"},
        {"src": "en", "tgt": "pt"}, {"src": "en", "tgt": "bn"},
        {"src": "en", "tgt": "ur"}, {"src": "en", "tgt": "pa"},
        {"src": "en", "tgt": "gu"}, {"src": "en", "tgt": "ta"},
        {"src": "en", "tgt": "te"}, {"src": "hi", "tgt": "en"},
        {"src": "fr", "tgt": "en"}, {"src": "de", "tgt": "en"},
        {"src": "es", "tgt": "en"}, {"src": "ar", "tgt": "en"},
    ]
    return render_template("index.html", languages=LANGUAGES, pairs=curated)


@app.route("/translate", methods=["POST"])
def translate_api():
    body = request.get_json(silent=True) or {}
    text = (body.get("text") or "").strip()
    src  = body.get("src_lang", "en")
    tgt  = body.get("tgt_lang", "hi")

    if not text:
        return jsonify(error="Please enter some text."), 400
    if src not in LANGUAGES or tgt not in LANGUAGES:
        return jsonify(error="Unsupported language selected."), 400

    try:
        t0 = time.time()
        result = translate(text, src, tgt)
        elapsed = round(time.time() - t0, 2)
        return jsonify(translated_text=result, elapsed=elapsed)
    except Exception as e:
        return jsonify(error=f"Translation failed: {str(e)}"), 500


if __name__ == "__main__":
    app.run(debug=True)