import os
from supabase import create_client, Client
from supabase.client import ClientOptions
from fastapi import HTTPException, status

from app.utils.config import config
from app.utils.logger import logger

supabase_logger = logger.getChild("supabase")

supabase: Client = create_client(
    supabase_key=config.SUPABASE_SERVICE_KEY,
    supabase_url=config.SUPABASE_URL,
    options=ClientOptions(
        schema=config.DATABASE_SCHEMA,
    ),
)

# database
user_info_db = supabase.table("user_info")
product_info_db = supabase.table("product_info")
payment_db = supabase.table("payment")

# groups_db = supabase.table("groups")
# permissions_db = supabase.table("permissions")
# role_permission_db = supabase.table("role_permission")
# roles_db = supabase.table("roles")
# user_roles_db = supabase.table("user_roles")
# courses_db = supabase.table("courses")
# contents_db = supabase.table("contents")
# private_courses_viewable_db = supabase.table("private_courses_viewable")
# group_images_db = supabase.table("group_images")
# user_content_view_logs_db = supabase.table("user_content_view_logs")
# user_login_logs_db = supabase.table("user_login_logs")
# user_course_view_logs_db = supabase.table("user_course_view_logs")
# category_info_db = supabase.table("category_info")
# category_courses_db = supabase.table("category_courses")
# landing_page_db = supabase.table("landing_page")
# course_tutors_db = supabase.table("course_tutors")
# course_tags_db = supabase.table("course_tags")
# tutor_info_db = supabase.table("tutor_info")
# tag_info_db = supabase.table("tag_info")
# group_tags_db = supabase.table("group_tags")
# daily_checkin_db = supabase.table("daily_checkin")
# coupon_db = supabase.table("coupon")
# transactions_db = supabase.table("transactions")
# user_unlocked_courses_db = supabase.table("user_unlocked_courses")
# address_book_db = supabase.table("address_book")
