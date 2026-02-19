from sqlalchemy import Column, Numeric, Uuid


from backend.core.db import Base


class Wallet(Base):
    uuid = Column(Uuid, unique=True, nullable=False)
    balance = Column(Numeric(precision=10, scale=2), nullable=False, default=0)
