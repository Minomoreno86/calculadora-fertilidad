# Dockerfile Final y Corregido

# 1. Imagen base
FROM python:3.11-slim

# 2. Directorio de trabajo
WORKDIR /app

# 3. Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiar tu código
COPY . .

# 5. Comando de ejecución final para Cloud Run
# Ajusta '01_Calculadora.py' si tu archivo tiene otro nombre.
CMD streamlit run 01_Calculadora.py --server.port=$PORT --server.address=0.0.0.0 --server.enableCORS=false