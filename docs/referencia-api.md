# 📖 **Referencia de API**

Documentación completa de todos los endpoints disponibles en la API de análisis inmobiliario.

## 🌐 **Base URL**

```
http://127.0.0.1:8000
```

## 📊 **Endpoints de Propiedades**

### **Listar Propiedades**
```http
GET /propiedades/
```

**Parámetros de consulta:**
- `barrio` (string, opcional): Filtrar por barrio
- `ambientes_min` (int, opcional): Número mínimo de ambientes
- `price_max_usd` (float, opcional): Precio máximo en USD
- `skip` (int, default: 0): Registros a omitir (paginación)
- `limit` (int, default: 10, max: 100): Registros a devolver

**Ejemplo:**
```bash
curl "http://127.0.0.1:8000/propiedades/?barrio=Palermo&ambientes_min=3&limit=5"
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "source_id": "prop_001",
    "price_usd": 185000.0,
    "barrio": "Palermo",
    "ambientes": 3,
    "dormitorios": 2,
    "banos": 2,
    "superficie_total_m2": 80,
    "cocheras": 1
  }
]
```

### **Obtener Propiedad por ID**
```http
GET /propiedades/{id}
```

**Ejemplo:**
```bash
curl http://127.0.0.1:8000/propiedades/123
```

### **Crear Nueva Propiedad**
```http
POST /propiedades/
```

**Body:**
```json
{
  "source_id": "prop_nueva",
  "price_usd": 200000.0,
  "barrio": "Recoleta",
  "ambientes": 4,
  "dormitorios": 3,
  "banos": 2,
  "superficie_total_m2": 100,
  "cocheras": 1
}
```

### **Actualizar Propiedad**
```http
PUT /propiedades/{id}
```

**Body (campos opcionales):**
```json
{
  "price_usd": 210000.0,
  "description": "Propiedad actualizada"
}
```

### **Eliminar Propiedad**
```http
DELETE /propiedades/{id}
```

## 📈 **Endpoints de Estadísticas**

### **Estadísticas por Barrio**
```http
GET /estadisticas/precio-por-barrio/
```

**Respuesta:**
```json
[
  {
    "barrio": "Palermo",
    "cantidad_propiedades": 1250,
    "precio_promedio_usd": 185000.0,
    "precio_min_usd": 120000.0,
    "precio_max_usd": 450000.0,
    "precio_promedio_m2_usd": 2312.5
  }
]
```

### **Evolución del Mercado**
```http
GET /estadisticas/evolucion-mercado/
```

**Respuesta:**
```json
[
  {
    "fecha_scraping": "2024-01-15T00:00:00",
    "cantidad_propiedades": 12500,
    "precio_promedio_usd": 175000.0
  }
]
```

## 🤖 **Endpoints de Machine Learning**

### **Predicción de Precios**
```http
POST /predict/
```

**Body:**
```json
{
  "barrio": "Palermo",
  "ambientes": 3,
  "dormitorios": 2,
  "banos": 2,
  "superficie_total_m2": 80,
  "cocheras": 1,
  "description": "Excelente departamento muy luminoso con balcón. A estrenar."
}
```

**Respuesta:**
```json
{
  "predicted_price_usd": 185000.0,
  "confidence_interval": {
    "lower": 170000.0,
    "upper": 200000.0
  },
  "similar_properties_avg": 178500.0
}
```

### **Información del Modelo**
```http
GET /predict/model-info
```

**Respuesta:**
```json
{
  "model_type": "RandomForestRegressor",
  "n_features": 67,
  "n_estimators": 100,
  "metrics": {
    "r2_score": 0.8764,
    "rmse_usd": 152468
  },
  "top_features": [
    {
      "feature": "superficie_total_m2",
      "importance": 0.42
    },
    {
      "feature": "barrio_Palermo",
      "importance": 0.11
    },
    {
      "feature": "feature_luminoso",
      "importance": 0.05
    }
  ]
}
```

## ✅ **Validaciones de Input**

### **PredictionInput**
- `barrio`: Debe ser un barrio válido de CABA
- `ambientes`: Entre 1 y 10
- `dormitorios`: Entre 0 y 8 (no puede superar ambientes)
- `banos`: Entre 1 y 6
- `superficie_total_m2`: Entre 20 y 1000 m²
- `cocheras`: Entre 0 y 4

### **Barrios Válidos**
```
Palermo, Recoleta, Belgrano, Caballito, Villa Urquiza,
Núñez, Almagro, Villa Crespo, Colegiales, Barrio Norte,
San Telmo, La Boca, Puerto Madero, Retiro, San Nicolás,
Balvanera, Monserrat, Constitucion, Barracas, Parque Patricios,
Boedo, San Cristobal, Liniers, Mataderos, Villa Lugano,
Villa Riachuelo, Villa Soldati, Pompeya, Parque Chacabuco,
Parque Avellaneda, Versalles, Villa Real, Monte Castro,
Villa Devoto, Villa del Parque, Villa Santa Rita, Agronomia,
Chacarita, Paternal, Villa Ortuzar, Coghlan, Parque Chas,
Floresta, Villa Luro, Villa Pueyrredon, Villa General Mitre,
Velez Sarsfield, Flores, Saavedra
```

## 🔍 **Códigos de Error**

| Código | Descripción |
|--------|-------------|
| 200 | OK |
| 201 | Creado |
| 400 | Error de validación |
| 404 | No encontrado |
| 409 | Conflicto (duplicado) |
| 500 | Error interno del servidor |
| 503 | Servicio no disponible |

## 📝 **Ejemplos de Uso**

### **Buscar Propiedades en Palermo**
```bash
curl "http://127.0.0.1:8000/propiedades/?barrio=Palermo&ambientes_min=3"
```

### **Predicción con Validación**
```bash
curl -X POST "http://127.0.0.1:8000/predict/" \
  -H "Content-Type: application/json" \
  -d '{
    "barrio": "Recoleta",
    "ambientes": 4,
    "dormitorios": 3,
    "banos": 2,
    "superficie_total_m2": 120,
    "cocheras": 2
  }'
```

### **Error de Validación**
```bash
curl -X POST "http://127.0.0.1:8000/predict/" \
  -H "Content-Type: application/json" \
  -d '{
    "barrio": "BarrioInexistente",
    "ambientes": 15,
    "dormitorios": 20,
    "banos": 1,
    "superficie_total_m2": 5,
    "cocheras": 0
  }'
```

**Respuesta de error:**
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "barrio"],
      "msg": "Barrio 'BarrioInexistente' no es válido",
      "input": "BarrioInexistente"
    }
  ]
}
```

## 🔗 **Enlaces Relacionados**

- **[🚀 Inicio Rápido](inicio-rapido.md)** - Configuración inicial
- **[🤖 Modelo de ML](modelo-ml.md)** - Detalles del modelo
- **[📊 Visualizaciones](visualizaciones.md)** - Gráficos y análisis
- **[💡 Ejemplos](ejemplos.md)** - Casos de uso prácticos
