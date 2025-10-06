# src/api/db_connection.py
import mysql.connector
from mysql.connector import pooling
from mysql.connector.pooling import PooledMySQLConnection
from fastapi import HTTPException, status
import os
from dotenv import load_dotenv

load_dotenv()

try:
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name="propiedades_pool",
        pool_size=5,
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    print("✅ Pool de conexiones a la base de datos creado exitosamente.")

except mysql.connector.Error as e:
    print(f"❌ Error al crear el pool de conexiones: {e}")
    connection_pool = None

def get_db_connection() -> PooledMySQLConnection:
    """
    Obtiene una conexión del pool.
    El tipo de retorno ahora es más específico.
    """
    if connection_pool:
        return connection_pool.get_connection()
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="No se pudo establecer conexión con la base de datos (pool no disponible)"
    )

def get_db_cursor():
    """
    Dependencia de FastAPI que gestiona el ciclo de vida de la conexión y el cursor.
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        yield cursor
    except mysql.connector.Error as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error de base de datos: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

