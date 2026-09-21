# Guía de Contribución y Desarrollo

Gracias por interesarte en el desarrollo de `ecoflow_reader`. Este documento explica cómo está configurado el entorno de trabajo y cuáles son los pasos exactos para probar, empaquetar y publicar nuevas versiones.

## Entorno de Trabajo

Este repositorio incluye un entorno basado en Docker Compose diseñado para aislar completamente el ciclo de desarrollo. De esta manera, garantizamos la reproducibilidad de las pruebas y el empaquetado sin depender de la configuración local o las versiones de Python del sistema anfitrión.

## Desarrollo y Publicación

Para publicar una nueva versión en PyPI, sigue estos pasos:

1. **Verifica la estabilidad:** Asegúrate de que la Matriz Completa con `tox` finaliza con éxito.
2. **Actualiza la versión:** Modifica el número de versión en el archivo `pyproject.toml`.
3. **Credenciales:** Asegúrate de tener configurada la variable `UV_PUBLISH_TOKEN` en tu archivo `.env` local con tu token de PyPI.
4. **Construye y publica:** Ejecuta el entorno de construcción:

```bash
docker compose run --rm build
```

El contenedor se encargará de limpiar compilaciones previas, generará los nuevos empaquetados `.tar.gz` y `.whl` utilizando `uv`, los subirá a PyPI y se detendrá automáticamente.
