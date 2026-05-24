# Usage Guide

This guide explains how to run the Hivemind data ingestion pipeline and manage its execution.

## Running the Pipeline

Once the [environment is set up](SETUP.md), you can execute the master data ingestion pipeline.

```bash
# Navigate to the source directory
cd src

# Run the master orchestrator
python data_ingestion/master_pipeline.py
```

## Running The Free AI Layer

The AI layer can be tested without paid APIs. Start with dry-run RSS ingestion:

```powershell
python src\ai_layer_cli.py ingest-rss --source "Sample=docs\sample_feed.xml" --ticker ABC --ticker XYZ --dry-run
python src\ai_layer_cli.py ingest-rss --source-config docs\sample_sources.json --dry-run
```

Use a real permitted RSS feed URL when available. Dry-run mode fetches, classifies, resolves tickers/company aliases, and scores events but does not write to Postgres.

To persist RSS events and alerts locally:

```powershell
docker compose up -d
python src\ai_layer_cli.py ingest-rss --source "Sample=docs\sample_feed.xml" --ticker ABC --ticker XYZ
python src\ai_layer_cli.py ingest-rss --source-config docs\sample_sources.json
```

To review stored alerts:

```powershell
python src\ai_layer_cli.py alerts --limit 20
python src\ai_layer_cli.py alerts --status ALL --limit 50
```

To run the first deterministic agent triage loop without paid APIs:

```powershell
python src\ai_layer_cli.py triage-rss --source "Sample=docs\sample_feed.xml" --ticker ABC --ticker XYZ
python src\ai_layer_cli.py triage-rss --source-config docs\sample_sources.json
```

If you pass a current price, APEX can produce a paper-only `PROCEED` decision when the event has cited evidence, VERA does not veto, and the alert score is high enough:

```powershell
python src\ai_layer_cli.py triage-rss --source "Sample=docs\sample_feed.xml" --ticker ABC --ticker XYZ --current-price 100
python src\ai_layer_cli.py triage-rss --source-config docs\sample_sources.json --current-price 100
```

To persist the event, alert, and all four deterministic agent outputs:

```powershell
docker compose up -d
python src\ai_layer_cli.py triage-rss --source "Sample=docs\sample_feed.xml" --ticker ABC --ticker XYZ --current-price 100 --persist
python src\ai_layer_cli.py triage-rss --source-config docs\sample_sources.json --current-price 100 --persist
```

To also write compact Redis memory and Neo4j graph facts when local services are running:

```powershell
python src\ai_layer_cli.py triage-rss --source-config docs\sample_sources.json --current-price 100 --persist --remember --graph
```

To review persisted agent outputs:

```powershell
python src\ai_layer_cli.py agent-outputs --limit 20
python src\ai_layer_cli.py agent-outputs --agent APEX --limit 10
python src\ai_layer_cli.py agent-outputs --ticker ABC --limit 10
```

To review Redis mistake memory:

```powershell
python src\ai_layer_cli.py mistakes --agent VERA --limit 10
python src\ai_layer_cli.py mistakes --agent APEX --limit 10
```

All of the above uses local Docker/Postgres and deterministic rules. No paid model provider is required.

### What happens when you run it?
1. **Universe Sync**: Updates the list of F&O stocks.
2. **Fundamental Scan**: Scrapes and updates fundamental metrics for the universe.
3. **Regime Analysis**: Checks VIX and institutional flows.
4. **Price Update**: Loads OHLCV and delivery data for the day.
5. **Database Sync**: All collected data is upserted into TimescaleDB.

---

## Scheduling (Production)

For a fully automated setup, it is recommended to run the pipeline daily after market hours.

### Linux (Cron)
We recommend running the script at **18:30 IST** (after Bhavcopy is typically released).

```bash
# Open crontab
crontab -e

# Add the following line (adjust paths to your project)
30 18 * * 1-5 cd /path/to/Hivemind/src && /path/to/Hivemind/venv/bin/python data_ingestion/master_pipeline.py >> /var/log/hivemind.log 2>&1
```

### Windows (Task Scheduler)
1. Open Task Scheduler.
2. Create a "Basic Task".
3. Trigger: Daily at 18:30.
4. Action: Start a Program.
5. Program/script: `C:\path\to\Hivemind\venv\Scripts\python.exe`
6. Add arguments: `data_ingestion\master_pipeline.py`
7. Start in: `C:\path\to\Hivemind\src`

---

## Troubleshooting

### Database Connection Failures
- Ensure the Docker container is running: `docker-compose ps`.
- Check `.env` credentials.

### Playwright Timeouts
- If Screener.in takes too long to load, the script might time out. Ensure you have a stable internet connection.
- Verify `SCREENER_SCREEN_URL` is accessible in a normal browser.
