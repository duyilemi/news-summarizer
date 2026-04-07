# 📰 AI News Summarizer Pipeline

An end-to-end news processing pipeline that fetches top headlines, summarizes them with an LLM (Groq), versions datasets with DVC, orchestrates workflows with Apache Airflow, serves results through a FastAPI backend, and exposes a lightweight web frontend. The entire system is containerized with Docker Compose and validated with automated tests in CI/CD.

[![CI](https://github.com/duyilemi/news-summarizer/actions/workflows/ci.yml/badge.svg)](https://github.com/duyilemi/news-summarizer/actions/workflows/ci.yml)

## Overview

This project demonstrates a production-style data pipeline that combines data ingestion, orchestration, validation, model-assisted summarization, version control for datasets, API delivery, and a frontend interface. It is designed as a portfolio-ready engineering project that highlights practical skills in data engineering, backend development, workflow orchestration, containerization, testing, and deployment.

## Key Features

* **Orchestration with Airflow** — A scheduled DAG runs daily, supports retries, and sends email alerts when failures occur.
* **LLM-based Summarization** — Uses Groq’s LLaMA 3.1 models to generate concise summaries of news articles.
* **Dataset Versioning with DVC** — Tracks raw and processed datasets using a local DVC remote.
* **FastAPI Backend** — Serves summaries and can be extended to trigger pipeline actions programmatically.
* **Lightweight Web Frontend** — A simple HTML/JavaScript interface served through nginx.
* **Data Quality Checks** — Validates titles, URLs, and dates before articles are processed.
* **Automated Testing** — Includes unit and integration-style tests for fetching, summarization, API behavior, and data validation.
* **CI/CD with GitHub Actions** — Runs the test suite on every push.
* **Fully Containerized** — Uses Docker Compose to run Airflow, PostgreSQL, Redis, FastAPI, nginx, and the frontend together.

## Tech Stack

| Area                   | Tools                                      |
| ---------------------- | ------------------------------------------ |
| Workflow orchestration | Apache Airflow 2.10 (LocalExecutor)        |
| LLM inference          | Groq API                                   |
| Backend API            | FastAPI, Uvicorn                           |
| Frontend               | HTML, CSS, JavaScript, nginx reverse proxy |
| Data versioning        | DVC with local remote                      |
| Testing                | Pytest, pytest-asyncio, pytest-cov         |
| CI/CD                  | GitHub Actions                             |
| Containerization       | Docker, Docker Compose                     |
| Language/runtime       | Python 3.12, `uv`                          |

## Architecture

```text
NewsAPI → Airflow DAG → Fetch Articles → Data Quality Checks → LLM Summarization → DVC Versioning → FastAPI → nginx → Frontend
                           ↓
                      Email Alerts on Failure
                           ↓
                    GitHub Actions CI Tests
```


## Local Setup (Recommended: Docker Compose)

### Prerequisites

* Docker
* Docker Compose
* `uv` (optional, for local development)
* API keys for:

  * [NewsAPI](https://newsapi.org/)
  * [Groq](https://console.groq.com/)

### 1) Clone the repository

```bash
git clone https://github.com/duyilemi/news-summarizer.git
cd news-summarizer
```

### 2) Configure environment variables

Create a `.env` file in the project root:

```env
NEWS_API_KEY=your_newsapi_key
GROQ_API_KEY=your_groq_api_key
```

If your Gmail SMTP credentials or other Airflow alert settings are required, add them here as well.

### 3) Build and start the services

```bash
sudo docker-compose up --build
```

### 4) Access the services

* **Frontend:** [http://localhost](http://localhost)
* **FastAPI docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
* **Airflow UI:** [http://localhost:8080](http://localhost:8080)

  * Default login : `admin / admin`

### 5) Trigger the pipeline

You can trigger the DAG from the Airflow UI by enabling `news_summarizer` and running it manually, or from the CLI:

```bash
sudo docker-compose exec airflow-scheduler airflow dags trigger news_summarizer
```

### 6) View the summaries

Open the frontend and click **Refresh Summaries**, or query the API directly:

```bash
curl http://localhost:8000/summaries
```

## Running Tests

Run the test suite locally with:

```bash
uv run pytest
```

You can also extend this with coverage reporting if needed:

```bash
uv run pytest --cov=.
```

## Docker Compose Services

| Service           | Description                                        | Ports           |
| ----------------- | -------------------------------------------------- | --------------- |
| postgres          | Airflow metadata database                          | 5432 (internal) |
| redis             | Broker for Celery-style messaging support          | 6379 (internal) |
| airflow-init      | One-time database initialization and user creation | -               |
| airflow-webserver | Airflow UI                                         | 8080            |
| airflow-scheduler | Schedules and executes tasks                       | -               |
| fastapi           | API backend                                        | 8000            |
| frontend          | nginx serving the UI and proxying API requests     | 80              |

## Monitoring and Alerts

* **Email alerts** are configured through Gmail SMTP in `docker-compose.yml`.
* **Airflow logs** are available through the Airflow UI or via:

```bash
sudo docker-compose logs airflow-scheduler
```

## Testing Strategy

The project includes tests that validate the most important parts of the system:

* `tests/test_fetch_news.py` — mocks NewsAPI calls.
* `tests/test_summarize.py` — mocks Groq API calls.
* `tests/test_api.py` — tests FastAPI endpoints.
* `tests/test_data_quality.py` — validates the filtering and checking logic.

These tests help ensure the pipeline behaves correctly even when external services are unavailable.

## Documentation Strategy


* **`README.md`** — the main project overview, setup, architecture, and usage guide.
* **`ISSUES.md`** — a chronological record of bugs, errors, and fixes i encountered during development.
* **`DECISIONS.md`** — the reasoning behind architectural choices and tool selection.


## Contributing

This project is intended as a portfolio piece, but suggestions, improvements, and issues are welcome. Feel free to open an issue or submit a pull request.

## License

MIT

## Author

**Charles Duyilemi**

GitHub: [https://github.com/duyilemi](https://github.com/duyilemi)

LinkedIn: [https://linkedin.com/in/charlesolajide/](https://linkedin.com/in/charlesolajide/)

## Acknowledgements

* [NewsAPI](https://newsapi.org/) for news data.
* [Groq](https://groq.com/) for fast LLM inference.
* [Apache Airflow](https://airflow.apache.org/) for orchestration.
* [DVC](https://dvc.org/) for dataset versioning.
* [FastAPI](https://fastapi.tiangolo.com/) for the API layer.

---
