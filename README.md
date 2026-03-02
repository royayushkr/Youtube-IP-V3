# Purdue YouTube Intelligence Platform

An end-to-end analytics and recommendation system that leverages public YouTube metadata and LLMs to help creators plan high-impact content strategies.

## Overview
Small-to-mid-tier creators often lack cross-channel intelligence and actionable insights. This project fills that gap by combining scalable public data collection with modern NLP and LLM-assisted recommendations to deliver channel-specific strategy guidance.

## Project Brief
The full business context, goals, scope, deliverables, and schedule live in `docs/PROJECT_BRIEF.md`.

## Solution Summary
- **Collect** public channel/video metadata and captions
- **Process** and clean data for analysis
- **Model** topics and patterns that correlate with engagement
- **Recommend** titles, topics, thumbnails, and posting strategy
- **Deliver** results via a premium, dark-mode Streamlit dashboard for stakeholders and creators

## Tech Stack
- **Python 3.10+** for data collection, processing, and modeling
- **YouTube Data API v3** for public metadata
- **BERTopic** for topic modeling and semantic patterns
- **Gemini API** for image and text generation (titles, scripts, thumbnails)
- **OpenAI API (GPT + Images)** for optional/fallback text and thumbnail generation
- **Streamlit** for interactive insights delivery with a custom dark theme

## System Architecture
See `docs/ARCHITECTURE.md` for the component map and data flow.

## Data Sources
- **YouTube Data API v3:** titles, tags, views, likes, comments, channel data
- **Public captions:** NLP inputs for semantic modeling
- **Google Trends (optional):** external signal for topic validation

## Repository Structure
```
.
├── config/                 # Project configuration
├── dashboard/              # Streamlit app and UI components
├── data/                   # Raw and processed data (gitignored)
├── docs/                   # Architecture and project brief
├── notebooks/              # Exploration, modeling, and reporting notebooks
├── outputs/                # Figures, reports, and models (gitignored)
├── src/                    # Core Python package
│   ├── data_collection/    # API clients and scrapers
│   ├── data_processing/    # Cleaning and feature engineering
│   ├── llm_integration/    # GPT-4 integration
│   ├── modeling/           # BERTopic and modeling logic
│   └── utils/              # Helpers and logging
└── tests/                  # Unit and integration tests
```

## Getting Started

### Prerequisites
- Python 3.10+
- YouTube Data API key
- Gemini API key
- OpenAI API key (optional but recommended)

### Setup (local)
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Environment Variables
Copy and edit:
```bash
cp .env.example .env
```
Then populate with your credentials (do not commit `.env`).

Required keys:
- `YOUTUBE_API_KEY` – YouTube Data API v3
- `GEMINI_API_KEY` – Gemini text + image
- `OPENAI_API_KEY` – OpenAI GPT + images (optional)

### Run the Dashboard (local)
```bash
streamlit run dashboard/app.py
```

### Run Tests
```bash
pytest
```

## Configuration
Project-level configuration lives in `config/config.yaml`. Logging is configured in `config/logging_config.yaml`.

The Streamlit UI theme is configured in:
- `.streamlit/config.toml` – dark theme colors for the entire app.

Key frontend dependencies:
- `plotly` and `altair` for interactive charts
- `streamlit-option-menu` for sidebar navigation

---

## Dashboard Overview

The main app entrypoint is `dashboard/app.py`. It exposes three primary views via the left-hand navigation:

1. **Channel Analysis**
2. **Recommendations**
3. **Ytuber (Creator Suite)**

All pages share:
- A **Purdue × Google** branded dark UI
- Glassmorphism KPI cards
- Plotly-based charts using a shared dark template

### 1. Channel Analysis

Location: `dashboard/views/channel_analysis.py`

- **Dataset selector**:
  - Research / Science
  - Tech
  - Gaming
  - Entertainment
  - **All Categories** (combined multi-category view)
- **Filters**:
  - Channel multi-select
  - Published date range
- **KPI strip** (per current filters):
  - Total videos, channels, views
  - Average views per video
  - Median engagement rate
- **Visuals**:
  - Top channels by views (horizontal bar chart + detailed table)
  - Monthly uploads & views (dual-axis line chart)
  - Best-performing videos (styled table with gradients)
  - Publishing day performance (bar charts for average views and engagement rate by weekday)
  - Views vs. engagement scatter (per-video bubble chart)
  - Engagement distribution (donut chart: low/medium/high buckets)

This view is ideal for stakeholder readouts on **portfolio-level performance** and publishing behavior.

### 2. Recommendations & Thumbnail Studio

Location: `dashboard/views/recommendations.py`

- **Dataset selector** (same categories as Channel Analysis, including **All Categories**).
- **Analytics-backed recommendations**:
  - KPIs for:
    - Best publish day
    - Target title length
    - High-performing sample size
  - Suggested keyword angles rendered as **styled chips**.
  - Reference videos to model (styled dataframe with optional thumbnail preview column).
- **🎨 AI Thumbnail Studio**:
  - Provider: `gemini` or `openai`
  - Model fields:
    - Gemini (e.g. `gemini-2.0-flash-exp-image-generation`)
    - OpenAI (e.g. `gpt-image-1`)
  - Inputs:
    - Video title, context, style, negative prompt
    - Number of options and size (for OpenAI)
  - Outputs:
    - Grid of thumbnail cards with hover effects
    - One-click **Download** for each generated image

This page connects **observed data patterns** with **creative assets** (thumbnails) in a single workflow.

### 3. Ytuber – Creator Suite

Location: `dashboard/views/ytuber.py`

End-to-end **creator cockpit** combining YouTube API pulls, analytics, and AI assistance.

#### Inputs
- `YOUTUBE_API_KEY` (from `.env` or Streamlit secrets)
- Channel handle / name / channel ID
- Optional: force-refresh toggle to bypass cache

#### Tabs

1. **Overview**
   - KPIs for videos (1Y), views, likes, comments, average views, median engagement
   - Monthly uploads + views (dual-axis Plotly line chart)
   - Top 12 videos table (styled)

2. **Channel Audit**
   - Consistency score, average upload gap, 90-day view growth, outlier rate
   - Audit notes rendered in styled cards

3. **Keyword Intel**
   - Keyword table with scores (styled dataframe)
   - High-opportunity keywords as chips
   - Keyword treemap and bar chart for opportunity visualization

4. **Title & SEO Lab**
   - Title and description scores as **gauge charts**
   - Detailed breakdown tables
   - Suggested improvements as tip lists

5. **Competitor Benchmark**
   - Compare multiple competitor channels:
     - Videos (1Y), total views, average views, median engagement
   - Radar chart and bar charts for stakeholder-friendly comparisons

6. **Trend Radar**
   - Rising vs. falling keyword momentum in the last 60 days vs prior 60
   - Styled table + diverging bar charts

7. **Content Planner**
   - Best day and hour for publishing (KPI cards)
   - Day × metric heatmap and views-by-hour bar chart
   - 4-week suggested calendar rendered as visual cards

8. **AI Studio**
   - **Dual-provider AI content and thumbnail lab**:
     - Text provider: `gemini` or `openai`
       - Models such as `gemini-2.0-flash` or `gpt-4.1-mini`
     - Image provider: `gemini` or `openai`
       - Models such as `gemini-2.0-flash-exp-image-generation` or `gpt-image-1`
   - Creative brief + task selector (full pack, titles only, descriptions only, scripts, hooks/CTAs)
   - AI Output rendered in a styled, scrollable card with preserved formatting
   - Thumbnails rendered using the same grid/card system as Recommendations

This suite is designed for **live strategy sessions** with stakeholders and for hands-on creator experimentation.

---

## Visual Analytics
Place generated visuals in `outputs/figures/` and link them here. Recommended artifacts:
- **Channel Performance Summary:** engagement vs. frequency
- **Topic Clusters:** BERTopic 2D embeddings and top keywords
- **Recommendation Impact:** before/after mock strategy uplift

## Ethics and Compliance
- Respect YouTube API Terms of Service
- Do not store or share personally identifiable information (PII)
- Publish only aggregated or anonymized insights

## Contributing
See `CONTRIBUTING.md` for standards and workflow.

## License
MIT License. See `LICENSE`.

---

## Deployment (Streamlit Cloud)

The dashboard is designed to be deployed directly to **Streamlit Cloud**.

1. **Push to GitHub**
   - Repository should contain:
     - `dashboard/app.py` (entrypoint)
     - `.streamlit/config.toml`
     - `requirements.txt`

2. **Create Streamlit app**
   - Visit the Streamlit Cloud UI and click **New app**.
   - Choose:
     - **Repo**: `Debadri1999/Youtube-Optmization`
     - **Branch**: `main`
     - **Main file path**: `dashboard/app.py`

3. **Configure secrets**
   - In the app settings, add:
     ```toml
     YOUTUBE_API_KEY = "your_youtube_key"
     GEMINI_API_KEY = "your_gemini_key"
     OPENAI_API_KEY = "your_openai_key"
     ```

4. **Launch**
   - Streamlit installs dependencies from `requirements.txt` and boots the app with the dark theme + all dashboards enabled.

This setup is stakeholder-ready for demos to Google and Purdue partners: the UI, navigation, and AI integrations mirror a modern SaaS analytics product.
