# 🌱 FoodSaver AI — SIH 2026 Prototype

**Problem Statement:** SIH26234 — AI-powered food waste reduction and redistribution platform for institutional kitchens and food processing units.

**Core flow:** Kitchen data → Demand forecast → Production plan → Surplus detection → Rescue-window urgency → NGO matching → Route to NGO → Unified dashboard

---

## Project Structure

```
food-waste-platform/
├── backend/          # Python · FastAPI · SQLAlchemy · PostgreSQL (Supabase)
├── frontend/         # Next.js 14 · TypeScript · Tailwind CSS · Recharts · MapLibre GL
└── README.md
```

---

## Prerequisites

| Tool | Version |
|---|---|
| Python | 3.11+ |
| Node.js | 18+ |
| npm / yarn | latest |
| PostgreSQL | via Supabase (cloud) |

---

## 1. Backend Setup

### 1.1 Install dependencies

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 1.2 Configure environment

```bash
cp .env.example .env
```

Edit `.env` and set your Supabase connection string:

```
DATABASE_URL=postgresql://postgres:<your-password>@<your-project>.supabase.co:5432/postgres
```

> **Where to find this:** Supabase Dashboard → Project Settings → Database → Connection string → URI mode. Use the "Direct connection" URI (port 5432), not the pooler.

### 1.3 Seed the database

This creates all tables and inserts 6 months of synthetic data:

```bash
cd backend
python -m scripts.seed_data
```

Expected output:
```
✓ Tables created
✓ Seeded: 1 kitchen, 8 food categories, 5 NGOs
✓ Generated: ~4,400 consumption records (6 months × 8 categories × 3 meals)
✓ Generated: ~4,400 production records
✓ Generated: ~1,200 surplus events
✓ Generated: ~183 sustainability metric rows
Seeding complete.
```

The script is **idempotent** — safe to re-run without duplicating data.

### 1.4 Run the backend

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

API docs available at: [http://localhost:8000/docs](http://localhost:8000/docs)

Health check: [http://localhost:8000/health](http://localhost:8000/health)

---

## 2. Frontend Setup

### 2.1 Install dependencies

```bash
cd frontend
npm install
```

### 2.2 Run the frontend

```bash
npm run dev
```

App available at: [http://localhost:3000](http://localhost:3000)

> Make sure the backend is running on port 8000 before opening the frontend, or you'll see API errors.

---

## 3. Regenerating Synthetic Data

To wipe and re-seed all synthetic data from scratch:

```bash
# From the backend/ directory with venv active
python -m scripts.seed_data
```

The script deletes existing rows before re-inserting, so the data is always fresh and consistent.

To export data as CSV instead of seeding into the DB, run:
```bash
python -m scripts.seed_data --export-csv
```
This writes CSV files to `backend/data/` (one per table).

---

## 4. API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `GET /health` | GET | Health check |
| `GET /forecast` | GET | Demand forecast for a category |
| `GET /surplus` | GET | Active surplus events with urgency |
| `POST /match` | POST | Ranked NGO list for a surplus event |
| `GET /route` | GET | Delivery route waypoints |
| `GET /dashboard/summary` | GET | Aggregated stats for dashboard |

Full interactive docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 5. What's Real vs. Stubbed

This is a **Phase 1 prototype**. The UI plumbing is fully wired, but the intelligence behind each module is currently a stub returning realistic-shaped fake data.

| Module | Status | Notes |
|---|---|---|
| **Database schema** | ✅ Real | All 8 tables created and normalized |
| **Synthetic data generator** | ✅ Real | 6 months of data with weekday/weekend/festival/seasonal variation |
| **NGO seed profiles** | ✅ Real | 5 NGOs with real Bengaluru coordinates |
| **Dashboard UI** | ✅ Real | Wired to live API |
| **Surplus list UI** | ✅ Real | Wired to live API |
| **NGO match list UI** | ✅ Real | Wired to live API |
| **Map with NGO markers** | ✅ Real | Real MapLibre GL JS with OSM tiles |
| **Route polyline on map** | ✅ Real | Renders stub route data correctly |
| **Forecast chart** | ✅ Real | Recharts chart, renders stub data |
| **`/forecast` logic** | 🟡 Stub | Returns deterministic fake predictions; Phase 2 will replace with Prophet/ARIMA model |
| **`/surplus` logic** | 🟡 Stub | Returns hardcoded surplus events; Phase 2 will query live DB with rule-based detection |
| **`/match` logic** | 🟡 Stub | Returns hardcoded ranked NGOs; Phase 2 will use scoring engine (distance + capacity + preference) |
| **`/route` logic** | 🟡 Stub | Returns interpolated straight-line route; Phase 2 will use nearest-neighbor ordering |
| **`/dashboard/summary` logic** | 🟡 Stub | Returns hardcoded stats; Phase 2 will aggregate from DB |
| **Rescue-window detection** | 🟡 Stub | Phase 2: rule-based lookup (category → shelf_life_hours − time_since_batch) |
| **Demand forecast model** | 🟡 Stub | Phase 2: Prophet or ARIMA trained on seeded consumption history |

### Not built (out of scope for now — P2)
- VRPTW routing solver (OR-Tools)
- Computer vision freshness detection
- Multi-role authentication
- SMS / push notifications
- LLM-generated sustainability reports (P1, not yet)

---

## 6. Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI 0.111 |
| ORM | SQLAlchemy 2.0 |
| Database | PostgreSQL via Supabase |
| Data validation | Pydantic v2 |
| Frontend framework | Next.js 14 (App Router) |
| Styling | Tailwind CSS 3 |
| Charts | Recharts 2 |
| Map | MapLibre GL JS 4 |
| Map tiles | OpenStreetMap (no API key required) |

---

## 7. Color Scheme Reference

| Token | Hex | Usage |
|---|---|---|
| Navy | `#0f172a` | Sidebar background |
| Navy 800 | `#1e293b` | Sidebar hover |
| Teal | `#0d9488` | Primary accent, CTAs |
| Teal light | `#14b8a6` | Chart lines, badges |
| Slate 50 | `#f8fafc` | Content background |

---

*Built for Smart India Hackathon 2026 · Problem Statement SIH26234*
