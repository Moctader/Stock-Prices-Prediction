from sqlalchemy import Column, Integer, String, Float, DateTime, Index
from app.db.base import Base


class StockPrice(Base):
    __tablename__ = "stock_price"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, index=True)
    exchange_short_name = Column(String)
    date = Column(DateTime, index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    adjusted_close = Column(Float)
    volume = Column(Integer)
    prev_close = Column(Float)
    change = Column(Float)
    change_p = Column(Float)
    mid_price = Column(Float)
    volatility = Column(Float)
    future_price = Column(Float)
    price_increase = Column(Integer)
    version = Column(String, index=True)
    dataset_type = Column(String, index=True)  # 'train', 'validation', 'test'

    __table_args__ = (
        Index('ix_code_date', 'code', 'date', unique=True),
    )
