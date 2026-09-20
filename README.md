# EcoFlow Reader

Librería en Python para interactuar con la API pública de EcoFlow. Permite obtener información sobre las cuotas y el estado de los equipos vinculados a tu cuenta, implementando de forma nativa el flujo de autenticación seguro requerido por la plataforma mediante firmas criptográficas (HMAC-SHA256) 

A partir de la versión `0.1.3`, las respuestas están tipadas y estructuradas utilizando **Pydantic**, ofreciendo autocompletado en tu editor de código y validación automática de datos.

## Instalación

Puedes instalar la librería directamente desde PyPI utilizando `pip` o `uv`

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

Al instalar el paquete, se expone un binario global en tu sistema. Si tienes el archivo `.env` configurado en el directorio actual, simplemente ejecuta:

```bash
ecoflow-cli
```

Si la configuración es correcta, recibirás en consola un resumen limpio y formateado con el estado de la batería, la entrada de energía (cargas AC/Solar) y el consumo actual del dispositivo. En caso de error, el sistema de logging te indicará qué credencial o problema de red debes revisar.

### 2. Como Librería en tu Código Python

Puedes importar la clase `EcoFlowClient` para integrarla en tus propias aplicaciones, contenedores o APIs. Gracias a Pydantic, navegar por los datos del equipo es sumamente intuitivo:

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
    print(f"Nivel de Batería: {quota.battery.level}%")
    print(f"Temperatura: {quota.battery.temp_c}°C")
    print(f"Salida de energía (Consumo): {quota.power_out.total_watts}W")
    print(f"Entrada de energía (Carga): {quota.power_in.total_watts}W")
    
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
