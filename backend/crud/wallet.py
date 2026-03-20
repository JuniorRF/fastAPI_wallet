from backend.core.db import AsyncSessionLocal
from backend.models.wallet import Wallet
from backend.schemas.wallet import WalletCreate


async def create_meeting_room(
        new_room: WalletCreate
) -> Wallet:
    wallet_data = new_room.dict()

    db_wallet = Wallet(**wallet_data)

    async with AsyncSessionLocal() as session:
        session.add(db_wallet)
        await session.commit()

        await session.refresh(db_wallet)
    return db_wallet
