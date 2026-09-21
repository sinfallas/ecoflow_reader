# EcoFlow Reader

Librería en Python para interactuar con la API pública de EcoFlow. Permite obtener información sobre las cuotas y el estado de los equipos vinculados a tu cuenta, implementando de forma nativa el flujo de autenticación seguro requerido por la plataforma mediante firmas criptográficas (HMAC-SHA256). 

A partir de la versión `0.1.5`, la librería ha sido rediseñada con estándares de nivel empresarial:
- **Modelos Estructurados:** Respuestas tipadas utilizando **Pydantic** para autocompletado de código y extracción de telemetría avanzada (voltajes, frecuencias, estado de interruptores y capacidad real).
- **Código Impecable:** Formateo automático y linting ultrarrápido garantizado por `ruff`.
- **Alta Fiabilidad:** Probada exhaustivamente con una cobertura de código superior al 97%.
- **Tipado Estricto:** Código 100% validado estáticamente en origen mediante `mypy`.
- **Compatibilidad Total:** Matriz de pruebas automatizada para entornos con Python 3.10, 3.11, 3.12, 3.13 y 3.14.

## Instalación

Puedes instalar la librería directamente desde PyPI utilizando `pip` o `uv`:

```bash
uv pip install ecoflow-reader
```

## Configuración

Para utilizar esta librería necesitas tus credenciales de acceso (Access Key y Secret Key) obtenidas en el portal de desarrolladores de EcoFlow, además del número de serie (SN) de tu equipo.

La librería lee estas credenciales desde variables de entorno. En la raíz de tu proyecto, copia la plantilla proporcionada:

```bash
cp env.example .env
```

Edita el archivo `.env` con tus credenciales reales:

```ini
ECOFLOW_API_KEY="tu_access_key_obtenida_en_ecoflow"
ECOFLOW_API_SECRET="tu_secret_key_obtenida_en_ecoflow"
ECOFLOW_DEVICE_SN="el_numero_de_serie_de_tu_equipo"
```

> **Importante:** Asegúrate de que el archivo `.env` esté incluido en tu `.gitignore` para evitar exponer tus credenciales.

## Uso

### 1. Desde la Terminal (CLI)

#### Opción A: Ejecución mediante Docker (Recomendado para pruebas sin instalación)
Si clonaste el repositorio y prefieres no instalar dependencias en tu sistema anfitrión, puedes ejecutar la herramienta directamente a través del contenedor de desarrollo aislado. Con tu archivo `.env` configurado en la raíz del proyecto, ejecuta:

```bash
docker compose run --rm test bash -c "uv pip install --system -e '.[dev]' && ecoflow-cli"
```

#### Opción B: Ejecución Local
Si instalaste el paquete en tu sistema usando `pip` o `uv`, se expone un binario global. Asegúrate de estar en el directorio donde se encuentra tu archivo `.env` y simplemente ejecuta:

```bash
ecoflow-cli
```

Si la configuración es correcta, recibirás en consola un resumen limpio y formateado mostrando la capacidad real de la batería (mAh), voltajes de la red eléctrica, estado de encendido de los puertos (AC/DC) y el consumo desglosado. En caso de error, el sistema de logging te indicará el problema.

### 2. Como Librería en tu Código Python

Puedes importar la clase `EcoFlowClient` para integrarla en tus propias aplicaciones, contenedores o APIs. Gracias a Pydantic, navegar por la telemetría del equipo es sumamente intuitivo:

```python
import os
from dotenv import load_dotenv
from ecoflow_reader import EcoFlowClient

# 1. Cargar las variables de entorno
load_dotenv()
API_KEY = os.getenv('ECOFLOW_API_KEY')
API_SECRET = os.getenv('ECOFLOW_API_SECRET')
DEVICE_SN = os.getenv('ECOFLOW_DEVICE_SN')

# 2. Inicializar el cliente
client = EcoFlowClient(api_key=API_KEY, api_secret=API_SECRET)

# 3. Consultar la API (Retorna un objeto DeviceQuota estructurado)
quota = client.get_device_quota(sn=DEVICE_SN)

if quota:
    print("=== BATERÍA ===")
    print(f"Nivel: {quota.battery.level}% ({quota.battery.remain_cap_mah} mAh)")
    print(f"Temperatura: {quota.battery.temp_c}°C")
    
    print("\n=== ENTRADA (CARGA) ===")
    print(f"Total: {quota.power_in.total_watts} W")
    if quota.power_in.ac_in_voltage > 0:
        print(f"Red Eléctrica: {quota.power_in.ac_in_voltage / 1000} V @ {quota.power_in.ac_in_freq} Hz")
    
    print("\n=== SALIDA (CONSUMO) ===")
    print(f"Total: {quota.power_out.total_watts} W")
    print(f"Enchufes AC Encendidos: {bool(quota.power_out.ac_enabled)}")
    print(f"Consumo AC: {quota.power_out.ac_watts} W")
    
    # Si quieres ver todo el objeto Pydantic en formato JSON estructurado:
    # print(quota.model_dump_json(indent=2))
else:
    print("No se pudo obtener la información del equipo.")
```

#### Acceso al JSON Original (Avanzado)
Si necesitas acceder a claves específicas del JSON de EcoFlow que no están mapeadas en el modelo principal, puedes solicitar la respuesta en formato diccionario nativo (crudo) pasando el parámetro `as_model=False`:

```python
raw_data = client.get_device_quota(sn=DEVICE_SN, as_model=False)
```

## Licencia y Autor

Desarrollado por Jesús Palencia (sinfallas)
Distribuido bajo la licencia GPL-2.0. Consulta el archivo `LICENSE` para más detalles.
