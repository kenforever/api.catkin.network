from typing import Literal
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class get_tx_calldata_data(BaseModel):
    src_token: str
    src_address: str
    src_network: str
    amount: str
    product_id: Optional[str] = None
    user_alias: Optional[str] = None

class UpdatePaymentData(BaseModel):
    payment_id: str
    product_id: Optional[int] = None
    tx_hash: Optional[str] = None
    user_alias: Optional[str] = None
    status: Optional[str] = None
    type: Optional[str] = None
    attestation: Optional[str] = None
    sourceChainId: Optional[int] = None