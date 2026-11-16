"""
Optimized TDL / XML requests for fast export from Tally Prime.
Uses collection queries with specific attributes to prevent full-database scan timeouts.
"""

def get_companies_xml() -> str:
    return """<ENVELOPE>
    <HEADER>
        <TALLYREQUEST>Export Data</TALLYREQUEST>
    </HEADER>
    <BODY>
        <EXPORTDATA>
            <REQUESTDESC>
                <REPORTNAME>List of Companies</REPORTNAME>
            </REQUESTDESC>
        </EXPORTDATA>
    </BODY>
</ENVELOPE>"""

def get_ledgers_xml(company_name: str = "") -> str:
    """Fast collection query fetching only essential ledger attributes."""
    cmp_filter = f"<STATICVARIABLES><SVCURRENTCOMPANY>{company_name}</SVCURRENTCOMPANY></STATICVARIABLES>" if company_name else ""
    return f"""<ENVELOPE>
    <HEADER>
        <TALLYREQUEST>Export Data</TALLYREQUEST>
    </HEADER>
    <BODY>
        <EXPORTDATA>
            <REQUESTDESC>
                <STATICVARIABLES>
                    <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
                    {cmp_filter}
                </STATICVARIABLES>
                <TDL>
                    <TDLMESSAGE>
                        <COLLECTION NAME="LedgerExport" ISINITIALIZE="Yes">
                            <TYPE>Ledger</TYPE>
                            <FETCH>Name,Parent,ClosingBalance,OpeningBalance,Guid</FETCH>
                        </COLLECTION>
                    </TDLMESSAGE>
                </TDL>
                <REPORTNAME>Ledger</REPORTNAME>
            </REQUESTDESC>
        </EXPORTDATA>
    </BODY>
</ENVELOPE>"""

def get_vouchers_xml(company_name: str = "", from_date: str = "20260401", to_date: str = "20261130") -> str:
    """Fetches vouchers with date filter to stay fast."""
    return f"""<ENVELOPE>
    <HEADER>
        <TALLYREQUEST>Export Data</TALLYREQUEST>
    </HEADER>
    <BODY>
        <EXPORTDATA>
            <REQUESTDESC>
                <STATICVARIABLES>
                    <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
                    {f"<SVCURRENTCOMPANY>{company_name}</SVCURRENTCOMPANY>" if company_name else ""}
                    <SVFROMDATE>{from_date}</SVFROMDATE>
                    <SVTODATE>{to_date}</SVTODATE>
                </STATICVARIABLES>
                <REPORTNAME>Voucher Register</REPORTNAME>
            </REQUESTDESC>
        </EXPORTDATA>
    </BODY>
</ENVELOPE>"""
