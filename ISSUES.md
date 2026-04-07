# 🛠️ Issues & Resolutions

This document captures the real-world challenges encountered during the development of the **AI News Summarizer Pipeline** and how they were resolved. It highlights debugging skills, system design understanding, and practical experience working with containerized data systems.

---

## 1. Docker Permission Denied When Stopping Containers

**Problem**  
Running `docker-compose down` resulted in a `permission denied` error.

**Root Cause**  
The current user did not have sufficient privileges to interact with the Docker daemon.

**Solution**  
- Used `sudo` for Docker commands as an immediate workaround.
- Permanently resolved by adding the user to the Docker group:

  ```bash
  sudo usermod -aG docker $USER
  ```

- Restarted the terminal session to apply the changes.

---

## 2. Airflow Webserver Timeout (Gunicorn Master)

**Problem**  
Airflow webserver failed to start within the default timeout of 120 seconds.

**Root Cause**  
Heavy imports and initialization logic in DAG files caused slow startup of Gunicorn workers.

**Solution**  
- Increased the timeout:

  ```bash
  WEB_SERVER_WORKER_TIMEOUT=300
  ```

- Refactored DAG files to move heavy imports inside task functions (lazy loading).

---

## 3. DVC "Not a Git Repository" Error in Container

**Problem**  
Running `dvc add` failed due to a missing or improperly initialized `.dvc` directory.

**Root Cause**  
The container environment did not persist or correctly initialize DVC metadata.

**Solution**  
- Added a dedicated Airflow task to initialize DVC:

  ```bash
  rm -rf .dvc && dvc init --no-scm
  ```

- Ensured this step runs before any `dvc add` operation.

---

## 4. Groq API Key Not Detected in Airflow Tasks

**Problem**  
`groq.AuthenticationError` occurred inside Airflow containers.

**Root Cause**  
Environment variables were not properly passed to the Airflow scheduler container.

**Solution**  
- Added the variable explicitly in `docker-compose.yml`:

  ```yaml
  environment:
    - GROQ_API_KEY=${GROQ_API_KEY}
  ```

- Verified availability inside the container:

  ```bash
  env | grep GROQ
  ```

---

## 5. Frontend 404 Error on `/summaries`

**Problem**  
Requests to `/summaries` returned 404 errors.

**Root Cause**  
nginx attempted to serve the route as a static file instead of proxying it to the FastAPI backend.

**Solution**  
- Updated frontend API calls to:

  ```text
  /api/summaries
  ```

- Configured nginx reverse proxy:

  ```nginx
  location /api/ {
      proxy_pass http://fastapi:8000/;
  }
  ```

---

## 6. Permission Denied Writing to `data/` Directory

**Problem**  
The Airflow container could not write to the mounted `data/` directory.

**Root Cause**  
There was a mismatch between the container user (UID 50000) and host filesystem ownership.

**Solution**  
- Updated ownership on the host system:

  ```bash
  sudo chown -R 50000:50000 data/
  ```

- Ensured consistent permissions across environments.

---

## Key Takeaways

- Containerized environments require explicit handling of permissions and environment variables.
- Airflow performance depends heavily on DAG design, especially avoiding heavy top-level imports.
- Reverse proxy configuration is essential for correct frontend-backend communication.
- Data tools like DVC may require initialization logic in ephemeral container environments.

---

## Engineering Impact

These challenges reflect real-world production scenarios and demonstrate:

- Strong debugging and troubleshooting skills
- Understanding of distributed and containerized systems
- Ability to identify root causes, not just symptoms
- Practical experience with DevOps and data engineering workflows

This document serves as evidence of hands-on experience building and maintaining a robust data pipeline system.