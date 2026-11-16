"""
Mock Tally Server for development, demo, and testing when Tally is offline.
Emulates Tally Prime XML HTTP responses on port 9000.
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MockTally")

SAMPLE_COMPANIES_XML = """<ENVELOPE>
    <HEADER><TALLYREQUEST>Export Data</TALLYREQUEST></HEADER>
    <BODY>
        <DATA>
            <COLLECTION>
                <COMPANY NAME="Apex Enterprises Pvt Ltd">
                    <GUID>COMP-APEX-2024-001</GUID>
                </COMPANY>
                <COMPANY NAME="Global Logistics Inc">
                    <GUID>COMP-GLO-2024-002</GUID>
                </COMPANY>
            </COLLECTION>
        </DATA>
    </BODY>
</ENVELOPE>"""

SAMPLE_LEDGERS_XML = """<ENVELOPE>
    <HEADER><TALLYREQUEST>Export Data</TALLYREQUEST></HEADER>
    <BODY>
        <DATA>
            <TALLYMESSAGE>
                <LEDGER NAME="Metro Tech Solutions">
                    <GUID>LEDG-001</GUID>
                    <PARENT>Sundry Debtors</PARENT>
                    <CLOSINGBALANCE>-425000.00</CLOSINGBALANCE>
                </LEDGER>
            </TALLYMESSAGE>
            <TALLYMESSAGE>
                <LEDGER NAME="BlueStar Industries">
                    <GUID>LEDG-002</GUID>
                    <PARENT>Sundry Debtors</PARENT>
                    <CLOSINGBALANCE>-185000.00</CLOSINGBALANCE>
                </LEDGER>
            </TALLYMESSAGE>
            <TALLYMESSAGE>
                <LEDGER NAME="Zenith Trading Corp">
                    <GUID>LEDG-003</GUID>
                    <PARENT>Sundry Debtors</PARENT>
                    <CLOSINGBALANCE>-95000.00</CLOSINGBALANCE>
                </LEDGER>
            </TALLYMESSAGE>
            <TALLYMESSAGE>
                <LEDGER NAME="HDFC Current Account">
                    <GUID>LEDG-004</GUID>
                    <PARENT>Bank Accounts</PARENT>
                    <CLOSINGBALANCE>1250000.00</CLOSINGBALANCE>
                </LEDGER>
            </TALLYMESSAGE>
            <TALLYMESSAGE>
                <LEDGER NAME="ICICI Bank Ltd">
                    <GUID>LEDG-005</GUID>
                    <PARENT>Bank Accounts</PARENT>
                    <CLOSINGBALANCE>680000.00</CLOSINGBALANCE>
                </LEDGER>
            </TALLYMESSAGE>
            <TALLYMESSAGE>
                <LEDGER NAME="Petty Cash">
                    <GUID>LEDG-006</GUID>
                    <PARENT>Cash-in-hand</PARENT>
                    <CLOSINGBALANCE>45000.00</CLOSINGBALANCE>
                </LEDGER>
            </TALLYMESSAGE>
            <TALLYMESSAGE>
                <LEDGER NAME="Delta Suppliers">
                    <GUID>LEDG-007</GUID>
                    <PARENT>Sundry Creditors</PARENT>
                    <CLOSINGBALANCE>320000.00</CLOSINGBALANCE>
                </LEDGER>
            </TALLYMESSAGE>
            <TALLYMESSAGE>
                <LEDGER NAME="Supreme Polymers">
                    <GUID>LEDG-008</GUID>
                    <PARENT>Sundry Creditors</PARENT>
                    <CLOSINGBALANCE>215000.00</CLOSINGBALANCE>
                </LEDGER>
            </TALLYMESSAGE>
        </DATA>
    </BODY>
</ENVELOPE>"""

SAMPLE_VOUCHERS_XML = """<ENVELOPE>
    <HEADER><TALLYREQUEST>Export Data</TALLYREQUEST></HEADER>
    <BODY>
        <DATA>
            <TALLYMESSAGE>
                <VOUCHER VCHTYPE="Sales">
                    <GUID>VCH-2026-001</GUID>
                    <VOUCHERNUMBER>INV/26/0101</VOUCHERNUMBER>
                    <DATE>20261102</DATE>
                    <PARTYLEDGERNAME>Metro Tech Solutions</PARTYLEDGERNAME>
                    <ALLLEDGERENTRIES.LIST>
                        <LEDGERNAME>Metro Tech Solutions</LEDGERNAME>
                        <AMOUNT>-145000.00</AMOUNT>
                    </ALLLEDGERENTRIES.LIST>
                </VOUCHER>
            </TALLYMESSAGE>
            <TALLYMESSAGE>
                <VOUCHER VCHTYPE="Sales">
                    <GUID>VCH-2026-002</GUID>
                    <VOUCHERNUMBER>INV/26/0102</VOUCHERNUMBER>
                    <DATE>20261105</DATE>
                    <PARTYLEDGERNAME>BlueStar Industries</PARTYLEDGERNAME>
                    <ALLLEDGERENTRIES.LIST>
                        <LEDGERNAME>BlueStar Industries</LEDGERNAME>
                        <AMOUNT>-85000.00</AMOUNT>
                    </ALLLEDGERENTRIES.LIST>
                </VOUCHER>
            </TALLYMESSAGE>
            <TALLYMESSAGE>
                <VOUCHER VCHTYPE="Sales">
                    <GUID>VCH-2026-003</GUID>
                    <VOUCHERNUMBER>INV/26/0103</VOUCHERNUMBER>
                    <DATE>20261108</DATE>
                    <PARTYLEDGERNAME>Zenith Trading Corp</PARTYLEDGERNAME>
                    <ALLLEDGERENTRIES.LIST>
                        <LEDGERNAME>Zenith Trading Corp</LEDGERNAME>
                        <AMOUNT>-95000.00</AMOUNT>
                    </ALLLEDGERENTRIES.LIST>
                </VOUCHER>
            </TALLYMESSAGE>
            <TALLYMESSAGE>
                <VOUCHER VCHTYPE="Purchase">
                    <GUID>VCH-2026-004</GUID>
                    <VOUCHERNUMBER>PUR/26/0055</VOUCHERNUMBER>
                    <DATE>20261103</DATE>
                    <PARTYLEDGERNAME>Delta Suppliers</PARTYLEDGERNAME>
                    <ALLLEDGERENTRIES.LIST>
                        <LEDGERNAME>Delta Suppliers</LEDGERNAME>
                        <AMOUNT>120000.00</AMOUNT>
                    </ALLLEDGERENTRIES.LIST>
                </VOUCHER>
            </TALLYMESSAGE>
            <TALLYMESSAGE>
                <VOUCHER VCHTYPE="Receipt">
                    <GUID>VCH-2026-005</GUID>
                    <VOUCHERNUMBER>RCT/26/0012</VOUCHERNUMBER>
                    <DATE>20261110</DATE>
                    <PARTYLEDGERNAME>Metro Tech Solutions</PARTYLEDGERNAME>
                    <ALLLEDGERENTRIES.LIST>
                        <LEDGERNAME>HDFC Current Account</LEDGERNAME>
                        <AMOUNT>-50000.00</AMOUNT>
                    </ALLLEDGERENTRIES.LIST>
                </VOUCHER>
            </TALLYMESSAGE>
        </DATA>
    </BODY>
</ENVELOPE>"""

class MockTallyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/xml; charset=utf-8')
        self.end_headers()
        
        if "List of Companies" in post_data:
            self.wfile.write(SAMPLE_COMPANIES_XML.encode('utf-8'))
        elif "Ledger" in post_data:
            self.wfile.write(SAMPLE_LEDGERS_XML.encode('utf-8'))
        elif "Voucher" in post_data:
            self.wfile.write(SAMPLE_VOUCHERS_XML.encode('utf-8'))
        else:
            self.wfile.write(SAMPLE_LEDGERS_XML.encode('utf-8'))

    def log_message(self, format, *args):
        logger.info("%s - - [%s] %s" % (self.client_address[0], self.log_date_time_string(), format%args))

def start_mock_server(port: int = 9000):
    server = HTTPServer(('127.0.0.1', port), MockTallyHandler)
    logger.info(f"Mock Tally Prime server running on http://127.0.0.1:{port}")
    server.serve_forever()

if __name__ == "__main__":
    start_mock_server()
