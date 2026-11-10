from flask import Flask, render_template, request, send_file
from io import BytesIO

from enhancer import enhance_image_bytes


app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/enhance")
def enhance():
    uploaded = request.files.get("image")
    if uploaded is None or uploaded.filename == "":
        return "Please upload an image.", 400

    try:
        output_bytes = enhance_image_bytes(uploaded.read())
    except ValueError as exc:
        return str(exc), 400

    return send_file(
        BytesIO(output_bytes),
        mimetype="image/jpeg",
        as_attachment=True,
        download_name="enhanced-4k.jpg",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
