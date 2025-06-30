# Dockerfile para la Calculadora de Fertilidad en Streamlit

# Etapa 1: Imagen base liviana
FROM python:3.11-slim

# Etapa 2: Directorio de trabajo
WORKDIR /app

# Etapa 3: Copiar dependencias y optimizar cache
COPY requirements.txt .

# Etapa 4: Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Etapa 5: Copiar el código
COPY . .

# Etapa 6: Exponer el puerto requerido por Cloud Run
EXPOSE 8080

# Etapa 7: Configurar el comando de ejecución (correcto para variables de entorno)
# Esta es la forma correcta que Cloud Run interpreta bien (forma exec)
CMD ["streamlit", "run", "Calculadora.py", "--server.port=8080", "--server.address=0.0.0.0", "--server.enableCORS=false"]
