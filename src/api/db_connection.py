# src/api/db_connection.py
import mysql.connector
from mysql.connector import pooling
import os
from dotenv import load_dotenv

load_dotenv()

try:
    # Crear un "pool" de conexiones para reutilizarlas y ser más eficiente
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

def get_db_connection():
    """
    Obtiene una conexión del pool.
    Esta función será usada por los endpoints de la API.
    """
    if connection_pool:
        return connection_pool.get_connection()
    return None