from supabase import create_client
from app.core.config import settings

SUPABASE_URL = settings.supabase_url
SUPABASE_KEY = settings.supabase_service_key

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)