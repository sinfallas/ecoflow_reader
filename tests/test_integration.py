import os
import pytest
from dotenv import load_dotenv
from ecoflow_reader.client import EcoFlowClient
from ecoflow_reader.models import DeviceQuota

# Cargamos las variables reales de tu entorno
load_dotenv()

# Verificamos si tenemos las credenciales necesarias
has_credentials = all([
    os.getenv('ECOFLOW_API_KEY'),
    os.getenv('ECOFLOW_API_SECRET'),
    os.getenv('ECOFLOW_DEVICE_SN')
])

# Marcamos esta prueba como "integration" y le decimos que la omita si no hay credenciales
@pytest.mark.integration
@pytest.mark.skipif(not has_credentials, reason="Se requieren credenciales reales en el .env")
def test_live_api_connection():
    """Conecta con la API real de EcoFlow y valida que el formato de respuesta sea compatible con nuestros modelos."""
    
    key = os.getenv('ECOFLOW_API_KEY')
    secret = os.getenv('ECOFLOW_API_SECRET')
    sn = os.getenv('ECOFLOW_DEVICE_SN')
    
    client = EcoFlowClient(api_key=key, api_secret=secret)
    
    # 1. Validar que la API responde exitosamente en crudo (código "0")
    raw_response = client.get_device_quota(sn=sn, as_model=False)
    assert raw_response is not None
    assert isinstance(raw_response, dict)
    assert raw_response.get("code") == "0", f"La API devolvió un error: {raw_response.get('message')}"
    assert "data" in raw_response
    
    # 2. Validar que Pydantic puede procesar la respuesta viva actual
    quota = client.get_device_quota(sn=sn, as_model=True)
    assert quota is not None
    assert isinstance(quota, DeviceQuota)
    
    # Comprobamos que al menos los datos críticos están presentes y mapeados
    assert hasattr(quota.battery, 'level')
    assert isinstance(quota.battery.level, int)
    assert hasattr(quota.power_in, 'ac_in_voltage')
