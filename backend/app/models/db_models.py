"""
Database Models using SQLAlchemy
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    tally_guid = Column(String, unique=True, index=True)
    name = Column(String, nullable=False)
    last_sync_at = Column(DateTime, default=datetime.utcnow)

class Ledger(Base):
    __tablename__ = "ledgers"
    id = Column(Integer, primary_key=True, index=True)
    tally_guid = Column(String, unique=True, index=True)
    company_name = Column(String, default="")
    name = Column(String, index=True, nullable=False)
    parent_group = Column(String, index=True)
    closing_balance = Column(Float, default=0.0)
    contact_person = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    gstin = Column(String, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow)

class Voucher(Base):
    __tablename__ = "vouchers"
    id = Column(Integer, primary_key=True, index=True)
    tally_guid = Column(String, unique=True, index=True)
    voucher_number = Column(String, index=True)
    voucher_type = Column(String, index=True)
    date = Column(String)  # YYYYMMDD
    party_name = Column(String, index=True)
    amount = Column(Float, default=0.0)
    narration = Column(Text, nullable=True)
    is_cancelled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class OutstandingBill(Base):
    __tablename__ = "outstanding_bills"
    id = Column(Integer, primary_key=True, index=True)
    bill_type = Column(String, index=True)  # RECEIVABLE or PAYABLE
    party_name = Column(String, index=True)
    bill_number = Column(String)
    bill_date = Column(String)
    due_date = Column(String)
    pending_amount = Column(Float, default=0.0)
    overdue_days = Column(Integer, default=0)
    aging_bucket = Column(String)  # '0-30', '31-60', '61-90', '90+'

class SyncLog(Base):
    __tablename__ = "sync_logs"
    id = Column(Integer, primary_key=True, index=True)
    status = Column(String)  # 'SUCCESS', 'FAILED', 'WARNING'
    records_synced = Column(Integer, default=0)
    message = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
