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