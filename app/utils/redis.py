import redis as redis_module
from hashlib import sha256
from fastapi import HTTPException, status

from app.utils.config import config
from app.utils.logger import logger

redis_instance = redis_module.Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    password=config.REDIS_PASSWORD,
    ssl=config.REDIS_SSL,
)

redis_logger = logger.getChild("redis")

def set_nonce_redis(address: str, nonce: str) -> True:
    try:
        redis_instance.set(
            f"nonce:{address}",
            nonce,
            ex=getattr(config, "NONCE_EXPIRY_SECONDS", 300)  # expiration time (in seconds)
        )
    except Exception as e:
        redis_logger.error(e)
        raise HTTPException(
            status_code=500,
            detail="Redis Error",
        )
    return True

def get_nonce(address: str) -> str:
    try:
        nonce = redis_instance.get(f"nonce:{address}")
        if nonce is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Nonce not found",
            )
        return nonce.decode("utf-8")
    except Exception as e:
        redis_logger.error(e)
        raise HTTPException(
            status_code=500,
            detail="Redis Error",
        )
    
def delete_nonce(address: str) -> True:
    try:
        redis_instance.delete(f"nonce:{address}")
    except Exception as e:
        redis_logger.error(e)
        raise HTTPException(
            status_code=500,
            detail="Redis Error",
        )
    return True


def add_blacklist_token(token: str) -> True:

    token = sha256(token.encode()).hexdigest()

    try:
        redis_instance.set(
            f"blacklisted:{token}", "true", ex=config.JWT_EXPIRE_MINUTES * 60
        )
    except Exception as e:
        redis_logger.error(e)
        raise HTTPException(
            status_code=500,
            detail="Redis Error",
        )
    return True


def is_token_blacklisted(token: str) -> bool:

    token = sha256(token.encode()).hexdigest()

    try:
        return redis_instance.exists(f"blacklisted:{token}") == 1
    except Exception as e:
        redis_logger.error(e)
        raise HTTPException(
            status_code=500,
            detail="Redis Error",
        )
    return False