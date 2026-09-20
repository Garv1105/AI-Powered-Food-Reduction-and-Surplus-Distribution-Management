from sqlalchemy import Column, Integer, String, Float, Date, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from app.database import Base


class ProcessingUnitLog(Base):
    """
    Daily efficiency log for a food processing unit.

    Synthetic dataset — 6 months of daily logs for Unit PU-001 (Maize/Pulse
    processing line at BMTC Central Processing Facility, Peenya Industrial Area,
    Bengaluru). Ranges grounded in published FSSAI & UNIDO food-processing
    benchmarks for small-scale institutional units in South India.
    See backend/data/PROCESSING_UNIT_DATASET_NOTES.md for full assumptions.
    """
    __tablename__ = "processing_unit_logs"

    id = Column(Integer, primary_key=True, index=True)
    unit_id = Column(String(50), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)

    # Raw materials (kg) fed into the processing line
    raw_material_input_kg = Column(Float, nullable=False)

    # Actual processed output (kg) — after cleaning, sorting, packaging
    actual_output_kg = Column(Float, nullable=False)

    # Target / planned output (kg) — set from production schedule
    expected_output_kg = Column(Float, nullable=False)

    # Machine downtime (hours) within the scheduled operating window
    machine_downtime_hours = Column(Float, nullable=False, default=0.0)

    # Total hours the facility was scheduled to operate
    scheduled_operating_hours = Column(Float, nullable=False, default=16.0)

    # Electricity consumed (kWh) for the full shift
    energy_consumed_kwh = Column(Float, nullable=False)

    # Units (bags/packets) rejected during quality check
    rejected_units = Column(Integer, nullable=False, default=0)

    # Total units (bags/packets) produced before quality check
    total_units_produced = Column(Integer, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("unit_id", "date", name="uq_processing_unit_log_unit_date"),
    )
