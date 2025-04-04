from app.utils.config import config
from app.utils.supabase import supabase
from app.utils.logger import logger
from app.utils.redis import is_token_blacklisted
from app.utils.schema import User_Data

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt 
import time
from fastapi import HTTPException

access_logger = logger.getChild("access")

def verify_token(
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> User_Data:

    try:
        payload = jwt.decode(token.credentials, config.JWT_SECRET, algorithms=["HS256"])

    except Exception as e:
        access_logger.error(e)
        raise HTTPException(status_code=401, detail="Invalid token")

    if payload.get("exp") < int(time.time()):
        raise HTTPException(status_code=401, detail="Invalid token")

    if is_token_blacklisted(token.credentials):
        raise HTTPException(status_code=401, detail="Invalid token")

    address = payload.get("address")
    response = User_Data(
        address = address,
    )

    return response
