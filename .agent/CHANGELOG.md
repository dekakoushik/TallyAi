# Changelog

All notable changes to the TallyAI Dashboard project are documented in this file.

## [1.0.0] - 2026-11-14

### Added
- **.agent Directory**:
  - `ARCHITECTURE.md`: High-level system architecture, sync protocol, and static IP remote configuration.
  - `SCHEMA.md`: Complete database models (Companies, Ledgers, Vouchers, OutstandingBills, SyncLogs).
  - `CHANGELOG.md`: Continuous records of all system changes.
- **tally-agent**:
  - `tally_xml_templates.py`: TDL XML envelopes for Exporting Companies, Ledgers, Vouchers, and Outstandings via Tally XML Gateway.
  - `tally_parser.py`: Robust XML-to-JSON and dictionary normalizer.
  - `tally_client.py`: Resilient HTTP client communicating with Tally Prime on port 9000.
  - `mock_tally_server.py`: Local Tally Prime emulator on port 9000 for instant offline testing and validation.
- **backend**:
  - FastAPI service with CORS enabled for remote static IP clients.
  - SQLite/SQLAlchemy ORM models and database setup.
  - Background scheduler (APScheduler) for periodic automatic sync.
  - `/api/v1/metrics`, `/api/v1/receivables`, `/api/v1/payables`, `/api/v1/vouchers`, `/api/v1/sync`.
  - `/api/v1/ask-ai`: Natural language querying engine for debtor analysis, bank balances, and sales performance.
- **frontend**:
  - Responsive dark-mode dashboard built with React (Vite) and Tailwind CSS.
  - Executive KPI Cards (Receivables, Payables, Cash/Bank Liquidity, Sales Revenue).
  - Debtor aging chart (0-30, 31-60, 61-90, 90+ days).
  - Liquidity coverage progress indicators.
  - Full Accounts Receivable table with overdue tracking.
  - Full Vouchers & Invoices ledger table.
  - Embedded conversational "Ask Tally AI" chat assistant.
  - Configured to bind on `0.0.0.0:3000` for remote Static IP accessibility.
- **Launchers**:
  - `start-all.bat`: One-click startup for Backend + Frontend.
  - `tally-agent/start-mock-tally.bat`: Instant startup for mock Tally environment.

## [1.1.0] - 2026-11-16

### Added
- Created `tally-agent/run_agent.py`: Standalone background polling agent and Windows service script.
- Created `tally-agent/start-service.bat`: 1-click batch launcher for running the sync agent on the Tally machine.
- Created `tally-agent/.env.example`: Configuration file for `TALLY_HOST`, `TALLY_PORT`, `BACKEND_API_URL`, and `SYNC_INTERVAL_SECS`.
- Created `tally-agent/SERVER_INSTALL_GUIDE.md`: Step-by-step server setup guide including Tally Prime connectivity settings, NSSM Windows service instructions, and router port forwarding.

## [1.2.0] - 2026-11-16

### Network & IP Configuration
- Configured Tally Server LAN IP: `192.168.2.100` (port `9000`).
- Configured Public Static IP: `115.246.171.163` for worldwide dashboard access.
- Updated `backend/.env` with `TALLY_HOST=http://192.168.2.100` and `TALLY_PORT=9000`.
- Updated `tally-agent/.env` to query `http://192.168.2.100:9000`.
- Updated `frontend/src/App.jsx` dynamic API host resolver so it works automatically whether accessed via `localhost`, office LAN (`192.168.2.100:3000`), or public Static IP (`115.246.171.163:3000`).
- Updated `start-all.bat` launcher with network details.

## [1.3.0] - 2026-11-16

### Dokploy Cloud & Lightweight Agent Architecture
- Added `Dockerfile` & `docker-compose.yml` to deploy the entire Dashboard + Backend on **Dokploy** (or VPS) in one container.
- Added `/api/v1/sync-push` endpoint in `backend/app/api/routes.py` to allow the local agent on the Tally PC to push updates outwards without requiring inbound ports on the Tally PC.
- Built lightweight standalone push agent `tally-agent/push_agent.py` and `tally-agent/start-push-agent.bat`.
- The Tally PC only needs the tiny `tally-agent/` folder (no database, no Node.js, no frontend).
