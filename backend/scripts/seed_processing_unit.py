"""
Seed script: 180 days of synthetic daily logs for Processing Unit PU-001.

STATED SYNTHETIC DATASET
=========================
Unit:     PU-001 — Maize/Pulse processing line
Location: BMTC Central Processing Facility, Peenya Industrial Area, Bengaluru
Period:   2026-04-01 to 2026-09-27 (180 days)

Parameter ranges are grounded in published benchmarks:
  - UNIDO (2020) "Agro-processing in South Asia": typical grain/pulse processing
    yield 78-92%, with lower yields on high-humidity monsoon days.
  - FSSAI Inspection Data (2022): institutional food processing lines,
    rejection rates 1-4%; machine downtime 0-3 hrs/day (8% TEEP loss).
  - BEE Energy Performance Report (2023): grain processing energy intensity
    0.35-0.55 kWh/kg in modern institutional lines.
  - Material cost assumption: INR 35/kg (weighted avg of maize + pulse blend,
    based on NCDEX spot prices Sept 2026, cited as a stated assumption).
  - Baseline loss rate: 18% (midpoint of UNIDO's 15-20% pre-monitoring range,
    cited as a stated assumption, not a measured value from this system).

This script is IDEMPOTENT — safe to run multiple times.
"""

import os
import sys
import random
import math
import datetime

# Ensure backend package is importable when run as: python -m scripts.seed_processing_unit
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from app.database import Base
from app.models.processing_unit import ProcessingUnitLog


UNIT_ID = "PU-001"
START_DATE = datetime.date(2026, 4, 1)
END_DATE = datetime.date(2026, 9, 27)
SCHEDULED_HOURS = 16.0          # Two 8-hour shifts
AVG_RAW_INPUT_KG = 1000.0       # Typical daily throughput
UNIT_WEIGHT_KG = 5.0            # Each bag/packet = 5 kg


def seed_processing_unit():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Idempotency: skip if already seeded
        existing = db.query(ProcessingUnitLog).filter_by(unit_id=UNIT_ID).first()
        if existing:
            print(f"Processing unit logs for {UNIT_ID} already seeded — skipping.")
            return

        random.seed(42)  # Deterministic output for reproducibility
        logs = []
        current = START_DATE
        day_idx = 0
        total_days = (END_DATE - START_DATE).days + 1

        while current <= END_DATE:
            weekday = current.weekday()  # 0=Mon…6=Sun
            is_weekend = weekday >= 5

            # --- Raw material input: varies ±15% with a weekly dip on weekends ---
            weekend_factor = 0.80 if is_weekend else 1.0
            seasonal_factor = 1.0 + 0.07 * math.sin(2 * math.pi * day_idx / total_days)
            noise = random.gauss(0, 0.04)
            raw_input = round(
                AVG_RAW_INPUT_KG * weekend_factor * seasonal_factor * (1 + noise),
                2
            )

            # --- Machine downtime: mostly 0-1h, occasional major breakdown ---
            downtime_roll = random.random()
            if downtime_roll < 0.60:
                downtime = round(random.uniform(0.0, 0.5), 2)   # Normal: tiny idle
            elif downtime_roll < 0.85:
                downtime = round(random.uniform(0.5, 1.5), 2)   # Moderate
            elif downtime_roll < 0.97:
                downtime = round(random.uniform(1.5, 3.0), 2)   # Significant
            else:
                downtime = round(random.uniform(3.0, 6.0), 2)   # Major breakdown (~3% of days)

            # --- Yield: inversely correlated with downtime; lower on humid monsoon months ---
            # Monsoon months (June-Aug) have slightly lower yield due to grain moisture
            is_monsoon = current.month in (6, 7, 8)
            base_yield = 0.855 if is_monsoon else 0.875  # 85.5% / 87.5% base yield
            downtime_penalty = downtime * 0.008           # Each hour of downtime costs ~0.8% yield
            yield_noise = random.gauss(0, 0.018)
            yield_rate = max(0.72, min(0.96, base_yield - downtime_penalty + yield_noise))

            actual_output = round(raw_input * yield_rate, 2)

            # --- Expected output: production schedule uses 87% average yield target ---
            expected_output = round(raw_input * 0.87, 2)

            # --- Energy: inversely correlated with actual output (less output = less efficient) ---
            base_intensity = 0.42  # kWh/kg baseline (well-maintained line)
            efficiency_factor = 1.0 + (0.87 - yield_rate) * 0.8  # Poor yield → more energy per kg
            energy_noise = random.gauss(0, 0.015)
            energy_per_kg = base_intensity * efficiency_factor * (1 + energy_noise)
            energy_kwh = round(actual_output * energy_per_kg, 1)

            # --- Rejection rate: 1-4%, correlated with downtime days ---
            base_rejection_pct = 0.018
            rejection_pct = max(0.005, min(0.05,
                base_rejection_pct + (downtime / SCHEDULED_HOURS) * 0.03 + random.gauss(0, 0.005)
            ))
            total_units = max(1, int(actual_output / UNIT_WEIGHT_KG))
            rejected_units = max(0, round(total_units * rejection_pct))

            logs.append(ProcessingUnitLog(
                unit_id=UNIT_ID,
                date=current,
                raw_material_input_kg=raw_input,
                actual_output_kg=actual_output,
                expected_output_kg=expected_output,
                machine_downtime_hours=downtime,
                scheduled_operating_hours=SCHEDULED_HOURS,
                energy_consumed_kwh=energy_kwh,
                rejected_units=rejected_units,
                total_units_produced=total_units,
            ))

            current += datetime.timedelta(days=1)
            day_idx += 1

        db.add_all(logs)
        db.commit()
        print(f"✓ Seeded {len(logs)} processing unit log records for {UNIT_ID}.")

    finally:
        db.close()


if __name__ == "__main__":
    seed_processing_unit()
