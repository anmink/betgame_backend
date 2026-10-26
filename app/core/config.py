from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Pflichtwerte: ohne sie startet der Server nicht
    supabase_url: str
    supabase_service_key: str
    api_football_key: str

    # Werte mit Standard: können in der .env überschrieben werden
    api_football_base_url: str = "https://v3.football.api-sports.io"
    league_id: int = 1      # vorerst WM, die Bundesliga (78) kommt in Woche 2
    season: int = 2026


settings = Settings()