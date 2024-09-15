from sqlalchemy import Column, Integer, String, Float, DateTime, Index
from app.db.base import Base


class StockAnalysis(Base):
    __tablename__ = "stock_analysis"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, index=True)
    close = Column(Float)
    return_ = Column(Float)
    sma_10 = Column(Float)
    sma_50 = Column(Float)
    trend = Column(String)

    __table_args__ = (
        Index('ix_date', 'date', unique=True),
    )
