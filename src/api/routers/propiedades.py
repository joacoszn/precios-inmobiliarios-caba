# src/api/routers/propiedades.py
from fastapi import APIRouter, HTTPException, Query, status, Depends
from typing import List, Optional
import mysql.connector
from mysql.connector.cursor import MySQLCursorDict
from ..db_connection import get_db_cursor
from ..schemas import Propiedad, EstadisticasBarrio, PropiedadCreate, PropiedadUpdate, EvolucionMercado

router = APIRouter()

@router.get("/", response_model=List[Propiedad], summary="Obtener un listado de propiedades con filtros")
def get_propiedades(
    barrio: Optional[str] = Query(None, description="Filtrar propiedades por barrio"),
    ambientes_min: Optional[int] = Query(None, description="Número mínimo de ambientes"),
    price_max_usd: Optional[float] = Query(None, description="Precio máximo en USD"),
    skip: int = Query(0, ge=0, description="Número de registros a omitir (para paginación)"),
    limit: int = Query(10, ge=1, le=100, description="Número máximo de registros a devolver"),
    cursor: MySQLCursorDict = Depends(get_db_cursor) # Inyección de dependencia
):
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
    return cursor.fetchall()

@router.get("/{propiedad_id}", response_model=Propiedad, summary="Obtener una propiedad por su ID")
def get_propiedad_by_id(propiedad_id: int, cursor: MySQLCursorDict = Depends(get_db_cursor)):
    query = "SELECT * FROM propiedades WHERE id = %s"
    cursor.execute(query, (propiedad_id,))
    propiedad = cursor.fetchone()
    
    if not propiedad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Propiedad no encontrada")
        
    return propiedad

@router.get("/estadisticas/precio-por-barrio/", response_model=List[EstadisticasBarrio], summary="Obtener estadísticas de precios por barrio")
def get_estadisticas_por_barrio(cursor: MySQLCursorDict = Depends(get_db_cursor)):
    query = """
        SELECT 
            barrio,
            COUNT(*) as cantidad_propiedades,
            ROUND(AVG(price_usd), 2) as precio_promedio_usd,
            ROUND(MIN(price_usd), 2) as precio_min_usd,
            ROUND(MAX(price_usd), 2) as precio_max_usd,
            ROUND(AVG(price_usd / superficie_total_m2), 2) as precio_promedio_m2_usd
        FROM propiedades
        WHERE superficie_total_m2 IS NOT NULL AND superficie_total_m2 > 0
        GROUP BY barrio ORDER BY barrio;
    """
    cursor.execute(query)
    return cursor.fetchall()

@router.get("/estadisticas/evolucion-mercado/", response_model=List[EvolucionMercado], summary="Obtener la evolución del mercado por fecha de scraping")
def get_evolucion_mercado(cursor: MySQLCursorDict = Depends(get_db_cursor)):
    query = """
        SELECT 
            scrap_date,
            COUNT(*) as cantidad_propiedades,
            ROUND(AVG(price_usd), 2) as precio_promedio_usd
        FROM propiedades
        GROUP BY scrap_date ORDER BY scrap_date;
    """
    cursor.execute(query)
    return cursor.fetchall()

@router.post("/", response_model=Propiedad, status_code=status.HTTP_201_CREATED, summary="Añadir una nueva propiedad")
def create_propiedad(propiedad: PropiedadCreate, cursor: MySQLCursorDict = Depends(get_db_cursor)):
    try:
        datos_propiedad = propiedad.model_dump()
        columnas = ", ".join(datos_propiedad.keys())
        placeholders = ", ".join(["%s"] * len(datos_propiedad))
        query = f"INSERT INTO propiedades ({columnas}) VALUES ({placeholders})"
        
        cursor.execute(query, list(datos_propiedad.values()))
        
        nuevo_id = cursor.lastrowid
        
        return {"id": nuevo_id, **datos_propiedad}

    except mysql.connector.Error as err:
        if err.errno == 1062:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe una propiedad con ese 'source_id'")
        # Otros errores de base de datos son manejados por la dependencia.
        raise

@router.put("/{propiedad_id}", response_model=Propiedad, summary="Actualizar una propiedad existente")
def update_propiedad(propiedad_id: int, updates: PropiedadUpdate, cursor: MySQLCursorDict = Depends(get_db_cursor)):
    update_data = updates.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se proporcionaron datos para actualizar")

    set_clause = ", ".join([f"{key} = %s" for key in update_data.keys()])
    params = list(update_data.values())
    params.append(propiedad_id)

    query = f"UPDATE propiedades SET {set_clause} WHERE id = %s"
    cursor.execute(query, params)
    
    if cursor.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Propiedad no encontrada para actualizar")
    
    select_query = "SELECT * FROM propiedades WHERE id = %s"
    cursor.execute(select_query, (propiedad_id,))
    return cursor.fetchone()

@router.delete("/{propiedad_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar una propiedad")
def delete_propiedad(propiedad_id: int, cursor: MySQLCursorDict = Depends(get_db_cursor)):
    query = "DELETE FROM propiedades WHERE id = %s"
    cursor.execute(query, (propiedad_id,))
    
    if cursor.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Propiedad no encontrada para eliminar")
    
    return None




