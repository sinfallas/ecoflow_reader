# EcoFlow Reader

Librería en Python para interactuar con la API pública de EcoFlow. Permite obtener información sobre las cuotas y el estado de los equipos vinculados a tu cuenta, implementando de forma nativa el flujo de autenticación seguro requerido por la plataforma mediante firmas criptográficas (HMAC-SHA256).

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

Al instalar el paquete, se expone un binario global en tu sistema. Si tienes el archivo `.env` configurado en el directorio actual, simplemente ejecuta:

```bash
ecoflow-cli
```

Si la configuración es correcta, recibirás en consola la información de cuota y estado del dispositivo en formato JSON. En caso de error, el sistema de logging te indicará qué credencial o problema de red debes revisar.

### 2. Como Librería en tu Código Python

Puedes importar la clase `EcoFlowClient` para integrarla en tus propias aplicaciones, contenedores o APIs:

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

# 3. Consultar la API
datos = client.get_device_quota(sn=DEVICE_SN)

if datos:
    print(datos)
else:
    print("No se pudo obtener la información del equipo.")
```

## Desarrollo y Publicación

Este repositorio incluye un entorno basado en Docker Compose diseñado para empaquetar y publicar la librería de forma limpia y aislada.

Para publicar una nueva versión en PyPI:

1. Actualiza el número de versión en el archivo `pyproject.toml`.
2. Asegúrate de tener configurada la variable `UV_PUBLISH_TOKEN` en tu archivo `.env` con tu token de PyPI.
3. Ejecuta el entorno de construcción:

```bash
docker compose up build
```

El contenedor generará los empaquetados `.tar.gz` y `.whl` utilizando `uv`, los subirá a PyPI y se detendrá automáticamente.

## Licencia y Autor

Desarrollado por Jesús Palencia.  
Distribuido bajo la licencia GPL-2.0. Consulta el archivo `LICENSE` para más detalles.
