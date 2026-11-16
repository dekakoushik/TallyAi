"""
Tally XML / TDL Request Templates.
Tally Prime / ERP 9 responds to HTTP POST requests containing XML wrappers.
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
    cmp_filter = f"<STATICVARIABLES><SVCURRENTCOMPANY>{company_name}</SVCURRENTCOMPANY></STATICVARIABLES>" if company_name else ""
    return f"""<ENVELOPE>
    <HEADER>
        <TALLYREQUEST>Export Data</TALLYREQUEST>
    </HEADER>
    <BODY>
        <EXPORTDATA>
            <REQUESTDESC>
                <REPORTNAME>Ledger</REPORTNAME>
                {cmp_filter}
            </REQUESTDESC>
        </EXPORTDATA>
    </BODY>
</ENVELOPE>"""

def get_vouchers_xml(company_name: str = "", from_date: str = "20240401", to_date: str = "20261231") -> str:
    return f"""<ENVELOPE>
    <HEADER>
        <TALLYREQUEST>Export Data</TALLYREQUEST>
    </HEADER>
    <BODY>
        <EXPORTDATA>
            <REQUESTDESC>
                <REPORTNAME>Voucher Register</REPORTNAME>
                <STATICVARIABLES>
                    {f"<SVCURRENTCOMPANY>{company_name}</SVCURRENTCOMPANY>" if company_name else ""}
                    <SVFROMDATE>{from_date}</SVFROMDATE>
                    <SVTODATE>{to_date}</SVTODATE>
                </STATICVARIABLES>
            </REQUESTDESC>
        </EXPORTDATA>
    </BODY>
</ENVELOPE>"""

def get_bills_outstanding_xml(company_name: str = "", bill_type: str = "Receivables") -> str:
    """
    bill_type can be 'Receivables' or 'Payables' (Bills Outstanding report in Tally).
    """
    report_name = "Bills Outstanding" if bill_type == "Receivables" else "Bills Payable"
    return f"""<ENVELOPE>
    <HEADER>
        <TALLYREQUEST>Export Data</TALLYREQUEST>
    </HEADER>
    <BODY>
        <EXPORTDATA>
            <REQUESTDESC>
                <REPORTNAME>{report_name}</REPORTNAME>
                {f"<STATICVARIABLES><SVCURRENTCOMPANY>{company_name}</SVCURRENTCOMPANY></STATICVARIABLES>" if company_name else ""}
            </REQUESTDESC>
        </EXPORTDATA>
    </BODY>
</ENVELOPE>"""

def get_trial_balance_xml(company_name: str = "") -> str:
    return f"""<ENVELOPE>
    <HEADER>
        <TALLYREQUEST>Export Data</TALLYREQUEST>
    </HEADER>
    <BODY>
        <EXPORTDATA>
            <REQUESTDESC>
                <REPORTNAME>Trial Balance</REPORTNAME>
                {f"<STATICVARIABLES><SVCURRENTCOMPANY>{company_name}</SVCURRENTCOMPANY></STATICVARIABLES>" if company_name else ""}
            </REQUESTDESC>
        </EXPORTDATA>
    </BODY>
</ENVELOPE>"""
