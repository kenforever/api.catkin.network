from typing import Literal, Optional
from pydantic import BaseModel, Field, EmailStr


class get_siwe_message_data(BaseModel):
    address: str
    chain_id: int = Field(default=1, description="Ethereum mainnet chain ID")

class verify_siwe_data(BaseModel):
    address: str
    signature: str
    message: str

# 產品創建模型
class ProductCreate(BaseModel):
    image_uri: Optional[str] = None
    title: str
    description: Optional[str] = None
    price: int

# 產品更新模型
class ProductUpdate(BaseModel):
    image_uri: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None

# 產品返回模型
class ProductResponse(BaseModel):
    id: int
    created_at: str
    owner: str
    image_uri: Optional[str] = None
    title: str
    description: Optional[str] = None
    price: int