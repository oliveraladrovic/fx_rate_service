from datetime import datetime, timezone
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models import FXRate
from schemes import FXRateOut
from services.fx_service import collect_data

app = FastAPI()

@app.post("/rates")
async def create_fxrate(db: AsyncSession = Depends(get_db)):
    data = await collect_data()
    inserted = 0
    updated = 0
    for d in data:
        stmt = select(FXRate).where(FXRate.base_currency == d["base_currency"], FXRate.quote_currency == d["quote_currency"])
        result = await db.execute(stmt)
        existing = result.scalar_one_or_none()
        if existing:
            existing.rate = d["rate"]
            existing.timestamp = datetime.now(timezone.utc)
            inserted += 1
        else:
            db.add(FXRate(**d))
            updated += 1
    await db.commit()
    return {
        "inserted": inserted,
        "updated": updated,
        "total": inserted + updated
    }

@app.get("/rates/{base}", response_model=List[FXRateOut])
async def get_quotes(base: str, db: AsyncSession = Depends(get_db)):
    stmt = select(FXRate).where(FXRate.base_currency == base)
    result = await db.execute(stmt)
    return result.scalars().all()

@app.get("/rates/{base}/{quote}", response_model=FXRateOut)
async def get_one_quote(base: str, quote: str, db: AsyncSession = Depends(get_db)):
    stmt = select(FXRate).where(FXRate.base_currency == base, FXRate.quote_currency == quote)
    result = await db.execute(stmt)
    rate = result.scalar_one_or_none()
    if rate is None:
        raise HTTPException(status_code=404, detail="Rate not found")
    return rate