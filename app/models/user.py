from pydantic import BaseModel
from typing import Optional

class User_Data(BaseModel):
    address: str
    exp: Optional[int] = None
