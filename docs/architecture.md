\# DevSecOps Architecture



\## Overview

This project implements a DevSecOps model for a Web application by integrating

security testing tools into the CI/CD pipeline.



\## Architecture Flow



Developer pushes source code to GitLab repository.

Each commit triggers a GitLab CI/CD pipeline that performs:



1\. Build and test the application

2\. Static Application Security Testing (SAST) using SonarQube

3\. Container image vulnerability scanning using Trivy

4\. Dynamic Application Security Testing (DAST) using OWASP ZAP

5\. Generate security reports for evaluation



\## Tools Used

\- GitLab: Source code management

\- GitLab CI: CI/CD pipeline

\- Docker: Application containerization

\- SonarQube: SAST

\- Trivy: Image scanning

\- OWASP ZAP: DAST



