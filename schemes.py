from pydantic import BaseModel, ConfigDict
from datetime import datetime

class FXRateOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    base_currency: str
    quote_currency: str
    rate: float
    timestamp: datetime