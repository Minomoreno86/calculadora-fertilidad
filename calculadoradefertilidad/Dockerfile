# Dockerfile Final para la Calculadora de Fertilidad

# 1. IMAGEN BASE: Empezamos con un entorno Python limpio.
FROM python:3.11-slim

# 2. DIRECTORIO DE TRABAJO: Creamos y nos movemos a la carpeta /app.
WORKDIR /app

# 3. INSTALAR DEPENDENCIAS: Copiamos la lista y la instalamos.
# Este paso va primero para aprovechar la caché de Docker y acelerar futuras construcciones.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. COPIAR CÓDIGO: Copiamos todo nuestro código fuente al contenedor.
COPY . .

# 5. EXPONER PUERTO: Informamos que la app usará el puerto 8080.
EXPOSE 8080

# 6. COMANDO DE EJECUCIÓN: Esta es la ÚNICA instrucción CMD y va al FINAL.
# Usamos el nombre de archivo correcto y los parámetros que ya habías investigado.
# Por favor, confirma que tu archivo principal se llama 'calculadora.py' (con minúscula).
CMD ["streamlit", "run", "calculadora.py", "--server.port=8080", "--server.address=0.0.0.0", "--server.enableCORS=false"]