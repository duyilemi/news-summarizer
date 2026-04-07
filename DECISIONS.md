# Architectural Decisions

## Why LocalExecutor instead of CeleryExecutor?
- Simpler setup for a single‑node development environment.
- Avoids complexity of Redis/worker management while still demonstrating containerization.

## Why DVC with local remote instead of cloud storage?
- No cost, no authentication issues.
- Can be easily changed to S3/GCS later; the concept of remote versioning is still shown.

## Why nginx reverse proxy for the frontend?
- To avoid CORS issues and provide a clean `/api/` route.
- Lightweight and fast, easy to containerize.

## Why not use `airflow.providers.standard`?
- That module does not exist in Airflow 2.x/3.x; operators are in `airflow.operators.*`.