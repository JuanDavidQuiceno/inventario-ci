# Imagen de la aplicación: solo el código, sin pruebas ni dependencias de desarrollo
FROM python:3.12-slim

WORKDIR /app
ENV PYTHONPATH=/app/src \
    PYTHONUNBUFFERED=1

COPY src ./src

# Usuario sin privilegios
USER nobody

EXPOSE 8000
CMD ["python", "-m", "inventario.servidor"]
