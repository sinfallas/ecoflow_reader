import hashlib
import hmac
import random
import time
import logging
from typing import Any, cast
import requests

from .models import DeviceQuota

log = logging.getLogger(__name__)

class EcoFlowClient:
    def __init__(self, api_key: str, api_secret: str, base_url: str = 'https://api.ecoflow.com') -> None:
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url

    def _hmac_sha256(self, data: str) -> str:
        return hmac.new(self.api_secret.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest()

    def _get_qstring(self, params: dict[str, Any] | None) -> str:
        if not params:
            return ""
        return '&'.join([f"{key}={params[key]}" for key in sorted(params.keys())])

    def request(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any] | None:
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
            # Mypy requiere que confirmemos explícitamente que JSON devuelve un diccionario
            return cast(dict[str, Any], response.json())
        except requests.exceptions.RequestException as e:
            log.error(f"Error en la petición a la API: {e}")
            if hasattr(e, 'response') and e.response is not None:
                log.error(f"Detalle del servidor: {e.response.text}")
            return None

    def get_device_quota(self, sn: str, as_model: bool = True) -> DeviceQuota | dict[str, Any] | None:
        response = self.request('/iot-open/sign/device/quota/all', {'sn': sn})
        
        if not response or response.get("code") != "0":
            return None
            
        data = cast(dict[str, Any], response.get("data", {}))
        
        if as_model:
            try:
                return DeviceQuota.from_ecoflow_json(data)
            except Exception as e:
                log.error(f"Error parseando datos con Pydantic: {e}")
                return None
        
        return response
