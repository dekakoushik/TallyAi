# Tally Sync Agent - Server Installation & Setup Guide

The agent is located in the `tally-agent/` folder of this project.

## How It Works
Tally Prime has a built-in XML Server (ODBC/HTTP) that runs on port `9000`.
The `tally-agent` service:
1. Pings Tally on `http://127.0.0.1:9000` to verify Tally is open.
2. Posts TDL/XML requests to pull Ledger masters, Vouchers, and Overdue Bills.
3. Parses the XML into clean records and updates the database via the API.
4. Repeats automatically on your configured interval (e.g., every 5 minutes).

---

## Step 1: Enable XML Gateway in Tally Prime (1-minute setup)
On your Tally server:
1. Open **Tally Prime**.
2. Press **F1** (Help) > **Settings** > **Connectivity**.
3. Under **Client/Server configuration**:
   - Set **TallyPrime acts as**: `Both` (or `Server`)
   - Set **Port**: `9000`
4. Press `Ctrl + A` to save and **restart Tally Prime**.
5. Keep your company loaded in Tally.

---

## Step 2: Where the Agent Files Are
Copy or locate the folder on your Tally server:
`D:\Projects\TallyAi\tally-agent\`

Key files inside:
- `run_agent.py`: The background sync script.
- `start-service.bat`: Double-click batch runner.
- `.env.example`: Configuration file (sync interval, port, backend URL).
- `tally_client.py`: XML HTTP communication engine.
- `tally_parser.py`: Tally XML parser.

---

## Step 3: Running the Agent

### Option A: Direct Double-Click (Quickest)
Simply double-click:
`tally-agent\start-service.bat`

It will continuously monitor Tally and sync data automatically.

### Option B: Run as a Silent Windows Background Service (NSSM)
If you want it to run permanently in the background even when no user is logged in:
1. Download NSSM (Non-Sucking Service Manager) or use Windows Task Scheduler.
2. Run:
   ```cmd
   nssm install TallySyncAgent "D:\Projects\TallyAi\backend\venv\Scripts\python.exe" "D:\Projects\TallyAi\tally-agent\run_agent.py"
   nssm start TallySyncAgent
   ```

---

## Step 4: Accessing the Dashboard from Anywhere (Static IP)
1. Run `start-all.bat` in `D:\Projects\TallyAi\`.
2. On your router/firewall, forward port `3000` (Frontend) and `8000` (Backend) to this server's LAN IP.
3. Access from any phone, laptop, or remote office at:
   `http://<YOUR_STATIC_IP>:3000`
