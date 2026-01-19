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



\\## Roadmap

\\- Week 3: Dockerize the Flask app (Dockerfile / docker-compose)

\\- Week 4: Setup GitLab CI pipeline stages (build/test/docker-build)

\\- Week 5: Integrate SonarQube (SAST), Trivy (Image Scan), OWASP ZAP (DAST)

\\- Week 6: Fix 1–2 vulnerabilities and compare before/after results








