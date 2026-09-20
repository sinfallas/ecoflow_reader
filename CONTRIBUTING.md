# Guía de Contribución y Desarrollo

Gracias por interesarte en el desarrollo de `ecoflow_reader`. Este documento explica cómo está configurado el entorno de trabajo y cuáles son los pasos exactos para probar, empaquetar y publicar nuevas versiones.

## Entorno de Trabajo

Este repositorio incluye un entorno basado en Docker Compose diseñado para aislar completamente el ciclo de desarrollo. De esta manera, garantizamos la reproducibilidad de las pruebas y el empaquetado sin depender de la configuración local o las versiones de Python del sistema anfitrión.

## Calidad de Código y Pruebas (Testing)

Para garantizar un estándar de nivel empresarial, el proyecto implementa múltiples capas de validación automatizada:

1. **Pruebas Unitarias y de Integración:** A través de `pytest`. Se evalúa el funcionamiento aislado mediante simulaciones (mocks) y se verifica la conexión en vivo con los servidores de EcoFlow.
2. **Cobertura de Código:** Medida con `pytest-cov`, garantizando que más del 95% del código es ejecutado durante las pruebas.
3. **Análisis Estático de Tipos:** Código validado en modo estricto con `mypy`.
4. **Matriz de Compatibilidad (Cross-Version):** Pruebas orquestadas con `tox` y `uv` para asegurar el funcionamiento en Python 3.10, 3.11, 3.12 y 3.13.

### Comandos de Validación

Dependiendo de la fase de desarrollo, puedes usar dos enfoques utilizando el contenedor `test`:

**A. La Matriz Completa (Ideal antes de un commit o publicación):**
Descarga automáticamente los intérpretes necesarios, ejecuta el análisis de tipos estricto (`mypy`) y corre todas las pruebas unitarias en las 4 versiones de Python soportadas.
```bash
docker compose run --rm -e UV_PYTHON_DOWNLOADS=true test bash -c "uv pip install --system -e '.[dev]' && tox"
```

**B. Prueba de Desarrollo (Unitarias + Integración):**
Ideal para el día a día. Ejecuta las pruebas de forma instantánea en tu versión de Python actual y evalúa la conexión real a EcoFlow (requiere un `.env` configurado con credenciales válidas; de lo contrario, la integración se omitirá automáticamente).
```bash
docker compose run --rm test
```

*(Nota: Para ejecutar exclusivamente las pruebas unitarias y omitir la conexión a internet, puedes usar: `docker compose run --rm test bash -c "uv pip install --system -e '.[dev]' && pytest -m 'not integration'"`).*

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
