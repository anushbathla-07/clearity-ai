# clearity-ai

A minimal full-automation image enhancement website.

## What it does
- Upload any image from the browser.
- Applies non-generative enhancement to preserve face/identity details.
- Upscales to 4K long side when input is smaller.
- Returns an enhanced high-quality JPEG.

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000` and upload an image.

## Test
```bash
python -m unittest tests/test_enhancer.py
```
