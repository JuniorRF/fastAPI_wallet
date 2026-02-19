import uuid

from pydantic import BaseModel, Field


class WalletCreate(BaseModel):
    uuid: uuid.UUID = Field(default_factory=uuid.uuid4)
