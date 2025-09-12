# bloom_pipeline
# 🌸 Bloom & Co. Pre-Launch Pipeline (Python 3.12)

**Goal:** Build a pre-launch AI-driven pipeline for **Bloom & Co.**, a luxury beauty brand, to analyze competitor reviews, pre-launch surveys, and industry/retailer reports.  
The pipeline outputs **pain points, differentiators, ROI simulations, and dashboards** that guide Bloom’s launch strategy.

---

## 🚀 Features

- **Data Ingestion**
  - Scrape competitor reviews (Sephora, Ulta, Amazon, Reddit, TikTok comments).
  - Import Bloom’s own survey results.
  - Ingest structured insights from McKinsey/Nielsen/Sephora trend reports.

- **Processing**
  - Clean & deduplicate text.
  - Extract undertone/oxidation keywords.
  - Generate embeddings + sentiment.

- **Agents (5)**
  1) **Ingestion Agent** → pulls reviews, surveys, reports into DB  
  2) **Cleaning Agent** → normalizes text, dedups, extracts keywords  
  3) **Clustering Agent** → groups reviews into pain-point clusters  
  4) **Gap-Finder Agent** → turns clusters into Bloom differentiators (Impact vs Effort)  
  5) **ROI Agent** → simulates pricing/profit scenarios (DTC vs retail)  
  *(Optional)* **Decision Log Agent** → records weekly recommendations

- **Outputs**
  - **Streamlit Dashboard** (Pain Points, ROI, Influencers, Shade Quiz).
  - **Weekly Report (PDF)** (Top pain points, differentiators, ROI summary).

---

## 🛠 Tech Stack

- **Python 3.12**
- **Postgres 15/16 + pgvector** (embeddings, analytics views)
- **Poetry** (dependency mgmt)
- **Streamlit** (dashboard)
- **pandas · scikit-learn · sentence-transformers · spaCy** (NLP, clustering)
- **HuggingFace Transformers** (sentiment)
- **SQLAlchemy + psycopg2** (DB)
- **pytest · pre-commit (black, isort, flake8)** (quality)
- **Docker Compose** (Postgres service)


---

## 📂 Repo Structure

bloom-pipeline/
├── README.md                  # Project overview + setup instructions
├── pyproject.toml              # Poetry dependency file (Python 3.12)
├── poetry.lock                 # Auto-generated lockfile
├── .gitignore                  # Ignore .env, __pycache__, data dumps, etc.
├── .env.example                # Template for secrets (DB creds, API keys)
├── Makefile                    # Dev shortcuts (up, down, fmt, lint, test, init-sql)
├── docker-compose.yml          # Postgres + pgvector service
│
├── ingestion/                  # Raw data ingestion
│   ├── scrape_competitors.py   # Scraper for Sephora/Ulta reviews
│   ├── load_surveys.py         # Import survey CSV → DB
│   └── ingest_reports.py       # Parse McKinsey/Sephora reports (manual → structured)
│
├── processing/                 # Data cleaning + prep
│   ├── clean_reviews.py        # Normalize + dedup reviews
│   ├── embed_reviews.py        # Generate embeddings
│   └── extract_keywords.py     # Undertone/oxidation keyword tagging
│
├── agents/                     # AI agents (one file per "role")
│   ├── ingestion_agent.py      # Pulls reviews/surveys/reports into DB
│   ├── cleaning_agent.py       # Runs cleaning pipeline
│   ├── clustering_agent.py     # Groups reviews → clusters
│   ├── gap_finder_agent.py     # Turns clusters → differentiators
│   ├── roi_agent.py            # Pricing/profitability simulator
│   └── decision_log_agent.py   # Records recommendations (optional extension)
│
├── nlp/                        # NLP & LLM helpers
│   ├── sentiment.py            # Sentiment classifier (HuggingFace)
│   └── summarize_cluster.py    # Cluster labeling (LLM/heuristics)
│
├── dashboard/                  # Founder-facing Streamlit UI
│   └── app.py                  # Tabs: Pain Points, ROI, Influencers, Shade Quiz
│
├── reports/                    # Generated outputs
│   ├── weekly_report.py        # Markdown → PDF report
│   └── templates/              # Report templates
│
├── sql/                        # DB migrations + views
│   ├── 001_init.sql            # Schemas bloom_raw/core/analytics
│   ├── 010_reviews.sql         # Raw + clean reviews tables
│   ├── 020_clusters.sql        # Clusters + assignments
│   ├── 030_actions.sql         # Differentiator actions
│   ├── 040_roi.sql             # ROI inputs + outputs
│   └── refresh_all.sql         # Refresh all mats/views in order
│
├── utils/                      # Shared utilities
│   ├── db.py                   # DB connector (SQLAlchemy/psycopg2)
│   ├── config.py               # Loads .env vars
│   └── logging.py              # Standard logging
│
└── tests/                      # Unit + integration tests
    ├── test_cleaning.py
    ├── test_clustering.py
    ├── test_roi.py
    └── test_end_to_end.py


---

Apple Silicon tip (if you hit torch/transformers wheels issues):
After poetry install, run:
poetry run pip install --extra-index-url https://download.pytorch.org/whl/cpu torch torchvision torchaudio
(CPU-only is fine for this project.)

## ⚙️ Setup (Python 3.12)

### 1) Clone
```bash
git clone https://github.com/<your-username>/bloom-pipeline.git
cd bloom-pipeline
```

### 2) Python and Poetry
# install Python 3.12.x (pick latest 3.12)
pyenv install 3.12.5
pyenv local 3.12.5

# Poetry
pip install --upgrade pip
pip install poetry

# install deps from pyproject.toml
poetry install

# install Python 3.12.x (pick latest 3.12)
pyenv install 3.12.5
pyenv local 3.12.5

# Poetry
pip install --upgrade pip
pip install poetry

# install deps from pyproject.toml
poetry install

### 3) Database and Docker
docker compose up -d

### 4) Initialize Schemas
make init-sql

### 5) Environment
Copy .env.example → .env and fill:
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bloom
DB_USER=bloom
DB_PASSWORD=bloom
OPENAI_API_KEY=

### 6) Run Dashboard
poetry run streamlit run dashboard/app.py

✅ Development Workflow
You (Lead / Python)
ingestion/ (scrapers, survey loader, report parser)
processing/ (clean, embed, keywords)
agents/ (clustering, gap-finder, roi, decision-log)
dashboard/ (Streamlit)
Brother (SQL / Data)
sql/ (schemas, tables, materialized views, refresh scripts)
QA queries, performance indexing, docs in sql/README.md

🧪 QA Gates (what “good” looks like)
Ingestion: expected row counts; timestamps sane; duplicates < 10%
Cleaning: no NULL critical fields; language mix reasonable; keyword hits exist
Clustering: no single cluster > 40% of docs; few tiny “noise” clusters; sample 5 docs/cluster look coherent
ROI: assert msrp > cogs; break-even formula matches calculator; scenarios ($30/$35/$40) make sense
End-to-end: one command regenerates clusters/actions/ROI and dashboard reflects new data

📊 What the Founder Gets
Dashboard tabs
Pain Point Radar (themes from competitor reviews/forums)
ROI Simulator (DTC vs retail, price points)
Influencer Shortlist (stubbed now, API later)
Shade Quiz MVP (pre-launch survey responses)
Weekly PDF Report
Top 10 pain points (with quotes)
Bloom differentiators (Impact vs Effort)
ROI scenario summary
Decision log (recommendations + rationale)
🌩️ Scaling (only when needed)
Local-first is enough now (tens of thousands of reviews < ~500MB text + embeddings).
When to move to cloud: many collaborators, always-on dashboard, >1M rows, sensitive customer data.
Lightweight cloud path: Postgres → AWS RDS/Cloud SQL; Streamlit in a small container (ECS/Fargate/Render/Heroku); reports in S3/GCS; basic OAuth.



