import supabase_service
from datetime import datetime, timedelta

supabase = supabase_service.SupabaseService().client

def cleanup_old_logs():
    # Calculate timestamp for 20 minutes ago
    twenty_minutes_ago = datetime.utcnow() - timedelta(minutes=20)
    iso_timestamp = twenty_minutes_ago.isoformat()
    
    # Delete rows older than 20 minutes
    result = supabase.table('log-monitor').delete().lt('created_at', iso_timestamp).execute()
    
    return result

if __name__ == "__main__":
    cleanup_old_logs()