import hashlib
import hmac
import json
import logging
import os
import random
import time
import requests
from dotenv import load_dotenv

# 1. Configuración de logging
logging.basicConfig(level=logging.ERROR, format='%(levelname)s: %(message)s')
log = logging.getLogger(__name__)

def hmac_sha256(data: str, key: str) -> str:
    """Genera el hash HMAC-SHA256 en formato hexadecimal de forma nativa."""
    return hmac.new(key.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest()

def get_qstring(params: dict) -> str:
    """Construye el string de parámetros ordenados alfabéticamente."""
    if not params:
        return ""
    return '&'.join([f"{key}={params[key]}" for key in sorted(params.keys())])

def get_api(url: str, key: str, secret: str, params: dict = None) -> dict | None:
    """Realiza la petición GET firmada a la API de EcoFlow."""
    nonce = str(random.randint(100000, 999999))
    timestamp = str(int(time.time() * 1000))
    
    headers = {
        'accessKey': key,
        'nonce': nonce,
        'timestamp': timestamp
    }
    
    # Código limpio para concatenar la firma
    sign_str = (get_qstring(params) + '&' if params else '') + get_qstring(headers)
    headers['sign'] = hmac_sha256(sign_str, secret)
    
    try:
        # Se agrega un timeout de 10 segundos por seguridad de red
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status() # Lanza una excepción si el HTTP status es 4xx o 5xx
        return response.json()
    except requests.exceptions.RequestException as e:
        log.error(f"Error en la petición a la API: {e}")
        # Intentamos imprimir el detalle de la API si está disponible
        if 'response' in locals() and response is not None:
            log.error(f"Detalle del servidor: {response.text}")
        return None

if __name__ == "__main__":
    
    # Lee el archivo .env y carga las variables al entorno
    load_dotenv()
    
    url = 'https://api.ecoflow.com'
    path = '/iot-open/sign/device/quota/all'
    
    # Las credenciales se leen desde variables de entorno
    key = os.getenv('ECOFLOW_API_KEY')
    secret = os.getenv('ECOFLOW_API_SECRET')
    sn = os.getenv('ECOFLOW_DEVICE_SN')
    
    # Validación: verificar que las claves existen antes de hacer la petición
    if not all([key, secret, sn]):
        log.error("Faltan credenciales. Verifica que el archivo .env existe y contiene ECOFLOW_API_KEY, ECOFLOW_API_SECRET y ECOFLOW_DEVICE_SN.")
        exit(1)
    
    payload = get_api(f"{url}{path}", key, secret, {'sn': sn})
    
    if payload:
        print(json.dumps(payload, indent=2))
    else:
        print("No se pudo obtener la información del equipo.")
