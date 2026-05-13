# Setup Guide

Follow these steps to set up a stable and reproducible development environment for Hivemind.

## 1. Prerequisites
- Python 3.10+
- Docker & Docker Compose
- [Playwright](https://playwright.dev/python/)

## 2. Environment Initialization

It is highly recommended to use a Python virtual environment to prevent dependency conflicts.

```bash
# Navigate to the project root
cd Hivemind

# Create a virtual environment
python -m venv venv

# Activate it (Linux/Mac)
source venv/bin/activate
# Or on Windows:
# .\venv\Scripts\activate

# Install core dependencies
pip install -r requirements.txt

# Install Playwright browsers (required for Screener.in extraction)
playwright install chromium
```

## 3. Configuration

The system relies on external APIs and databases. Ensure your `.env` is correctly set up.

```bash
# Copy the template
cp config/.env.example .env

# Edit .env with your credentials
# Key variables include:
# - SCREENER_USERNAME & SCREENER_PASSWORD
# - SCREENER_SCREEN_URL: Your custom screener.in dashboard URL
# - DB_HOST, DB_PORT, DB_NAME, etc. (for TimescaleDB)
```

## 4. Database Infrastructure

The system uses TimescaleDB for time-series data storage.

```bash
# Start the database container
docker-compose up -d timescaledb

# Verify the container is running
docker-compose ps
```

## 5. Maintenance
Keep your environment up to date by periodically running:
```bash
pip install -r requirements.txt --upgrade
playwright install chromium --upgrade
```
