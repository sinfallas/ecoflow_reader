# Guía de Contribución y Desarrollo

Gracias por interesarte en el desarrollo de `ecoflow_reader`. Este documento explica cómo está configurado el entorno de trabajo y cuáles son los pasos exactos para probar, empaquetar y publicar nuevas versiones.

## Entorno de Trabajo

Este repositorio incluye un entorno basado en Docker Compose diseñado para aislar completamente el ciclo de desarrollo. De esta manera, garantizamos la reproducibilidad de las pruebas y el empaquetado sin depender de la configuración local o las versiones de Python del sistema anfitrión.

## Calidad de Código y Pruebas (Testing)

Para garantizar un estándar de nivel empresarial, el proyecto implementa múltiples capas de validación automatizada:

1. **Linting y Formateo Automático:** Uso de `ruff` para asegurar un estilo visual uniforme (PEP 8) y detectar errores de sintaxis o *imports* desordenados al instante.
2. **Pruebas Unitarias y de Integración:** A través de `pytest`. Se evalúa el funcionamiento aislado mediante simulaciones y se verifica la conexión en vivo con EcoFlow.
3. **Cobertura de Código:** Medida con `pytest-cov`, garantizando que más del 95% del código es ejecutado.
4. **Análisis Estático de Tipos:** Código validado en modo estricto con `mypy`.
5. **Matriz de Compatibilidad:** Pruebas orquestadas con `tox` para asegurar el funcionamiento en Python 3.10, 3.11, 3.12, 3.13 y 3.14.

### Comandos de Validación

Dependiendo de la fase de desarrollo, utiliza el contenedor `test`:

**A. La Matriz Completa (Ideal antes de un commit o publicación):**
Audita el estilo con Ruff, ejecuta el análisis de tipos con Mypy y corre las pruebas en las 5 versiones de Python soportadas.
```bash
docker compose run --rm -e UV_PYTHON_DOWNLOADS=true test bash -c "uv pip install --system -e '.[dev]' && tox"
```

**B. Auto-corrección de Estilo (Ruff):**
Formatea y arregla automáticamente los espacios e *imports* de todo el proyecto.
```bash
docker compose run --rm test bash -c "uv pip install --system -e '.[dev]' && ruff format src/ && ruff check --fix src/"
```

**C. Prueba Rápida de Desarrollo:**
Ejecuta las pruebas en tu versión actual y evalúa la conexión real a EcoFlow (requiere el archivo `.env` configurado).
```bash
docker compose run --rm test
```

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

## Solución de Problemas (Troubleshooting)

### Archivos de caché rastreados accidentalmente por Git
Si Git incluyó carpetas de caché temporal (como `.ruff_cache/` o `.pytest_cache/`) antes de que el archivo `.gitignore` fuera configurado, estas seguirán apareciendo en los *commits* futuros. Para obligar a Git a olvidarlas sin eliminarlas de tu disco duro, ejecuta el siguiente comando en tu entorno local:

```bash
git rm -r --cached .ruff_cache/
git rm -r --cached .pytest_cache/
```
