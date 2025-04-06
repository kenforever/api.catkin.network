import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from siwe import SiweMessage
from datetime import datetime, timedelta

# from app.utils.access.main import verify_token
from app.utils.redis import get_nonce, delete_nonce
from app.utils.config import config

from .schemas import get_siwe_message_data, verify_siwe_data
from .services import set_nonce, get_user
from app.utils.logger import logger
from fastapi import Request
from app.utils.access import verify_token
from app.models.user import User_Data
from app.utils.supabase import user_info_db

router = APIRouter()
@router.post("/get_siwe_message")
async def get_siwe_message(request: Request, data: get_siwe_message_data):
    nonce = set_nonce(data.address)

    statement = "Sign in with Ethereum to the app"
    message = SiweMessage(
        domain=config.APP_DOMAIN,
        address=data.address,
        statement=statement,
        uri=str(request.url),
        version="1",
        chain_id=data.chain_id,  # e.g., Ethereum mainnet Chain ID
        nonce=nonce,  # randomly generated nonce to prevent replay attacks
        issued_at=datetime.utcnow().isoformat() + "Z"  # current UTC time
    )
    response = {
        "message": message.prepare_message()
    }
    return response


@router.post("/verify_siwe")
async def verify_siwe(data: verify_siwe_data):
    """
    Verify the signature and nonce.
    """
    # Verify the signature
    siwe_message = SiweMessage.from_message(data.message)
    try:
        siwe_message.verify(data.signature)
    except Exception as e:
        logger.error(e)
        return {"message": "Signature verification failed"}

    # Verify the nonce
    if siwe_message.nonce != get_nonce(data.address):
        return {"message": "Nonce verification failed"}

    # Delete the nonce
    delete_nonce(data.address)

    # get_user
    get_user(data.address)

    # Generate JWT token
    token = jwt.encode(
        {
            "address": data.address,
            "exp": datetime.utcnow() + timedelta(minutes=config.JWT_EXPIRE_MINUTES),
        },
        config.JWT_SECRET,
        algorithm="HS256",
    )

    return {"token": token}

@router.get("/me")
async def me(token_payload: User_Data = Depends(verify_token)):
    # get user info from db
    try:
        user_info = user_info_db.select("*").eq("address", token_payload.address).execute()
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Failed to get user info")

    response = user_info.data[0]
    return response