from pydantic_settings import BaseSettings, SettingsConfigDict

class Credenciais(BaseSettings):
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str
    api_env: str = "development"

    # Propriedade computada para gerar a string de conexão automaticamente
    @property
    def database_url(self) -> str:
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    model_config = SettingsConfigDict(env_file=".env")

# Instancia as configurações uma única vez na memória
credenciais = Credenciais()