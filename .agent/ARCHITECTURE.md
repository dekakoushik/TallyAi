# Project Overview: TallyAI Dashboard & Sync System

## 1. Objectives
- **Local Agent (Tally Connector Service)**: Built from scratch to communicate directly with Tally Prime / Tally ERP 9 via XML/TDL interface (HTTP port 9000 by default), parse ledgers, vouchers, outstanding dues, cash/bank balances, and sync into storage.
- **Remote Access via Static IP**: The server has a static IP address. The system must support secure API authentication (API keys/JWT), configurable ports, and secure remote dashboard access.
- **Documentation & Continuity**: `.agent` stores architectural decisions, schemas, API specifications, and changelogs for continuity across sessions.

## 2. Architecture
```
┌────────────────────────────────────────────────────────┐
│               Tally Server (Localhost)                 │
│  - Tally Prime running XML Server (Port 9000)          │
│  - Tally Data Directory                                │
└───────────────────────────┬────────────────────────────┘
                            │ XML / TDL Request & Response
                            ▼
┌────────────────────────────────────────────────────────┐
│             Tally Local Sync Agent / Service           │
│  - Windows Background Service / Python Daemon          │
│  - TDL Generators (Vouchers, Ledgers, Outstandings)    │
│  - XML Parser & Normalizer                             │
│  - Push / Sync to Backend SQLite / Postgres DB         │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│                  Backend API Service                   │
│  - FastAPI (Python)                                    │
│  - Endpoints: KPI metrics, Sales, Receivables,         │
│    Payables, Cash flow, Inventory, Sync Trigger        │
│  - AI Query Engine (Natural language analytics)        │
│  - Token / API Key Auth for Static IP exposure         │
└───────────────────────────┬────────────────────────────┘
                            │ REST / JSON
                            ▼
┌────────────────────────────────────────────────────────┐
│               Web Frontend Dashboard                   │
│  - React (Vite) + Tailwind CSS + Lucide + Charts       │
│  - Executive KPI Cards                                 │
│  - Overdue Receivables & Aging                         │
│  - Sales & Purchase Trends                             │
│  - Tally Connection Status & Manual Sync Trigger       │
│  - Natural Language AI Assistant                       │
└────────────────────────────────────────────────────────┘
```

## 3. Directory Layout
- `tally-agent/` : Standalone local agent service that queries Tally XML server. Can run as CLI or Windows Service. Includes mock Tally server for testing when Tally is offline.
- `backend/` : FastAPI backend server, database models, analytics pipelines, authentication, and API endpoints.
- `frontend/` : Modern web UI dashboard built with React + Vite + Tailwind CSS.
- `.agent/` : Architecture, schema definitions, sync protocols, and changelog records.
