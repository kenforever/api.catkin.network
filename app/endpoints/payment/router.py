from typing import Optional
import jwt
from fastapi import APIRouter, Depends, HTTPException
import shortuuid

from app.utils.logger import logger
from fastapi import Request
from app.utils.supabase import payment_db

"""
- return calldata by:
1. src address
2. src token
3. src network
4. src amount for src token
5. product id / user alias

- register txid by payment id
- get status by txid / payment id
- 
"""


router = APIRouter()

@router.get("/new")
async def new_payment(
    product_id: Optional[str] = None,
    user_alias: Optional[str] = None,
):
    """
    Create a new payment
    """
    # check if product id and user alias are valid
    # if not, raise error
    if not product_id and not user_alias:
        raise HTTPException(
            status_code=400,
            detail="product_id and user_alias are empty"
        )
    
    if product_id and user_alias:
        raise HTTPException(
            status_code=400,
            detail="product_id and user_alias are both provided"
        )

    # create a new payment
    # return payment id
    try:
        insert_data = {}
        if product_id:
            insert_data["product_id"] = product_id
        if user_alias:
            insert_data["user_alias"] = user_alias
        # insert data into payment_db

        payment_id = shortuuid.uuid()
        insert_data["payment_id"] = payment_id

        result = payment_db.insert(insert_data).execute()
        if result.data and len(result.data) > 0:
            return result.data[0]
        else:
            raise HTTPException(
                status_code=500,
                detail="Unable to create payment"
            )
    except Exception as e:
        logger.error(f"Create payment failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error occurred while creating payment: {str(e)}"
        )

@router.get("/tx/submit")
async def submit_tx(
    payment_id: str,
    tx_hash: str,
):
    """
    Submit the transaction hash
    """
    # check if payment id is valid
    # if not, raise error
    if not payment_id:
        raise HTTPException(
            status_code=400,
            detail="payment_id is empty"
        )

    # update the payment with the tx hash
    try:
        result = payment_db.update({"tx_hash": tx_hash}).eq("payment_id", payment_id).execute()
        if result.data and len(result.data) > 0:
            return result.data[0]
        else:
            raise HTTPException(
                status_code=500,
                detail="Unable to update payment"
            )
    except Exception as e:
        logger.error(f"Submit transaction failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error occurred while submitting transaction: {str(e)}"
        )
    

@router.get("{payment_id}/status")
async def get_tx_status(
    payment_id: str,
):
    """
    Get the transaction status
    """
    # check if payment id is valid
    # if not, raise error
    if not payment_id:
        raise HTTPException(
            status_code=400,
            detail="payment_id is empty"
        )

    # get the payment status
    try:
        result = payment_db.select("*").eq("payment_id", payment_id).execute()
        if result.data and len(result.data) > 0:
            return result.data[0]
        else:
            raise HTTPException(
                status_code=404,
                detail="Payment not found"
            )
    except Exception as e:
        logger.error(f"Get transaction status failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error occurred while getting transaction status: {str(e)}"
        )




# @router.post("/get_calldata")
# async def get_tx_calldata(
#     data: get_tx_calldata_data,
# ):
    
#     # if product id and user alias are empty
#     # raise error
#     if not data.product_id and not data.user_alias:
#         raise HTTPException(
#             status_code=400,
#             detail="product_id and user_alias are empty"
#         )

#     income_user_address = data.income_user_address

#     # check allowance 
#     # if not enough, raise error 




#     # determine the how to finish the tx
#     # 1. if the src token and dest token are USDC, 
#     # and the network in: avax, base, ethereum, linea,
#     # use CCTP

#     # else, use 1inch fusion+



# async def get_siwe_message(request: Request, data: get_siwe_message_data):
#     nonce = set_nonce(data.address)

#     statement = "Sign in with Ethereum to the app"
#     message = SiweMessage(
#         domain=config.APP_DOMAIN,
#         address=data.address,
#         statement=statement,
#         uri=str(request.url),
#         version="1",
#         chain_id=data.chain_id,  # e.g., Ethereum mainnet Chain ID
#         nonce=nonce,  # randomly generated nonce to prevent replay attacks
#         issued_at=datetime.utcnow().isoformat() + "Z"  # current UTC time
#     )
#     response = {
#         "message": message.prepare_message()
#     }
#     return response


# @router.post("/verify_siwe")
# async def verify_siwe(data: verify_siwe_data):
#     """
#     Verify the signature and nonce.
#     """
#     # Verify the signature
#     siwe_message = SiweMessage.from_message(data.message)
#     try:
#         siwe_message.verify(data.signature)
#     except Exception as e:
#         logger.error(e)
#         return {"message": "Signature verification failed"}

#     # Verify the nonce
#     if siwe_message.nonce != get_nonce(data.address):
#         return {"message": "Nonce verification failed"}

#     # Delete the nonce
#     delete_nonce(data.address)

#     # get_user
#     get_user(data.address)

#     # Generate JWT token
#     token = jwt.encode(
#         {
#             "address": data.address,
#             "exp": datetime.utcnow() + timedelta(minutes=config.JWT_EXPIRE_MINUTES),
#         },
#         config.JWT_SECRET,
#         algorithm="HS256",
#     )

#     return {"token": token}
