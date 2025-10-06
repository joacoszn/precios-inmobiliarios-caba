# src/api/routers/propiedades.py
from fastapi import APIRouter, HTTPException, Query, status, Body
from typing import List, Optional
import mysql.connector

# Importamos el gestor de la base de datos y los schemas
from ..db_connection import get_db_connection
from ..schemas import Propiedad, EstadisticasBarrio, PropiedadCreate, PropiedadUpdate, EvolucionMercado

router = APIRouter()

@router.get("/propiedades/", response_model=List[Propiedad], summary="Obtener un listado de propiedades con filtros")
def get_propiedades(
    barrio: Optional[str] = Query(None, description="Filtrar propiedades por barrio"),
    ambientes_min: Optional[int] = Query(None, description="Número mínimo de ambientes"),
    price_max_usd: Optional[float] = Query(None, description="Precio máximo en USD"),
    skip: int = Query(0, ge=0, description="Número de registros a omitir (para paginación)"),
    limit: int = Query(10, ge=1, le=100, description="Número máximo de registros a devolver")
):
    """
    Obtiene un listado de propiedades. Permite filtrar por barrio, número mínimo de ambientes
    y precio máximo en USD. También soporta paginación con los parámetros skip y limit.
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if conn is None:
            raise HTTPException(status_code=503, detail="No se pudo establecer conexión con la base de datos")
        
        cursor = conn.cursor(dictionary=True)
        
        # Construcción dinámica de la consulta SQL
        query = "SELECT * FROM propiedades WHERE 1=1"
        params = []
        
        if barrio:
            query += " AND barrio = %s"
            params.append(barrio)
        
        if ambientes_min is not None:
            query += " AND ambientes >= %s"
            params.append(ambientes_min)
        
        if price_max_usd is not None:
            query += " AND price_usd <= %s"
            params.append(price_max_usd)
            
        query += " ORDER BY id LIMIT %s OFFSET %s"
        params.extend([limit, skip])
        
        cursor.execute(query, tuple(params))
        propiedades = cursor.fetchall()
        
        return propiedades
        
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

@router.get("/propiedades/{propiedad_id}", response_model=Propiedad, summary="Obtener una propiedad por su ID")
def get_propiedad_by_id(propiedad_id: int):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if conn is None:
            raise HTTPException(status_code=503, detail="No se pudo establecer conexión con la base de datos")
        
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM propiedades WHERE id = %s"
        cursor.execute(query, (propiedad_id,))
        propiedad = cursor.fetchone()
        
        if not propiedad:
            raise HTTPException(status_code=404, detail="Propiedad no encontrada")
            
        return propiedad
        
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

@router.get("/estadisticas/precio-por-barrio/", response_model=List[EstadisticasBarrio], summary="Obtener estadísticas de precios por barrio")
def get_estadisticas_por_barrio():
    """
    Calcula y devuelve estadísticas agregadas de precios para cada barrio,
    incluyendo el precio promedio por metro cuadrado.
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if conn is None:
            raise HTTPException(status_code=503, detail="No se pudo establecer conexión con la base de datos")
        
        cursor = conn.cursor(dictionary=True)
        
        # --- CONSULTA SQL ACTUALIZADA CON REDONDEO ---
        query = """
            SELECT 
                barrio,
                COUNT(*) as cantidad_propiedades,
                ROUND(AVG(price_usd), 2) as precio_promedio_usd,
                ROUND(MIN(price_usd), 2) as precio_minimo_usd,
                ROUND(MAX(price_usd), 2) as precio_maximo_usd,
                ROUND(AVG(price_usd / superficie_total_m2), 2) as precio_promedio_m2_usd
            FROM 
                propiedades
            WHERE
                superficie_total_m2 IS NOT NULL AND superficie_total_m2 > 0
            GROUP BY 
                barrio
            ORDER BY
                barrio;
        """
        
        cursor.execute(query)
        estadisticas = cursor.fetchall()
        
        return estadisticas
        
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

@router.get("/estadisticas/evolucion-mercado/", response_model=List[EvolucionMercado], summary="Obtener la evolución del mercado por fecha de scraping")
def get_evolucion_mercado():
    """
    Calcula y devuelve estadísticas agregadas para cada una de las 4 fechas de scraping,
    mostrando la evolución en la cantidad de propiedades y el precio promedio.
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if conn is None:
            raise HTTPException(status_code=503, detail="No se pudo establecer conexión con la base de datos")
        
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT 
                scrap_date as fecha_scraping,
                COUNT(*) as cantidad_propiedades,
                ROUND(AVG(price_usd), 2) as precio_promedio_usd
            FROM 
                propiedades
            GROUP BY 
                scrap_date
            ORDER BY
                scrap_date;
        """
        
        cursor.execute(query)
        evolucion = cursor.fetchall()
        
        return evolucion
        
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

@router.post("/propiedades/", response_model=Propiedad, status_code=status.HTTP_201_CREATED, summary="Añadir una nueva propiedad")
def create_propiedad(propiedad: PropiedadCreate):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if conn is None:
            raise HTTPException(status_code=503, detail="No se pudo establecer conexión con la base de datos")
        
        cursor = conn.cursor(dictionary=True)
        
        # Convertimos el objeto Pydantic a un diccionario
        datos_propiedad = propiedad.model_dump()
        
        columnas = ", ".join(datos_propiedad.keys())
        placeholders = ", ".join(["%s"] * len(datos_propiedad))
        
        query = f"INSERT INTO propiedades ({columnas}) VALUES ({placeholders})"
        
        cursor.execute(query, list(datos_propiedad.values()))
        conn.commit()
        
        # Obtenemos el ID de la propiedad recién creada
        nuevo_id = cursor.lastrowid
        
        # Devolvemos el objeto completo, incluyendo el nuevo ID
        return {"id": nuevo_id, **datos_propiedad}

    except mysql.connector.Error as err:
        if err.errno == 1062: # Código de error para entrada duplicada
            raise HTTPException(status_code=409, detail="Ya existe una propiedad con ese 'source_id'")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

@router.put("/propiedades/{propiedad_id}", response_model=Propiedad, summary="Actualizar una propiedad existente")
def update_propiedad(propiedad_id: int, updates: PropiedadUpdate):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if conn is None:
            raise HTTPException(status_code=503, detail="No se pudo establecer conexión con la base de datos")
        
        cursor = conn.cursor(dictionary=True)
        
        # Obtenemos solo los campos que el usuario quiere actualizar
        update_data = updates.model_dump(exclude_unset=True)
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No se proporcionaron datos para actualizar")

        set_clause = ", ".join([f"{key} = %s" for key in update_data.keys()])
        params = list(update_data.values())
        params.append(propiedad_id)

        query = f"UPDATE propiedades SET {set_clause} WHERE id = %s"
        
        cursor.execute(query, params)
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Propiedad no encontrada para actualizar")
            
        conn.commit()
        
        # Devolvemos la propiedad actualizada
        return get_propiedad_by_id(propiedad_id)

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

@router.delete("/propiedades/{propiedad_id}", status_code=status.HTTP_200_OK, summary="Eliminar una propiedad")
def delete_propiedad(propiedad_id: int):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if conn is None:
            raise HTTPException(status_code=503, detail="No se pudo establecer conexión con la base de datos")
        
        cursor = conn.cursor()
        
        query = "DELETE FROM propiedades WHERE id = %s"
        cursor.execute(query, (propiedad_id,))
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Propiedad no encontrada para eliminar")
        
        conn.commit()
        
        return {"detail": "Propiedad eliminada exitosamente"}

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()



