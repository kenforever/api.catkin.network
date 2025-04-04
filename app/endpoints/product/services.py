import os
from app.utils.redis import set_nonce_redis, get_nonce, delete_nonce
from app.utils.supabase import user_info_db
from app.utils.supabase import supabase

# 添加產品資料表
product_info_db = supabase.table("product_info")

def gernate_nonce() -> str:
    """
    Generate a random nonce for the user.
    """
    nonce = os.urandom(16).hex()
    return nonce

def save_nonce(address: str, nonce: str) -> True:
    """
    Save the nonce to Redis.
    """
    return set_nonce_redis(address, nonce)

def set_nonce(address: str) -> str:
    """
    Set the nonce for the user.
    """
    nonce = gernate_nonce()
    save_nonce(address, nonce)
    return nonce

def create_user(address: str) -> dict:
    """
    Create a user in the database.
    """
    # Assuming you have a function to create a user in your database
    # This is a placeholder implementation
    user_data = {
        "address": address,
    }

    # Save user data to the database 
    user_info_db.insert(user_data).execute()

    response = user_info_db.select("*").eq("address", address).execute()

    return response

def get_user(address: str) -> dict:
    """
    Get user data from the database.
    """
    # Assuming you have a function to get user data from your database
    # This is a placeholder implementation
    user_data = user_info_db.select("*").eq("address", address).execute().data

    if user_data == []:
        user_data = create_user(address).data
    
    print(user_data)

    return user_data
