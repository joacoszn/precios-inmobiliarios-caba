# scripts/poblar_db.py
import pandas as pd
import mysql.connector
from mysql.connector import Error
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.connection import MySQLConnection
import re
import ast
from typing import Dict, Any, Optional, List
import unicodedata
import os
from dotenv import load_dotenv

load_dotenv()

DATA_FILE_PATH = './data/ventas_deptos.pkl' 

def conectar_db() -> Optional[MySQLConnectionAbstract]:
    """
    Establece la conexión con la base de datos MySQL usando variables de entorno.
    """
    try:
        conexion = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        if conexion.is_connected():
            print("✅ Conexión a la base de datos MySQL exitosa.")
            return conexion
    except Error as e:
        print(f"❌ Error al conectar a MySQL: {e}")
        return None

def leer_datos_crudos(path: str) -> Optional[pd.DataFrame]:
    """
    Lee los datos crudos desde el archivo .pkl.
    """
    try:
        df = pd.read_pickle(path)
        print(f"✅ {len(df)} registros leídos correctamente desde {path}.")
        return df
    except FileNotFoundError:
        print(f"❌ Error: El archivo no se encontró en la ruta especificada: {path}")
        return None

def limpiar_y_validar_precio(precio_original: Any) -> Optional[float]:
    if not isinstance(precio_original, str) or precio_original.strip() == "":
        return None
    
    precio_limpio = precio_original.strip().upper().replace("USD", "").replace(".", "").strip()
    
    try:
        precio_numerico = float(precio_limpio)
        if precio_numerico < 10000:
            return None
        return precio_numerico
    except (ValueError, TypeError):
        return None

def limpiar_y_validar_expensas(expensa_original: Any) -> Optional[float]:
    if not isinstance(expensa_original, str) or expensa_original.strip() == "":
        return None
    
    expensa_limpia = expensa_original.strip().upper().replace("ARS", "").replace("$", "").replace(".", "").replace("EXPENSAS", "").strip()
    
    try:
        expensa_numerica = float(expensa_limpia)
        if expensa_numerica < 100:
            return None
        # Validacion contra el limite de la BBDD (DECIMAL 10,2)
        if expensa_numerica >= 100_000_000:
            return None
        return expensa_numerica
    except (ValueError, TypeError):
        return None

def normalizar_texto(texto: str) -> str:
    """Elimina tildes y convierte a minúsculas."""
    nfkd_form = unicodedata.normalize('NFKD', texto)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)]).lower()

def estandarizar_barrio(location_original: Any) -> Optional[str]:
    if not isinstance(location_original, str):
        return None

    # Mapa de barrios oficiales para validación y normalización
    barrios_oficiales = [
        "Recoleta", "Palermo", "Belgrano", "Caballito", "Almagro", "Villa Crespo",
        "Nuñez", "Saavedra", "Villa Urquiza", "Flores", "San Nicolas", "Retiro",
        "Balvanera", "Monserrat", "San Telmo", "La Boca", "Barracas", "Constitucion",
        "Parque Patricios", "Boedo", "San Cristobal", "Liniers", "Mataderos",
        "Villa Lugano", "Villa Riachuelo", "Villa Soldati", "Pompeya", "Parque Chacabuco",
        "Parque Avellaneda", "Versalles", "Villa Real", "Monte Castro", "Villa Devoto",
        "Villa del Parque", "Villa Santa Rita", "Agronomia", "Chacarita", "Paternal",
        "Villa Ortuzar", "Coghlan", "Colegiales", "Puerto Madero", "Parque Chas", 
        "Floresta", "Villa Luro", "Villa Pueyrredon", "Villa General Mitre", "Velez Sarsfield"
    ]
    barrios_oficiales_norm = {normalizar_texto(b): b for b in barrios_oficiales}

    mapa_excepciones = {
        "barrio norte": "Recoleta", "centro / microcentro": "San Nicolas",
        "congreso": "Balvanera", "once": "Balvanera", "abasto": "Almagro",
        "parque centenario": "Caballito", "tribunales": "San Nicolas",
        "la paternal": "Paternal", "catalinas": "Retiro"
    }
    location_normalizada = normalizar_texto(location_original.split(',')[0].strip())
    if location_normalizada in mapa_excepciones:
        return mapa_excepciones[location_normalizada].title()

    if ',' in location_original:
        partes = location_original.split(',')
        if len(partes) > 1:
            posible_barrio = partes[1].strip()
            posible_barrio_norm = normalizar_texto(posible_barrio)
            # PASO 3: Validar que el resultado sea un barrio oficial.
            if posible_barrio_norm in barrios_oficiales_norm:
                return barrios_oficiales_norm[posible_barrio_norm]

    if location_normalizada in barrios_oficiales_norm:
        return barrios_oficiales_norm[location_normalizada]
    
    return None

def parsear_features(features_list: Any) -> Dict[str, Optional[int]]:
    
    parsed_data: Dict[str, Optional[int]] = {
        'ambientes': None, 'dormitorios': None, 'banos': None,
        'superficie_total_m2': None, 'cocheras': None
    }

    if not isinstance(features_list, list):
        return parsed_data

    for item in features_list:
        if not isinstance(item, str):
            continue
        
        item_lower = item.lower()
        
        try:
            match = re.search(r'\d+', item_lower)
            if match:
                numero = int(match.group())
                
                if 'amb.' in item_lower:
                    parsed_data['ambientes'] = numero
                elif 'dorm.' in item_lower:
                    parsed_data['dormitorios'] = numero
                elif 'baño' in item_lower:
                    parsed_data['banos'] = numero
                elif 'm² tot.' in item_lower:
                    parsed_data['superficie_total_m2'] = numero
                elif 'coch.' in item_lower:
                    parsed_data['cocheras'] = numero
        except ValueError:
            continue
            
    return parsed_data

def transformar_datos(df: pd.DataFrame) -> pd.DataFrame:
    print("ETL: Iniciando Fase de Transformación...")
    
    df_transformado = pd.DataFrame()
    
    df_transformado['price_usd'] = df['Price'].apply(limpiar_y_validar_precio)
    print(f"  - Columna 'Price' transformada. Registros inválidos: {df_transformado['price_usd'].isnull().sum()}")

    df_transformado['expensas_ars'] = df['Expensas'].apply(limpiar_y_validar_expensas)
    nulos_antes = df_transformado['expensas_ars'].isnull().sum()
    print(f"  - Columna 'Expensas' transformada. Registros nulos/inválidos antes de imputar: {nulos_antes}")
    
    mediana_expensas = df_transformado['expensas_ars'].median()
    df_transformado['expensas_ars'] = df_transformado['expensas_ars'].fillna(mediana_expensas)
    print(f"  - Valores nulos de 'expensas_ars' imputados con la mediana: ${mediana_expensas:,.2f} ARS")

    df_transformado['barrio'] = df['Location'].apply(estandarizar_barrio)
    print(f"  - Columna 'Location' estandarizada a 'barrio'. Registros no mapeados: {df_transformado['barrio'].isnull().sum()}")

    features_df = df['Features'].apply(parsear_features).apply(pd.Series)
    df_transformado = pd.concat([df_transformado, features_df], axis=1)
    print("  - Parseando columna 'Features'...")
    for col in ['ambientes', 'dormitorios', 'banos', 'superficie_total_m2', 'cocheras']:
        print(f"    - {col.replace('_', ' ').capitalize()} extraídos: {df_transformado[col].notnull().sum()}")

    for col in ['ambientes', 'dormitorios', 'banos', 'cocheras']:
        df_transformado[col] = df_transformado[col].fillna(0).astype(int)

    columnas_originales = ['id', 'Address', 'Description', 'Link', 'scrap_date']
    df_transformado[columnas_originales] = df[columnas_originales]
    df_transformado.rename(columns={'Address': 'address', 'Description': 'description', 'Link': 'link'}, inplace=True)
    
    print("ETL: Fase de Transformación completada.")
    return df_transformado

def cargar_datos(df: pd.DataFrame, conn: MySQLConnectionAbstract, batch_size: int = 1000):
    print("ETL: Iniciando Fase de Carga...")
    cursor = None
    try:
        cursor = conn.cursor()
        
        columnas_finales = [
            'source_id', 'price_usd', 'expensas_ars', 'barrio', 'address', 
            'ambientes', 'dormitorios', 'banos', 'superficie_total_m2', 
            'cocheras', 'description', 'link', 'scrap_date'
        ]
        
        df_final = df.rename(columns={'id': 'source_id'})
        df_final = df_final.dropna(subset=['price_usd', 'barrio'])
        
        registros_descartados = len(df) - len(df_final)
        print(f"  - Se descartaron {registros_descartados} registros por tener precio o barrio nulos.")

        df_para_cargar = df_final[columnas_finales]
        
        datos_para_insertar = [tuple(row) for row in df_para_cargar.where(pd.notnull(df_para_cargar), None).to_numpy()]
        
        sql = """
            INSERT INTO propiedades (
                source_id, price_usd, expensas_ars, barrio, address, 
                ambientes, dormitorios, banos, superficie_total_m2, 
                cocheras, description, link, scrap_date
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        for i in range(0, len(datos_para_insertar), batch_size):
            lote = datos_para_insertar[i:i + batch_size]
            cursor.executemany(sql, lote)
            conn.commit()
            print(f"  - Lote de {len(lote)} registros insertado.")
            
        print(f"✅ ¡Carga exitosa! Se han insertado {len(datos_para_insertar)} registros en la tabla 'propiedades'.")
        
    except mysql.connector.Error as e:
        print(f"❌ Error durante la carga de datos: {e}")
        conn.rollback()
    finally:
        if cursor:
            cursor.close()

if __name__ == '__main__':
    conn = conectar_db()
    
    if conn:
        df_crudo = leer_datos_crudos(DATA_FILE_PATH)
        
        if df_crudo is not None:
            df_transformado = transformar_datos(df_crudo)
            
            cargar_datos(df_transformado, conn)

        conn.close()
        print("✅ Proceso ETL completado y conexión cerrada.")