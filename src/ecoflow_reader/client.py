import hashlib
import hmac
import random
import time
import logging
import requests

log = logging.getLogger(__name__)

class EcoFlowClient:
    def __init__(self, api_key: str, api_secret: str, base_url: str = 'https://api.ecoflow.com'):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url

    def _hmac_sha256(self, data: str) -> str:
        """Genera el hash HMAC-SHA256 en formato hexadecimal de forma nativa."""
        return hmac.new(self.api_secret.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest()

    def _get_qstring(self, params: dict) -> str:
        """Construye el string de parámetros ordenados alfabéticamente."""
        if not params:
            return ""
        return '&'.join([f"{key}={params[key]}" for key in sorted(params.keys())])

    def request(self, path: str, params: dict = None) -> dict | None:
        """Realiza la petición GET firmada a la API de EcoFlow."""
        nonce = str(random.randint(100000, 999999))
        timestamp = str(int(time.time() * 1000))
        
        headers = {
            'accessKey': self.api_key,
            'nonce': nonce,
            'timestamp': timestamp
        }
        
        sign_str = (self._get_qstring(params) + '&' if params else '') + self._get_qstring(headers)
        headers['sign'] = self._hmac_sha256(sign_str)
        
        try:
            response = requests.get(f"{self.base_url}{path}", headers=headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            log.error(f"Error en la petición a la API: {e}")
            if hasattr(e, 'response') and e.response is not None:
                log.error(f"Detalle del servidor: {e.response.text}")
            return None

    def get_device_quota(self, sn: str) -> dict | None:
        """Obtiene la cuota y estado de un dispositivo específico."""
        return self.request('/iot-open/sign/device/quota/all', {'sn': sn})
