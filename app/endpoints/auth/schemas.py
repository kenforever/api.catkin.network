from typing import Literal
from pydantic import BaseModel, Field, EmailStr


class get_siwe_message_data(BaseModel):
    address: str
    chain_id: int = Field(default=1, description="Ethereum mainnet chain ID")

class verify_siwe_data(BaseModel):
    address: str
    signature: str
    message: str
