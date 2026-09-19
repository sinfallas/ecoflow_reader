# Integración API de EcoFlow

Este script de Python permite interactuar con la API pública de EcoFlow para obtener información sobre los equipos vinculados a tu cuenta. Implementa de forma nativa el flujo de autenticación seguro mediante firmas criptográficas (HMAC-SHA256) requerido por la plataforma.

## Características

- Autenticación segura basada en `nonce`, `timestamp` y firma HMAC-SHA256.
- Gestión de credenciales mediante variables de entorno (`.env`) para evitar exponer claves sensibles.
- Manejo estructurado de excepciones de red y timeouts.
- Validación preventiva de credenciales antes de ejecutar las peticiones.

## Requisitos Previos

- Python 3.7 o superior (probado con Python 3.13).
- Dependencias: `requests`, `python-dotenv`.

## Instalación

1. Clona este repositorio o descarga el script `ecoflow.py`.
2. Instala las dependencias necesarias. Puedes hacerlo utilizando `pip` estándar o `uv`:

   ```bash
   # Usando pip
   pip install requests python-dotenv

   # O usando uv para mayor velocidad
   uv pip install requests python-dotenv
   ```

## Configuración

Para utilizar este script, **primero debes registrarte en el portal de desarrolladores de la API de EcoFlow** para obtener tus credenciales de acceso (Access Key y Secret Key). También necesitarás tener a la mano el número de serie (SN) de tu equipo.

El script requiere que estas credenciales se pasen como variables de entorno. La forma más sencilla de gestionarlo es creando un archivo `.env`.

1. En el directorio raíz donde se encuentra tu script, crea un archivo llamado `.env`.
2. Añade tus credenciales siguiendo este formato:

   ```ini
   ECOFLOW_API_KEY="tu_access_key_obtenida_en_ecoflow"
   ECOFLOW_API_SECRET="tu_secret_key_obtenida_en_ecoflow"
   ECOFLOW_DEVICE_SN="el_numero_de_serie_de_tu_equipo"
   ```

> **Importante:** Asegúrate de tener `.env` listado dentro de tu archivo `.gitignore` para no subir tus credenciales a GitHub por error.

## Uso

Una vez que las dependencias estén instaladas y el archivo `.env` configurado, simplemente ejecuta el script desde la terminal:

```bash
python3 ecoflow.py
```

- Si la configuración es correcta, recibirás en consola la información de cuota y estado del dispositivo en formato JSON.
- Si falta alguna credencial o hay un problema de conectividad con la API, el sistema de logging mostrará un mensaje de error detallado indicando qué debes revisar.
