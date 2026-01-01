from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Float, DateTime, PrimaryKeyConstraint
from datetime import datetime, timezone

Base = declarative_base()

class FXRate(Base):
    __tablename__ = "fx_rates"
    base_currency = Column(String, nullable=False)
    quote_currency = Column(String, nullable=False)
    rate = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    __table_args__ = (PrimaryKeyConstraint("base_currency", "quote_currency"),)