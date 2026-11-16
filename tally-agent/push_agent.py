"""
Standalone Lightweight Tally Push Agent (For Tally PC).
Only requires Python with requests, xmltodict, and python-dotenv.
Pulls from local Tally (http://127.0.0.1:9000) and PUSHES to remote Dokploy server.
"""
import time
import os
import sys
import logging
import requests
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("tally_agent.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("TallyPushAgent")

from tally_client import TallyClient

TALLY_HOST = os.getenv("TALLY_HOST", "http://127.0.0.1")
TALLY_PORT = int(os.getenv("TALLY_PORT", "9000"))
REMOTE_DOKPLOY_API = os.getenv("REMOTE_DOKPLOY_API", "http://115.246.171.163:8000/api/v1/sync-push")
SYNC_INTERVAL_SECS = int(os.getenv("SYNC_INTERVAL_SECS", "300")) # 5 mins

def push_sync_cycle():
    client = TallyClient(host=TALLY_HOST, port=TALLY_PORT)
    logger.info(f"Checking Tally at {TALLY_HOST}:{TALLY_PORT}...")
    
    if not client.check_connection():
        logger.warning("Tally Prime is offline. Waiting for next cycle...")
        return False

    logger.info("Extracting data from Tally...")
    data = client.fetch_all_data()

    logger.info(f"Pushing data to remote Dokploy server: {REMOTE_DOKPLOY_API}...")
    try:
        resp = requests.post(REMOTE_DOKPLOY_API, json=data, timeout=60)
        if resp.status_code == 200:
            logger.info("Successfully pushed Tally data to Dokploy server!")
            return True
        else:
            logger.error(f"Dokploy server returned error: {resp.status_code} - {resp.text}")
            return False
    except Exception as e:
        logger.error(f"Failed to connect to Dokploy server: {e}")
        return False

def main():
    logger.info("==============================================")
    logger.info("   Tally Lightweight Push Agent (Tally PC)    ")
    logger.info(f"   Local Tally : {TALLY_HOST}:{TALLY_PORT}")
    logger.info(f"   Push Target : {REMOTE_DOKPLOY_API}")
    logger.info(f"   Interval    : Every {SYNC_INTERVAL_SECS} seconds")
    logger.info("==============================================")

    while True:
        try:
            push_sync_cycle()
        except Exception as e:
            logger.error(f"Error during push cycle: {e}")
        time.sleep(SYNC_INTERVAL_SECS)

if __name__ == "__main__":
    main()
