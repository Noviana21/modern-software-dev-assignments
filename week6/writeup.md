# Week 6 Writeup: Scan and Fix Vulnerabilities with Semgrep

## 1. Brief Findings Overview
I ran the Semgrep static analysis tool against the `week6/` directory. 
- **Categories Reported:** The scan surfaced 6 blocking issues primarily falling under SAST and Code Injection categories. Common findings included overly permissive CORS configurations, SQL Injection via f-strings, XSS vulnerabilities using `innerHTML`, and dangerous system executions like `eval()` and `subprocess` with `shell=True`.
- **False Positives/Noisy Rules:** I focused on remediating the highest impact vulnerabilities (CORS, SQLi, and XSS) that directly affect web security. Some generic warnings regarding local testing teardowns were ignored as they are isolated from production logic.

## 2. Three Fixes (Before -> After)

### Fix 1: Insecure CORS Configuration
* **File and line(s):** `backend/app/main.py`, line 24
* **Rule/category Semgrep flagged:** `python.fastapi.security.wildcard-cors.wildcard-cors`
* **Brief risk description:** The application allowed cross-origin requests from any domain using the wildcard `*`. This is insecure and could lead to unauthorized API access or CSRF attacks.
* **Your change:** I prompted Copilot to restrict the origins to specific development endpoints.
  * *Before:* `allow_origins=["*"]`
  * *After:* `allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"]`
* **Why this mitigates the issue:** By explicitly defining trusted origins, the browser will block malicious external sites from reading the API responses, adhering to the principle of least privilege.

### Fix 2: SQL Injection Vulnerability
* **File and line(s):** `backend/app/routers/notes.py`, lines 71-79
* **Rule/category Semgrep flagged:** `python.sqlalchemy.security.audit.avoid-sqlalchemy-text`
* **Brief risk description:** A database query was constructed using Python `f-strings`, allowing raw user input to directly alter the SQL logic.
* **Your change:** I prompted Copilot to rewrite the raw SQL query to use SQLAlchemy's parameterized execution.
  * *Before:* `WHERE title LIKE '%{q}%' OR content LIKE '%{q}%'` (inside an f-string)
  * *After:* `WHERE title LIKE :search_query OR content LIKE :search_query` (passing `{"search_query": f"%{q}%"}` into the execution parameters).
* **Why this mitigates the issue:** Parameterization ensures the database treats the user input strictly as a literal text value, not as executable SQL logic, neutralizing injection attacks.

### Fix 3: Cross-Site Scripting (XSS)
* **File and line(s):** `frontend/app.js`, line 14
* **Rule/category Semgrep flagged:** `javascript.browser.security.insecure-document-method`
* **Brief risk description:** The frontend used `innerHTML` to render note data. If a user inputted malicious JavaScript tags, it would be executed in the victim's browser.
* **Your change:** I prompted Copilot to safely create DOM elements using `textContent`.
  * *Before:* `li.innerHTML = "<strong>" + n.title + "</strong>: " + n.content;`
  * *After:* Used `document.createElement('strong')`, assigned `n.title` to its `textContent`, and appended it to the `li` element alongside the content text node.
* **Why this mitigates the issue:** `textContent` explicitly tells the browser to treat the input as raw text. Any HTML tags or script tags inputted by a user will be printed literally on the screen rather than being executed by the browser engine.