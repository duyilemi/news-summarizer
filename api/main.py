import os
import json
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional
import subprocess
from datetime import datetime
import glob

app = FastAPI(title="News Summarizer API")

class SummaryResponse(BaseModel):
    title: str
    summary: str
    url: str
    published_at: str

def run_airflow_dag(dag_id="news_summarizer"):
    """Trigger Airflow DAG via CLI (requires airflow installed)."""
    # This assumes Airflow is installed and accessible.
    # In production, you might use Airflow REST API.
    try:
        subprocess.run(
            ["airflow", "dags", "trigger", dag_id],
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Failed to trigger DAG: {e.stderr}")

@app.post("/trigger_pipeline")
async def trigger_pipeline(background_tasks: BackgroundTasks):
    """Trigger the news summarizer DAG."""
    background_tasks.add_task(run_airflow_dag)
    return {"message": "Pipeline triggered in background"}

@app.get("/summaries", response_model=List[SummaryResponse])
async def get_summaries(limit: int = 10):
    """Return latest summaries from processed data."""
    # Find the latest processed JSON file
    files = glob.glob("data/processed/summaries_*.json")
    if not files:
        raise HTTPException(status_code=404, detail="No summaries found")
    latest = max(files, key=os.path.getctime)
    with open(latest, "r") as f:
        data = json.load(f)
    return data[:limit]

@app.get("/")
async def root():
    return {"message": "News Summarizer API", "docs": "/docs"}