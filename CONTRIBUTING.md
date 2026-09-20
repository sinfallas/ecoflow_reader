# Guía de Contribución y Desarrollo

Gracias por interesarte en el desarrollo de `ecoflow_reader`. Este documento explica cómo está configurado el entorno de trabajo y cuáles son los pasos exactos para empaquetar y publicar nuevas versiones.

## Desarrollo y Publicación

Este repositorio incluye un entorno basado en Docker Compose diseñado para empaquetar y publicar la librería de forma limpia y aislada. De esta manera, garantizamos reproducibilidad en el empaquetado sin depender de la configuración local del sistema anfitrión.

Para publicar una nueva versión en PyPI:

1. Actualiza el número de versión en el archivo `pyproject.toml`.
2. Asegúrate de tener configurada la variable `UV_PUBLISH_TOKEN` en tu archivo `.env` local con tu token de PyPI.
3. Ejecuta el entorno de construcción:

```bash
docker compose up build
```

El contenedor generará los empaquetados `.tar.gz` y `.whl` utilizando `uv`, los subirá a PyPI y se detendrá automáticamente.
