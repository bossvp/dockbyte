# Imagen oficial de Playwright con Python y navegadores incluidos
FROM mcr.microsoft.com/playwright/python:v1.41.0-jammy

# Directorio de trabajo
WORKDIR /app

# Copiar dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Exponer el puerto interno
EXPOSE 10000

# Iniciar la app con Gunicorn
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:10000", "app:app"]
