from flask import Flask, render_template,request, jsonify
from analyzer import analyze_text
app=Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html")  ##we will return the index.html

@app.route("/analyze",methods=["POST"])
def analyze():
    data=request.get_json()

    if not data or "text" not in data:
        return jsonify({
            "error": "Sorry, no text provided"
        }),400

    text = data["text"]

    if not isinstance(text, str) or not text.strip():
        return jsonify({
            "error": "Please enter some text to analyze"
        }),400

    result=analyze_text(text)

    return jsonify(result)

if __name__== "__main__":
    app.run(debug=True)