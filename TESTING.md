# Estrategia de Pruebas (Testing)

En `ecoflow_reader` mantenemos un estándar estricto de calidad de código. Este documento detalla la arquitectura de pruebas implementada para garantizar la estabilidad de la librería, la integridad de los modelos de datos y la compatibilidad entre distintas versiones de Python.

## 1. Tipos de Pruebas y Tecnologías Utilizadas

Nuestra suite de validación se divide en dos enfoques principales. Aunque ambas pruebas comparten herramientas en su base, su propósito, configuración y ejecución técnica son completamente distintos:

### A. Pruebas Unitarias (Unit Tests)
*   **Propósito:** Verificar el comportamiento lógico interno de la librería (parseo de datos de Pydantic, manejo de errores de red, instanciación de clases) de forma completamente aislada, determinista y ultrarrápida.
*   **Paquetes y tecnologías:**
    *   `pytest`: Actúa como el motor de ejecución principal para correr los asserts y evaluar resultados.
    *   `unittest.mock` (Librería estándar): Utilizamos `@patch` para interceptar y "engañar" a la librería, simulando respuestas falsas en formato JSON y forzando caídas catastróficas (Timeout) para probar nuestra resiliencia.
*   **Diferencia clave:** En esta prueba **nunca hay conexión a internet**. El paquete `requests` es interceptado por `mock` antes de salir al exterior. No se requieren credenciales válidas ni se consume cuota de la API de EcoFlow.

### B. Pruebas de Integración (Integration Tests)
*   **Propósito:** Validar la comunicación real de extremo a extremo (End-to-End) con los servidores de producción de EcoFlow. Garantiza que la estructura que esperamos en nuestros modelos sigue coincidiendo con la información viva que la plataforma transmite hoy en día.
*   **Paquetes y tecnologías:**
    *   `pytest`: Vuelve a actuar como motor de ejecución, pero esta vez se aísla de las pruebas unitarias mediante el uso de marcadores explícitos (`pytest -m integration`).
    *   `requests`: A diferencia de las unitarias, aquí la librería sí ejecuta peticiones HTTP (GET) reales hacia `api.ecoflow.com` usando cabeceras criptográficas (HMAC-SHA256).
    *   `python-dotenv`: Juega un rol vital al inyectar las credenciales reales (`ECOFLOW_API_KEY`, etc.) desde tu archivo local `.env` directamente a las variables de entorno.
*   **Diferencia clave:** Esta prueba **requiere internet y credenciales reales**. Si los ingenieros de EcoFlow cambian sorpresivamente la estructura de su API o los servidores caen, esta prueba fallará automáticamente, alertándonos del problema externo.

---

## 2. Pilares de Calidad y Validación Avanzada

Más allá de verificar que el código "funciona", la librería se somete a tres análisis de validación profunda para asegurar un grado de ingeniería de nivel empresarial.

### A. Análisis de Cobertura (Code Coverage)
No basta con probar los "caminos felices" (cuando todo sale bien); necesitamos garantías de que el código reacciona correctamente ante el desastre.
*   **Propósito:** Cuantificar exactamente qué porcentaje del código fuente es ejecutado y validado durante la ejecución de las pruebas unitarias.
*   **Herramienta:** `pytest-cov` (que actúa como puente hacia la librería `coverage`).
*   **Implementación:** Exigimos un estándar de cobertura superior al **95%**. Esto nos obliga a escribir pruebas específicas para escenarios extremos, tales como:
    *   Forzar caídas de red o errores HTTP 500 para asegurar que los bloques `try/except` en `client.py` capturan el error, lo registran en el *log* y devuelven `None` sin romper la aplicación.
    *   Inyectar datos corruptos para validar que `Pydantic` maneja las excepciones adecuadamente.
    *   Simular la ausencia de variables de entorno para confirmar que la CLI (`cli.py`) aborta la ejecución limpiamente con un código de salida `1` en lugar de generar trazas de error incomprensibles.

### B. Análisis Estático de Tipos
Python es un lenguaje de tipado dinámico, lo cual es flexible pero propenso a errores en tiempo de ejecución. Nosotros eliminamos esta vulnerabilidad antes de que el código siquiera se ejecute.
*   **Propósito:** Auditar matemáticamente el flujo de datos para garantizar que cada variable, parámetro y valor de retorno coincida con su estructura esperada, previniendo errores críticos como los `AttributeError` (ej. intentar acceder a un método de un objeto que resultó ser nulo).
*   **Herramienta:** `mypy` configurado en **modo estricto** (`strict = true` en `pyproject.toml`).
*   **Implementación:** Mypy audita el 100% de la base de código. Exige declaraciones formales como `dict[str, Any] | None` y prohíbe las devoluciones implícitas (requiriendo `-> None`). Esto actúa como un desarrollador senior virtual: si el cliente puede devolver un modelo Pydantic o un diccionario crudo, Mypy obliga al desarrollador a utilizar validadores (como `isinstance()`) antes de permitir el acceso a propiedades como `.battery`, garantizando que el código sea estructuralmente invulnerable a inconsistencias de tipos.

### C. Testing de Matriz (Cross-Version Testing)
El ecosistema de Python es amplio y fragmentado. Una librería debe funcionar idénticamente en un servidor heredado y en un contenedor de última generación.
*   **Propósito:** Certificar la compatibilidad universal del paquete evaluándolo simultáneamente contra múltiples intérpretes de Python.
*   **Herramientas:** `tox` (el orquestador) potenciado por `tox-uv` (el motor de resolución ultrarrápido).
*   **Implementación:** En lugar de probar la librería únicamente en el entorno local del desarrollador (ej. Python 3.13), Tox está configurado para levantar entornos virtuales completamente aislados para **Python 3.10, 3.11, 3.12 y 3.13**. 
    *   Si el sistema anfitrión no posee estas versiones, la variable de entorno `UV_PYTHON_DOWNLOADS=true` le permite a `uv` descargar los intérpretes binarios en milisegundos.
    *   Dentro de cada entorno aislado, Tox instala las dependencias desde cero, ejecuta el análisis de tipos estricto (`mypy`) y corre la suite completa de pruebas unitarias (`pytest`). Si una sintaxis moderna o una función obsoleta rompe la retrocompatibilidad, la matriz fallará, evitando que se publique una versión defectuosa en PyPI.

---

## 3. Ejecución de las Pruebas

Toda la suite de validación está empaquetada dentro de contenedores Docker para evitar conflictos de dependencias en tu máquina local. 

Para ejecutar los flujos de prueba, utiliza nuestro contenedor `test`:

### A. Validación Estricta (Requerido antes de un Commit/Release)
Este comando descarga las diferentes versiones de Python, ejecuta el análisis estático con `mypy` y corre las pruebas unitarias en todas las versiones soportadas de manera secuencial.
```bash
docker compose run --rm -e UV_PYTHON_DOWNLOADS=true test bash -c "uv pip install --system -e '.[dev]' && tox"
```

### B. Ejecución Rápida de Desarrollo (Unitarias + Integración)
Ejecuta las pruebas en la versión actual de Python. **Nota:** Para que las pruebas de integración funcionen, debes tener el archivo `.env` configurado con tus credenciales reales de EcoFlow. De lo contrario, dichas pruebas serán omitidas de forma segura.
```bash
docker compose run --rm test
```
*(Nota: Para ejecutar exclusivamente las pruebas unitarias y omitir la conexión a internet, puedes usar: `docker compose run --rm test bash -c "uv pip install --system -e '.[dev]' && pytest -m 'not integration'"`).*
