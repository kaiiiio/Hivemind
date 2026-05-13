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
