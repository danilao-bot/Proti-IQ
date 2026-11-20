# Proti IQ — Render Deployment Guide

This guide walks through deploying the Proti IQ FastAPI Backend and Streamlit Hub to Render (https://render.com).

---

## Architecture on Render

Proti IQ can be deployed on Render using either **Option A (Automated Blueprint)** or **Option B (Manual Web Service)**.

```
                    +---------------------------+
                    |  Edna's React Frontend    |
                    |  (Vercel / Netlify / Web) |
                    +-------------+-------------+
                                  | HTTPS REST
                                  v
+---------------------------------------------------------------+
|                      Render.com Cloud                         |
|                                                               |
|  [proti-iq-api]                                               |
|  FastAPI Service (uvicorn api.main:app --port $PORT)          |
|  - GET  /api/v1/hub/applications                              |
|  - GET  /api/v1/hub/rankings                                  |
|  - POST /api/v1/hub/advisory/formulate (Groq LLM)             |
|                                                               |
|  [proti-iq-streamlit] (Optional Science UI)                   |
|  Streamlit App (streamlit run ui/Home.py --port $PORT)        |
+-------------------------------+-------------------------------+
                                |
                                v
               +--------------------------------+
               |   Supabase Cloud PostgreSQL    |
               |   (348 Proteins, 630 Rankings) |
               +--------------------------------+
```

---

## Option A: 1-Click Blueprint Deployment (Recommended)

1. Log in to [Render Dashboard](https://dashboard.render.com).
2. Click **New +** > **Blueprint**.
3. Connect your GitHub repository: `https://github.com/danilao-bot/Proti-IQ`.
4. Render will automatically detect `render.yaml` and configure the `proti-iq-api` service.
5. In the Environment Variables section for `proti-iq-api`, add your secret keys:
   - `GROQ_API_KEY`: [YOUR-GROQ-API-KEY]
   - `SUPABASE_SERVICE_KEY`: [YOUR-SUPABASE-SERVICE-KEY]
6. Click **Apply**.
7. In ~2 minutes, your service will be live at:
   `https://proti-iq-api.onrender.com`

---

## Option B: Manual Web Service Deployment

If deploying manually without Blueprint:

1. In Render Dashboard, click **New +** > **Web Service**.
2. Select your repository: `https://github.com/danilao-bot/Proti-IQ`.
3. Configure the settings:
   - **Name:** `proti-iq-api`
   - **Language / Runtime:** `Python 3`
   - **Region:** `Frankfurt (EU Central)`
   - **Branch:** `main`
   - **Build Command:** `pip install -r requirements-render.txt`
   - **Start Command:** `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
4. Add Environment Variables under **Advanced**:
   - `PYTHON_VERSION`: `3.11.8`
   - `APP_ENV`: `production`
   - `DATABASE_URL`: `sqlite:///./data/proti_iq.db`
   - `SUPABASE_URL`: `https://dzbcefkvzufomdpfjmrw.supabase.co`
   - `SUPABASE_ANON_KEY`: `sb_publishable_cRzeE31P8Dlc9T5AZpgdIg_3GUu7E46`
   - `SUPABASE_SERVICE_KEY`: [YOUR-SUPABASE-SERVICE-KEY]
   - `GROQ_API_KEY`: [YOUR-GROQ-API-KEY]
   - `ALLOWED_ORIGINS`: `["*"]`
5. Click **Create Web Service**.

---

## Verifying Deployment

Once deployed, test the live public URL:

1. **Health Check:**
   `curl https://proti-iq-api.onrender.com/health`
   Should return: `{"status": "healthy"}`

2. **Interactive Swagger Docs:**
   Open in your browser: `https://proti-iq-api.onrender.com/docs`

3. **Edna's React Configuration:**
   Edna only needs to update her API base URL in React:
   ```javascript
   // src/services/api.js
   const API_BASE = 'https://proti-iq-api.onrender.com/api/v1/hub'
   ```
