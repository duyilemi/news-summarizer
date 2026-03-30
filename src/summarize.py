import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def summarize_article(article_text, max_tokens=150):
    """Summarize a single article using Groq's Mixtral."""
    prompt = f"Summarize the following news article concisely in 2-3 sentences:\n\n{article_text}"
    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

def process_articles(raw_filepath, output_filepath=None):
    """Read raw JSON, summarize each article, save summaries."""
    with open(raw_filepath, "r") as f:
        raw_data = json.load(f)

    articles = raw_data.get("articles", [])
    summaries = []
    for article in articles:
        # Combine title and description as text to summarize
        text = f"{article.get('title', '')}. {article.get('description', '')}"
        if len(text) < 50:
            continue  # skip if too short
        summary = summarize_article(text)
        summaries.append({
            "title": article.get("title"),
            "original_text": text,
            "summary": summary,
            "url": article.get("url"),
            "published_at": article.get("publishedAt")
        })

    if output_filepath is None:
        output_filepath = f"data/processed/summaries_{raw_filepath.split('/')[-1]}"
    os.makedirs("data/processed", exist_ok=True)
    with open(output_filepath, "w") as f:
        json.dump(summaries, f, indent=2)
    return output_filepath