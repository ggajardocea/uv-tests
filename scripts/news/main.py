from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import requests
from transformers import pipeline
from diffusers import StableDiffusionPipeline
import torch
import os
import uvicorn
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()

# ---------- CONFIG ----------
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
HF_TOKEN = os.environ.get("HF_TOKEN")
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# ---------- APP ----------
app = FastAPI(title="AI Multimodal News Companion MVP")

# ---------- MODELS ----------
# Summarizer
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=0 if DEVICE=="cuda" else -1)

HF_TTS_URL = "https://api-inference.huggingface.co/models/espnet/kan-bayashi_ljspeech"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def generate_audio(text: str, filename: str) -> str:
    """Call Hugging Face API for TTS"""
    response = requests.post(HF_TTS_URL, headers=headers, json={"inputs": text})
    if response.status_code != 200:
        raise Exception(f"Hugging Face TTS Error: {response.text}")

    os.makedirs("static/audio", exist_ok=True)
    path = f"static/audio/{filename}.wav"
    with open(path, "wb") as f:
        f.write(response.content)
    logger.info(f"Audio saved to: {path}")
    return path

# Text-to-Image
sd_pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
sd_pipe.to(DEVICE)

def generate_image(prompt: str, filename: str) -> str:
    """Generate a thumbnail image"""
    os.makedirs("static/images", exist_ok=True)
    image = sd_pipe(prompt).images[0]
    path = f"static/images/{filename}.png"
    image.save(path)
    logger.info(f"Image saved to: {path}")
    return path

# ---------- SCHEMAS ----------
class BriefingResponse(BaseModel):
    title: str
    summary: str
    #audio_path: str
    image_path: str

# ---------- HELPERS ----------
def fetch_news(topic: str = "technology", n_articles: int = 1):
    """Fetch news articles from NewsAPI"""
    url = f"https://newsapi.org/v2/everything?q={topic}&pageSize={n_articles}&apiKey={NEWS_API_KEY}"
    r = requests.get(url)
    data = r.json()
    if "articles" not in data:
        logger.info(f"No articles found for topic: {topic}")
        return []
    return data["articles"]

def generate_summary(text: str) -> str:
    """Summarize long text into a short digest"""
    result = summarizer(text, max_length=80, min_length=30, do_sample=False)
    logger.info(f"Summary: {result[0]['summary_text']}")
    return result[0]["summary_text"]

# ---------- ROUTES ----------
@app.get("/briefing", response_model=List[BriefingResponse])
def get_briefing(topic: Optional[str] = "technology"):
    """End-to-end pipeline: fetch news → summarize → TTS → image"""
    articles = fetch_news(topic, n_articles=2)
    results = []

    for i, article in enumerate(articles):
        logger.info(f"Processing article {i+1} of {len(articles)}: {article['title']}")
        title = article["title"]
        text = article.get("content") or article.get("description") or title

        summary = generate_summary(text)
        #audio_path = generate_audio(summary, f"{topic}_{i}")
        image_path = generate_image(title, f"{topic}_{i}")

        results.append(BriefingResponse(
            title=title,
            summary=summary,
            #audio_path=audio_path,
            image_path=image_path
        ))

    return results

@app.get("/")
def read_root():
    return {"msg": "Hello FastAPI"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)