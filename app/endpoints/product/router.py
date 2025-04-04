import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from siwe import SiweMessage
from datetime import datetime, timedelta
from typing import List, Optional

from app.utils.access import verify_token
from app.utils.redis import get_nonce, delete_nonce
from app.utils.config import config

from .schemas import get_siwe_message_data, verify_siwe_data, ProductCreate, ProductUpdate, ProductResponse
from .services import set_nonce, get_user, product_info_db
from app.utils.logger import logger
from fastapi import Request
from app.models.user import User_Data


router = APIRouter()

# 創建產品
@router.post("/product", response_model=ProductResponse)
async def create_product(
    product: ProductCreate, 
    token_payload: User_Data = Depends(verify_token)
):
    """
    創建新產品
    """
    # 準備產品資料，添加擁有者
    product_data = product.dict()
    product_data["owner"] = token_payload.address
    
    # 插入資料庫
    try:
        result = product_info_db.insert(product_data).execute()
        if result.data and len(result.data) > 0:
            return result.data[0]
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="無法創建產品"
            )
    except Exception as e:
        logger.error(f"創建產品失敗: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"創建產品時發生錯誤: {str(e)}"
        )

# 獲取所有產品
@router.get("/products", response_model=List[ProductResponse])
async def get_products():
    """
    獲取所有產品列表
    """
    try:
        result = product_info_db.select("*").execute()
        return result.data
    except Exception as e:
        logger.error(f"獲取產品列表失敗: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"獲取產品列表時發生錯誤: {str(e)}"
        )

# 獲取單個產品
@router.get("/product/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int):
    """
    獲取單個產品詳情
    """
    try:
        result = product_info_db.select("*").eq("id", product_id).execute()
        if result.data and len(result.data) > 0:
            return result.data[0]
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"找不到 ID 為 {product_id} 的產品"
            )
    except Exception as e:
        logger.error(f"獲取產品詳情失敗: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"獲取產品詳情時發生錯誤: {str(e)}"
        )

# 更新產品
@router.put("/product/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int, 
    product: ProductUpdate, 
    token_payload: User_Data = Depends(verify_token)
):
    """
    更新產品資訊
    """
    # 先檢查產品是否存在並屬於該用戶
    try:
        check_result = product_info_db.select("*").eq("id", product_id).execute()
        if not check_result.data or len(check_result.data) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"找不到 ID 為 {product_id} 的產品"
            )
        
        # 檢查產品擁有者
        if check_result.data[0]["owner"] != token_payload.address:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="您無權更新此產品"
            )
        
        # 準備更新資料
        update_data = {k: v for k, v in product.dict().items() if v is not None}
        
        # 更新資料庫
        result = product_info_db.update(update_data).eq("id", product_id).execute()
        
        if result.data and len(result.data) > 0:
            return result.data[0]
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="無法更新產品"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新產品失敗: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新產品時發生錯誤: {str(e)}"
        )

# 刪除產品
@router.delete("/product/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int, 
    token_payload: User_Data = Depends(verify_token)
):
    """
    刪除產品
    """
    # 先檢查產品是否存在並屬於該用戶
    try:
        check_result = product_info_db.select("*").eq("id", product_id).execute()
        if not check_result.data or len(check_result.data) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"找不到 ID 為 {product_id} 的產品"
            )
        
        # 檢查產品擁有者
        if check_result.data[0]["owner"] != token_payload.address:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="您無權刪除此產品"
            )
        
        # 刪除產品
        product_info_db.delete().eq("id", product_id).execute()
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"刪除產品失敗: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"刪除產品時發生錯誤: {str(e)}"
        )

# 獲取用戶自己的產品
@router.get("/my-products", response_model=List[ProductResponse])
async def get_my_products(token_payload: User_Data = Depends(verify_token)):
    """
    獲取當前登入用戶的所有產品
    """
    try:
        result = product_info_db.select("*").eq("owner", token_payload.address).execute()
        return result.data
    except Exception as e:
        logger.error(f"獲取用戶產品失敗: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"獲取用戶產品時發生錯誤: {str(e)}"
        )

# 搜索產品
@router.get("/products/search", response_model=List[ProductResponse])
async def search_products(
    query: str = "",
    min_price: Optional[int] = None,
    max_price: Optional[int] = None
):
    """
    搜索產品，支持按關鍵字、價格範圍過濾
    
    參數:
    - query: 搜索關鍵字，會匹配標題和描述
    - min_price: 最低價格
    - max_price: 最高價格
    """
    try:
        # 初始查詢
        search_query = product_info_db.select("*")
        
        # 關鍵字搜索 (匹配標題或描述)
        if query:
            search_query = search_query.or_(f'title.ilike.%{query}%,description.ilike.%{query}%')
        
        # 價格範圍過濾
        if min_price is not None:
            search_query = search_query.gte("price", min_price)
        
        if max_price is not None:
            search_query = search_query.lte("price", max_price)
        
        # 執行查詢
        result = search_query.execute()
        
        return result.data
    except Exception as e:
        logger.error(f"搜索產品失敗: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"搜索產品時發生錯誤: {str(e)}"
        )
