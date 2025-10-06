# 🚀 **Inicio Rápido**

Esta guía te llevará paso a paso para configurar y ejecutar la API de análisis inmobiliario.

## 📋 **Prerrequisitos**

- Python 3.9+
- MySQL 8.0+
- Git

## ⚙️ **Configuración del Entorno**

### **1. Clonar el Repositorio**
```bash
git clone <tu-repositorio>
cd api-analisis-inmobiliario-caba/api
```

### **2. Crear Entorno Virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### **3. Instalar Dependencias**
```bash
pip install -r requirements.txt
```

## 🗄️ **Configuración de Base de Datos**

### **1. Crear Base de Datos MySQL**
```sql
CREATE DATABASE propiedades_caba;
```

### **2. Crear Archivo de Configuración**
```bash
cp .env.example .env
```

Edita el archivo `.env` con tus credenciales:
```env
DB_HOST=localhost
DB_USER=tu_usuario
DB_PASSWORD=tu_password
DB_NAME=propiedades_caba
```

### **3. Crear Tabla de Propiedades**
```sql
USE propiedades_caba;

CREATE TABLE propiedades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    source_id VARCHAR(255) UNIQUE NOT NULL,
    price_usd DECIMAL(12,2),
    expensas_ars DECIMAL(10,2),
    barrio VARCHAR(100) NOT NULL,
    address TEXT,
    ambientes INT,
    dormitorios INT,
    banos INT,
    superficie_total_m2 INT,
    cocheras INT,
    description TEXT,
    link VARCHAR(500),
    scrap_date DATETIME,
    INDEX idx_barrio (barrio),
    INDEX idx_price (price_usd),
    INDEX idx_superficie (superficie_total_m2)
);
```

## 📊 **Carga de Datos**

### **1. Poblar la Base de Datos**
```bash
python scripts/poblar_db.py
```

Este script:
- Lee los datos crudos desde `data/ventas_deptos.pkl`
- Limpia y valida los datos
- Estandariza nombres de barrios
- Carga los datos en MySQL

### **2. Verificar Carga**
```sql
SELECT COUNT(*) FROM propiedades;
-- Debería mostrar ~50,000 registros
```

## 🤖 **Entrenamiento del Modelo**

### **1. Ejecutar Notebook de Entrenamiento**
```bash
jupyter notebook notebooks/entrenamiento_modelo.ipynb
```

### **2. Ejecutar Todas las Celdas**
El notebook:
- Carga datos desde la base de datos
- Entrena el modelo RandomForest
- Evalúa el rendimiento
- Guarda el modelo en `src/ml/model.pkl`

### **3. Verificar Modelo**
```bash
ls src/ml/
# Debería mostrar: model.pkl, model_columns.pkl, predict.py
```

## 🌐 **Iniciar la API**

### **1. Iniciar Servidor**
```bash
uvicorn src.api.main:app --reload
```

### **2. Verificar Funcionamiento**
- **API:** http://127.0.0.1:8000
- **Documentación:** http://127.0.0.1:8000/docs
- **Health Check:** http://127.0.0.1:8000/

## 🧪 **Probar la API**

### **1. Listar Propiedades**
```bash
curl http://127.0.0.1:8000/propiedades/
```

### **2. Hacer Predicción**
```bash
curl -X POST "http://127.0.0.1:8000/predict/" \
  -H "Content-Type: application/json" \
  -d '{
    "barrio": "Palermo",
    "ambientes": 3,
    "dormitorios": 2,
    "banos": 2,
    "superficie_total_m2": 80,
    "cocheras": 1
  }'
```

### **3. Ver Información del Modelo**
```bash
curl http://127.0.0.1:8000/predict/model-info
```

## 🔧 **Solución de Problemas**

### **Error de Conexión a BD**
- Verificar que MySQL esté ejecutándose
- Revisar credenciales en `.env`
- Confirmar que la base de datos existe

### **Modelo No Encontrado**
- Ejecutar el notebook de entrenamiento completo
- Verificar que `src/ml/model.pkl` existe
- Revisar logs del servidor

### **Datos No Cargados**
- Verificar que `data/ventas_deptos.pkl` existe
- Ejecutar `python scripts/poblar_db.py` nuevamente
- Revisar logs del script ETL

## 📚 **Próximos Pasos**

Una vez que tengas la API funcionando:

1. **[📖 Referencia de API](referencia-api.md)** - Explora todos los endpoints
2. **[🤖 Modelo de ML](modelo-ml.md)** - Entiende cómo funciona el modelo
3. **[📊 Visualizaciones](visualizaciones.md)** - Genera gráficos y análisis
4. **[💡 Ejemplos](ejemplos.md)** - Casos de uso prácticos

## ❓ **¿Necesitas Ayuda?**

Si encuentras algún problema:
1. Revisa los logs del servidor
2. Verifica la configuración de la base de datos
3. Consulta la documentación completa
4. Contacta: joaquin99911@gmail.com
