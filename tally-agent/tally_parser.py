"""
Tally XML Parser.
Parses response XML strings from Tally Prime into clean Python dictionaries.
"""
import xmltodict
from typing import Dict, Any, List

def parse_tally_xml(xml_content: str) -> Dict[str, Any]:
    try:
        data = xmltodict.parse(xml_content)
        return data
    except Exception as e:
        return {"error": str(e), "raw": xml_content}

def extract_companies(parsed_dict: Dict[str, Any]) -> List[Dict[str, Any]]:
    companies = []
    try:
        body = parsed_dict.get("ENVELOPE", {}).get("BODY", {})
        data_block = body.get("DATA", {}) or body.get("EXPORTDATA", {})
        cmp_list = data_block.get("COLLECTION", {}).get("COMPANY", [])
        if isinstance(cmp_list, dict):
            cmp_list = [cmp_list]
        for c in cmp_list:
            companies.append({
                "name": c.get("@NAME", c.get("NAME", "Unknown Company")),
                "guid": c.get("GUID", "")
            })
    except Exception:
        pass
    return companies

def extract_ledgers(parsed_dict: Dict[str, Any]) -> List[Dict[str, Any]]:
    ledgers = []
    try:
        body = parsed_dict.get("ENVELOPE", {}).get("BODY", {})
        data_block = body.get("DATA", {}) or body.get("EXPORTDATA", {})
        tally_msg = data_block.get("TALLYMESSAGE", [])
        if isinstance(tally_msg, dict):
            tally_msg = [tally_msg]
        for msg in tally_msg:
            ledger = msg.get("LEDGER")
            if not ledger:
                continue
            name = ledger.get("@NAME", ledger.get("NAME", ""))
            parent = ledger.get("PARENT", "")
            closing_bal = ledger.get("CLOSINGBALANCE", 0)
            try:
                closing_bal = float(closing_bal)
            except (ValueError, TypeError):
                closing_bal = 0.0

            ledgers.append({
                "name": name,
                "parent_group": parent,
                "closing_balance": closing_bal,
                "guid": ledger.get("GUID", "")
            })
    except Exception:
        pass
    return ledgers

def extract_vouchers(parsed_dict: Dict[str, Any]) -> List[Dict[str, Any]]:
    vouchers = []
    try:
        body = parsed_dict.get("ENVELOPE", {}).get("BODY", {})
        data_block = body.get("DATA", {}) or body.get("EXPORTDATA", {})
        tally_msg = data_block.get("TALLYMESSAGE", [])
        if isinstance(tally_msg, dict):
            tally_msg = [tally_msg]
        for msg in tally_msg:
            v = msg.get("VOUCHER")
            if not v:
                continue
            v_type = v.get("VOUCHERTYPENAME", v.get("@VCHTYPE", "Sales"))
            v_number = v.get("VOUCHERNUMBER", "")
            v_date = v.get("DATE", "")
            party_name = v.get("PARTYLEDGERNAME", "")
            guid = v.get("GUID", "")
            
            # Extract line items
            ledger_entries = v.get("ALLLEDGERENTRIES.LIST", [])
            if isinstance(ledger_entries, dict):
                ledger_entries = [ledger_entries]
            
            total_amount = 0.0
            entries = []
            for entry in ledger_entries:
                l_name = entry.get("LEDGERNAME", "")
                amt = entry.get("AMOUNT", 0)
                try:
                    amt = float(amt)
                except (ValueError, TypeError):
                    amt = 0.0
                entries.append({"ledger_name": l_name, "amount": amt})
                if abs(amt) > abs(total_amount):
                    total_amount = abs(amt)

            vouchers.append({
                "guid": guid,
                "voucher_type": v_type,
                "voucher_number": v_number,
                "date": v_date,
                "party_name": party_name,
                "amount": total_amount,
                "entries": entries
            })
    except Exception:
        pass
    return vouchers
