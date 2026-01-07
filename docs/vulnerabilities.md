\# Identified Vulnerabilities



\## 1. SQL Injection

\- Location: login function

\- Cause: Dynamic SQL query without parameter binding

\- Impact: Authentication bypass



\## 2. Cross-Site Scripting (XSS)

\- Location: search endpoint

\- Cause: Unsanitized user input rendered to HTML

\- Impact: Client-side script execution



\## 3. Hardcoded Secret

\- Location: app.py

\- Cause: Sensitive information stored directly in source code

\- Impact: Secret exposure risk



