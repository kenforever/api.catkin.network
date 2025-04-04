from pydantic import BaseModel, Field, EmailStr


# class Token_Data(BaseModel):
#     uid: str
#     local_id: str


class User_Data(BaseModel):
    address: str
