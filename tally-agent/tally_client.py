"""
Tally Client:
Handles HTTP communication with Tally Prime's XML Gateway (usually http://localhost:9000).
Supports real Tally connections and mock responses when Tally is offline.
"""
import requests
import logging
from typing import Dict, Any, Optional
import tally_xml_templates as templates
import tally_parser as parser

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("TallyClient")

class TallyClient:
    def __init__(self, host: str = "http://127.0.0.1", port: int = 9000, timeout: int = 10):
        self.url = f"{host}:{port}"
        self.timeout = timeout

    def check_connection(self) -> bool:
        """Pings Tally XML port to see if Tally is online."""
        try:
            resp = requests.post(self.url, data=templates.get_companies_xml(), timeout=self.timeout)
            return resp.status_code == 200
        except Exception:
            return False

    def query(self, xml_payload: str) -> Optional[str]:
        """Sends an XML request to Tally and returns the response string."""
        try:
            headers = {"Content-Type": "text/xml;charset=utf-8"}
            response = requests.post(self.url, data=xml_payload, headers=headers, timeout=self.timeout)
            if response.status_code == 200:
                return response.text
            else:
                logger.error(f"Tally returned status code {response.status_code}")
                return None
        except requests.exceptions.ConnectionError:
            logger.warning(f"Could not connect to Tally on {self.url}. Make sure Tally is open with XML enabled.")
            return None
        except Exception as e:
            logger.error(f"Error communicating with Tally: {e}")
            return None

    def fetch_all_data(self, company_name: str = "") -> Dict[str, Any]:
        """Fetches companies, ledgers, vouchers, and bills outstanding."""
        result = {
            "online": False,
            "companies": [],
            "ledgers": [],
            "vouchers": [],
            "receivables": [],
            "payables": []
        }

        # Check connection
        if not self.check_connection():
            logger.info("Tally XML server offline. Using fallback / offline state.")
            return result

        result["online"] = True

        # 1. Fetch Companies
        cmp_xml = self.query(templates.get_companies_xml())
        if cmp_xml:
            parsed = parser.parse_tally_xml(cmp_xml)
            result["companies"] = parser.extract_companies(parsed)

        # 2. Fetch Ledgers
        ldg_xml = self.query(templates.get_ledgers_xml(company_name))
        if ldg_xml:
            parsed = parser.parse_tally_xml(ldg_xml)
            result["ledgers"] = parser.extract_ledgers(parsed)

        # 3. Fetch Vouchers
        vch_xml = self.query(templates.get_vouchers_xml(company_name))
        if vch_xml:
            parsed = parser.parse_tally_xml(vch_xml)
            result["vouchers"] = parser.extract_vouchers(parsed)

        return result
