from sqlalchemy import Column, Integer, String, Float, DateTime
from app.db.base import Base


class FinancialData(Base):
    __tablename__ = "financial_data"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, index=True)
    exchange_short_name = Column(String)
    date = Column(DateTime)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    adjusted_close = Column(Float)
    volume = Column(Integer)
    prev_close = Column(Float)
    change = Column(Float)
    change_p = Column(Float)
