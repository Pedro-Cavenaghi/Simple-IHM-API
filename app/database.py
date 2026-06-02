import asyncpg
from .dbconfig import credenciais


DB_CONFIG = {
    "host": credenciais.db_host,
    "database": credenciais.db_name,
    "user": credenciais.db_user,
    "password": credenciais.db_password,
    "port": str(credenciais.db_port)
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


async def get_db():
    pool = Database.get_pool()
    async with pool.acquire() as connection:
        yield connection