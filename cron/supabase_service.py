from supabase import create_client, Client

class SupabaseService:
    def __init__(self):
        self.url = "SUPABASE_URL"
        self.key = "SUPABASE_KEY"
        self.client: Client = create_client(self.url, self.key)
