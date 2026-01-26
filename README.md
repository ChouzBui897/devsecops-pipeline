\# DevSecOps Web Pipeline



\## Description

This project demonstrates a DevSecOps CI/CD pipeline for a Web application.

Security testing is integrated directly into the pipeline to detect vulnerabilities

early in the software development lifecycle.



The Web application is intentionally built with common security vulnerabilities

to serve as input for automated security testing tools (SAST/DAST/Image Scan).



---



\## Objectives

\- Build a CI/CD pipeline using GitLab CI

\- Integrate automated security testing tools

\- Detect security vulnerabilities in source code, container images, and running applications



---



\## Technologies

\- Python (Flask)

\- SQLite

\- Docker

\- GitLab (Source Control)

\- GitLab CI (CI/CD)

\- SonarQube (SAST)

\- Trivy (Image Scan)

\- OWASP ZAP (DAST)



---



\## Week 2 – Web Application (Flask) + Intentional Vulnerabilities



\### Features (Week 2)

\- Home page: `/`

\- Login: `/login`

\- Search: `/search`

\- Health check: `/health` (returns `OK`)



\### Run locally (Windows)



```powershell

cd .\\\\src\\\\app



pip install -r requirements.txt

python .\\\\scripts\\\\init\\\_db.py

python .\\\\scripts\\\\seed\\\_db.py



python .\\\\app.py



Open: http://localhost:5000  

Health: http://localhost:5000/health



\\### Demo account

\\- Username: `admin`

\\- Password: `admin123`



\\## Intentional Vulnerabilities (for DevSecOps testing)



\\### 1) SQL Injection (Login)

\\- Location: `POST /login` (app.py)

\\- PoC:

\&nbsp; - Username: `admin' OR '1'='1' --`

\&nbsp; - Password: `abc`

\\- Expected: bypass login / welcome message



\\### 2) XSS (Search)

\\- Location: `GET /search?q=...`

\\- PoC:

\&nbsp; - `http://localhost:5000/search?q=<script>alert(1)</script>`

\\- Expected: browser shows alert popup



\\### 3) Hardcoded Secret

\\- Location: `app.py` (`app.secret\\\_key = "hardcoded\\\_secret\\\_key"`)

\\- Expected: SAST (SonarQube) flags hardcoded secret


## Week 3 – Docker & Environment Standardization (Completed)
- Dockerized the Flask web application:
  - Created/updated `Dockerfile` to build a Docker image for the app
  - Switched runtime to `gunicorn` (production-like server) instead of Flask dev server
  - Exposed port `5000` and verified the app runs in a container

- Standardized local DevSecOps environment using Docker Compose:
  - Added `docker-compose.yml` to run services in one command:
    - `web` (Flask app container)
    - `sonarqube` (SAST platform, port 9000)
    - `zap` (OWASP ZAP daemon container, port 8080)
  - Verified services are accessible:
    - Web: `http://localhost:5000` (and `/health`)
    - SonarQube: `http://localhost:9000`
    - ZAP daemon: `http://localhost:8080`

### Deliverables
- `src/app/Dockerfile` (gunicorn-based)
- `src/app/requirements.txt` updated (added `gunicorn`)
- `docker-compose.yml` for local environment


## Week 4 – CI/CD with GitLab CI (Completed)
- Created/updated `.gitlab-ci.yml` with 3 stages: **build → test → docker-build**
- Pipeline triggers automatically on every `git push`
- Build stage:
  - Install dependencies from `requirements.txt`
  - Check Python syntax (`python -m py_compile app.py`)
- Test stage:
  - Run a smoke test by starting the app and calling `GET /health` (expects `OK`)
- Docker-build stage:
  - Build Docker image from `./src/app`
  - (Optional) Push image to GitLab Container Registry using `$CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA`

\\## Roadmap

\\- Week 5: Integrate SonarQube (SAST), Trivy (Image Scan), OWASP ZAP (DAST)

\\- Week 6: Fix 1–2 vulnerabilities and compare before/after results








