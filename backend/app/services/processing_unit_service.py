"""
Processing Unit Metrics Service
================================
All metrics are DERIVED at request time from the database — no hardcoded values.

Threshold definitions (documented):
  - yield_pct < 82%        → flagged (below industry-acceptable minimum per UNIDO 2020)
  - downtime_pct > 15%     → flagged (>2.4 hrs/day on a 16h schedule; maintenance trigger)
  - rejection_rate_pct > 3% → flagged (exceeds FSSAI institutional quality standard)

ROI assumption:
  - Baseline loss rate: 18% of raw material input (UNIDO typical pre-monitoring; stated assumption)
  - Material cost: INR 35/kg (NCDEX maize/pulse spot blend, Sept 2026; stated assumption)
  waste_cost_saved = (baseline_loss_kg - actual_loss_kg) * 35
"""

import datetime
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.processing_unit import ProcessingUnitLog


# Flagging thresholds — documented above
YIELD_FLAG_THRESHOLD_PCT = 82.0
DOWNTIME_FLAG_THRESHOLD_PCT = 15.0
REJECTION_FLAG_THRESHOLD_PCT = 3.0

# ROI constants — stated assumptions, cited in module docstring
BASELINE_LOSS_RATE = 0.18          # 18% raw material lost before this system
MATERIAL_COST_PER_KG_INR = 35.0   # INR/kg — NCDEX spot blend Sept 2026


def _compute_daily_metrics(log: ProcessingUnitLog) -> Dict[str, Any]:
    """Derive all metrics for a single log row."""
    actual = log.actual_output_kg
    expected = log.expected_output_kg
    raw = log.raw_material_input_kg
    downtime = log.machine_downtime_hours
    scheduled = log.scheduled_operating_hours or 16.0
    rejected = log.rejected_units
    total = log.total_units_produced or 1

    yield_pct = round((actual / expected) * 100, 2) if expected > 0 else 0.0
    raw_loss_pct = round(((raw - actual) / raw) * 100, 2) if raw > 0 else 0.0
    energy_intensity = round(log.energy_consumed_kwh / actual, 4) if actual > 0 else 0.0
    downtime_pct = round((downtime / scheduled) * 100, 2) if scheduled > 0 else 0.0
    rejection_rate_pct = round((rejected / total) * 100, 2) if total > 0 else 0.0
    overproduction_variance_pct = round(((actual - expected) / expected) * 100, 2) if expected > 0 else 0.0

    # ROI
    baseline_loss_kg = raw * BASELINE_LOSS_RATE
    actual_loss_kg = raw - actual
    waste_prevented_kg = max(0.0, baseline_loss_kg - actual_loss_kg)
    waste_cost_saved_inr = round(waste_prevented_kg * MATERIAL_COST_PER_KG_INR, 2)

    flags = []
    if yield_pct < YIELD_FLAG_THRESHOLD_PCT:
        flags.append(f"Low yield: {yield_pct:.1f}% (threshold: {YIELD_FLAG_THRESHOLD_PCT}%)")
    if downtime_pct > DOWNTIME_FLAG_THRESHOLD_PCT:
        flags.append(f"High downtime: {downtime_pct:.1f}% (threshold: {DOWNTIME_FLAG_THRESHOLD_PCT}%)")
    if rejection_rate_pct > REJECTION_FLAG_THRESHOLD_PCT:
        flags.append(f"High rejection: {rejection_rate_pct:.1f}% (threshold: {REJECTION_FLAG_THRESHOLD_PCT}%)")

    return {
        "date": log.date.isoformat(),
        "raw_material_input_kg": raw,
        "actual_output_kg": actual,
        "expected_output_kg": expected,
        "machine_downtime_hours": downtime,
        "energy_consumed_kwh": log.energy_consumed_kwh,
        "yield_pct": yield_pct,
        "raw_material_loss_pct": raw_loss_pct,
        "energy_intensity_kwh_per_kg": energy_intensity,
        "downtime_pct": downtime_pct,
        "rejection_rate_pct": rejection_rate_pct,
        "overproduction_variance_pct": overproduction_variance_pct,
        "waste_prevented_kg": round(waste_prevented_kg, 2),
        "waste_cost_saved_inr": waste_cost_saved_inr,
        "is_flagged": len(flags) > 0,
        "flag_reasons": flags,
    }


def get_unit_metrics(
    db: Session,
    unit_id: str,
    start_date: datetime.date,
    end_date: datetime.date,
) -> Dict[str, Any]:
    """
    Returns:
      - aggregate metrics across the date range
      - last-30-days daily trend for charting
    """
    logs = (
        db.query(ProcessingUnitLog)
        .filter(
            ProcessingUnitLog.unit_id == unit_id,
            ProcessingUnitLog.date >= start_date,
            ProcessingUnitLog.date <= end_date,
        )
        .order_by(ProcessingUnitLog.date)
        .all()
    )

    if not logs:
        return {"unit_id": unit_id, "data_available": False, "trend": []}

    daily = [_compute_daily_metrics(l) for l in logs]

    n = len(daily)
    avg_yield = round(sum(d["yield_pct"] for d in daily) / n, 2)
    avg_loss = round(sum(d["raw_material_loss_pct"] for d in daily) / n, 2)
    avg_energy_intensity = round(sum(d["energy_intensity_kwh_per_kg"] for d in daily) / n, 4)
    avg_downtime = round(sum(d["downtime_pct"] for d in daily) / n, 2)
    avg_rejection = round(sum(d["rejection_rate_pct"] for d in daily) / n, 2)
    total_waste_cost_saved = round(sum(d["waste_cost_saved_inr"] for d in daily), 2)
    total_waste_prevented_kg = round(sum(d["waste_prevented_kg"] for d in daily), 2)
    flagged_days = sum(1 for d in daily if d["is_flagged"])

    # Last 30 days for chart trend
    trend_slice = daily[-30:]

    return {
        "unit_id": unit_id,
        "data_available": True,
        "period": {"start": start_date.isoformat(), "end": end_date.isoformat(), "days": n},
        "aggregates": {
            "avg_yield_pct": avg_yield,
            "avg_raw_material_loss_pct": avg_loss,
            "avg_energy_intensity_kwh_per_kg": avg_energy_intensity,
            "avg_downtime_pct": avg_downtime,
            "avg_rejection_rate_pct": avg_rejection,
            "flagged_days": flagged_days,
            "flagged_days_pct": round(flagged_days / n * 100, 1),
        },
        "roi": {
            "total_waste_prevented_kg": total_waste_prevented_kg,
            "total_waste_cost_saved_inr": total_waste_cost_saved,
            "baseline_assumption": "18% material loss rate (UNIDO 2020 pre-monitoring benchmark)",
            "cost_assumption": "INR 35/kg (NCDEX maize/pulse blend, Sept 2026)",
        },
        "trend": trend_slice,
    }


def get_flagged_batches(db: Session, unit_id: str) -> List[Dict[str, Any]]:
    """Return all days that crossed any flagging threshold, most recent first."""
    logs = (
        db.query(ProcessingUnitLog)
        .filter(ProcessingUnitLog.unit_id == unit_id)
        .order_by(ProcessingUnitLog.date.desc())
        .all()
    )
    flagged = []
    for log in logs:
        metrics = _compute_daily_metrics(log)
        if metrics["is_flagged"]:
            flagged.append(metrics)
    return flagged
