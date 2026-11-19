# Proti IQ — Security & Threat Model

## 1. Threat Model Overview
Proti IQ is designed as a public, read-only decision-support platform.  
**Critical Assets:** Data integrity (verified answer key & sequence provenance), model artifact integrity, service availability, scientific credibility (prevention of hallucinated or falsified claims).

---

## 2. Implemented Security Controls

| Threat Vector | Mitigation Strategy | Implemented Control |
| :--- | :--- | :--- |
| **Input Tampering & Injection** | Strict Pydantic v2 schemas with `extra="forbid"`. Enums and constrained integers only. | Free-form arbitrary text never reaches the database or scoring engine. Request body capped at 16 KB. |
| **SQL Injection** | Parameterized queries via SQLAlchemy 2.0 ORM. | No raw string-interpolated SQL statements anywhere in backend. |
| **Database Privilege Escalation** | Role-based segregation. | FastAPI backend runs on a **read-only database connection**. Writing is strictly restricted to offline CLI pipeline scripts. |
| **Model & Artifact Tampering** | No untrusted pickle deserialization. | Embeddings and model weights stored in safe formats (safetensors / NumPy `.npy`). Startup routines verify SHA-256 digests against `manifest.json`. |
| **SSRF (Server-Side Request Forgery)** | Zero dynamic external queries at request time. | API does not make outbound HTTP calls during user requests. Offline ingestion only accesses an explicit allowlist (UniProt REST & AlphaFold DB API). |
| **Denial of Service (DoS)** | Precomputed inference & rate limiting. | Online `/rank` endpoint operates in $O(1)$ lookup / lightweight matrix dot-product under 300ms. Slowapi enforces 60 req/min per IP. |
| **CSV Formula Injection** | Sanitization during export. | Any exported CSV cell beginning with `=`, `+`, `-`, or `@` is prepended with a single quote (`'`). |
| **Secret Leaks** | Strict exclusion. | Zero hardcoded API keys or secrets. Pre-commit hooks and `.gitignore` guard credentials. |

---

## 3. Residual Risks & Declarations
- **Local Dev vs Multi-tenant Deployments:** For hackathon demonstration, local SQLite is deployed with filesystem permissions. Production migration targets PostgreSQL 16 with separate DB users (`proti_reader` vs `proti_writer`).
