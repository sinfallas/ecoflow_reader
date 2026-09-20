# Guía de Contribución y Desarrollo

Gracias por interesarte en el desarrollo de `ecoflow_reader`[cite: 32]. Este documento explica cómo está configurado el entorno de trabajo y cuáles son los pasos exactos para probar, empaquetar y publicar nuevas versiones[cite: 32].

## Entorno de Trabajo

Este repositorio incluye un entorno basado en Docker Compose diseñado para aislar completamente el ciclo de desarrollo[cite: 32]. De esta manera, garantizamos la reproducibilidad de las pruebas y el empaquetado sin depender de la configuración local o las versiones de Python del sistema anfitrión[cite: 32].

## Pruebas (Testing)

Antes de realizar un commit o publicar una nueva versión, es obligatorio verificar que el código base es estable[cite: 32]. Utilizamos `pytest` para ejecutar dos tipos de pruebas:

1. **Pruebas Unitarias:** Simulan las respuestas de la API de EcoFlow para validar la integridad de nuestros modelos de datos (Pydantic) de forma instantánea y sin consumir cuota de red.
2. **Pruebas de Integración:** Realizan una conexión real a los servidores de EcoFlow. Requieren que tengas un archivo `.env` configurado con credenciales válidas; de lo contrario, se omitirán automáticamente.

Puedes gestionar la ejecución de las pruebas utilizando el contenedor `test` que instalará las dependencias necesarias de forma aislada:

**A. Ejecutar TODAS las pruebas (Unitarias + Integración):**
```bash
docker compose run --rm test
```

**B. Ejecutar SOLO las pruebas unitarias (Rápidas, sin red):**
```bash
docker compose run --rm test bash -c "uv pip install --system -e '.[dev]' && pytest -v -m 'not integration'"
```

**C. Ejecutar SOLO las pruebas de integración (Conexión en vivo):**
```bash
docker compose run --rm test bash -c "uv pip install --system -e '.[dev]' && pytest -v -m integration"
```

## Desarrollo y Publicación

Para publicar una nueva versión en PyPI, sigue estos pasos[cite: 32]:

1. **Verifica la estabilidad:** Asegúrate de que las pruebas finalizan con éxito (todas las pruebas en verde)[cite: 32].
2. **Actualiza la versión:** Modifica el número de versión en el archivo `pyproject.toml`[cite: 32].
3. **Credenciales:** Asegúrate de tener configurada la variable `UV_PUBLISH_TOKEN` en tu archivo `.env` local con tu token de PyPI[cite: 32].
4. **Construye y publica:** Ejecuta el entorno de construcción[cite: 32]:

```bash
docker compose run --rm build
```

El contenedor se encargará de limpiar compilaciones previas, generará los nuevos empaquetados `.tar.gz` y `.whl` utilizando `uv`, los subirá a PyPI y se detendrá automáticamente[cite: 32].
