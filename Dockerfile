# 1. Usar una imagen base de Python slim
FROM python:3.12-slim

# 2. Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiar el archivo de requerimientos primero para aprovechar el cache de Docker
COPY requirements.txt .

# 4. Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar el resto del código de la aplicación (incluyendo los artefactos del modelo)
COPY ./src ./src

# 6. Exponer el puerto en el que correrá la aplicación
EXPOSE 8000

# 7. Comando para iniciar la aplicación
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
