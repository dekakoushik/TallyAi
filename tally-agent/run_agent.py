"""
Standalone Tally Sync Agent (Service / Daemon)
Can run directly on the Tally server machine as a background loop or Windows Service.
Pulls data from Tally XML (port 9000) and pushes it to the TallyAI Backend API.
"""
import time
import os
import sys
import logging
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("tally_agent.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("TallySyncAgent")

from tally_client import TallyClient

# Configuration via environment or defaults
TALLY_HOST = os.getenv("TALLY_HOST", "http://127.0.0.1")
TALLY_PORT = int(os.getenv("TALLY_PORT", "9000"))
BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8000/api/v1/sync")
SYNC_INTERVAL_SECS = int(os.getenv("SYNC_INTERVAL_SECS", "300")) # Default: 5 minutes

def run_sync_cycle():
    client = TallyClient(host=TALLY_HOST, port=TALLY_PORT)
    logger.info(f"Checking Tally connection at {TALLY_HOST}:{TALLY_PORT}...")
    
    if not client.check_connection():
        logger.warning(f"Tally Prime is NOT reachable at {TALLY_HOST}:{TALLY_PORT}. Waiting for next cycle...")
        return False

    logger.info("Tally Prime detected online. Triggering synchronization...")
    try:
        # Trigger sync on the backend API
        resp = requests.post(BACKEND_API_URL, timeout=30)
        if resp.status_code == 200:
            res_data = resp.json()
            logger.info(f"Sync successful! Records synced: {res_data.get('records_synced', 0)}")
            return True
        else:
            logger.error(f"Backend API returned error {resp.status_code}: {resp.text}")
            return False
    except Exception as e:
        logger.error(f"Failed to communicate with Backend API: {e}")
        return False

def main():
    logger.info("==========================================")
    logger.info("   TallyAI Local Sync Service Started     ")
    logger.info(f"   Tally Gateway : {TALLY_HOST}:{TALLY_PORT}")
    logger.info(f"   Backend Target: {BACKEND_API_URL}")
    logger.info(f"   Sync Interval : Every {SYNC_INTERVAL_SECS} seconds")
    logger.info("==========================================")

    while True:
        try:
            run_sync_cycle()
        except Exception as e:
            logger.error(f"Unexpected error during sync cycle: {e}")
        
        logger.info(f"Sleeping for {SYNC_INTERVAL_SECS} seconds...")
        time.sleep(SYNC_INTERVAL_SECS)

if __name__ == "__main__":
    main()
