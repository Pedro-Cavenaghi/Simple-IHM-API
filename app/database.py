import asyncpg
from .dbconfig import credenciais

# Agora os dados vêm do arquivo .env de forma dinâmica e segura
DB_CONFIG = {
    "host": credenciais.db_host,
    "database": credenciais.db_name,
    "user": credenciais.db_user,
    "password": credenciais.db_password,
    "port": str(credenciais.db_port)  # asyncpg aceita string ou int, mas manter o padrão original é bom
}

class Database:
    pool = None

    @classmethod
    def get_pool(cls):
        if cls.pool is None:
            raise RuntimeError("O Pool de conexões não foi inicializado!")
        return cls.pool

    @classmethod
    async def connect(cls):
        print("--- Inicializando Pool de Conexões Otimizado (asyncpg) ---")
        # Mantém 5 conexões abertas sempre, escalando até 20 em picos de requisições da ESP32/React
        cls.pool = await asyncpg.create_pool(
            **DB_CONFIG,
            min_size=5,
            max_size=20
        )

    @classmethod
    async def disconnect(cls):
        if cls.pool:
            print("--- Fechando Pool de Conexões com Segurança ---")
            await cls.pool.close()

# Injeção de dependência para o FastAPI usar nas rotas
async def get_db():
    pool = Database.get_pool()
    async with pool.acquire() as connection:
        yield connection