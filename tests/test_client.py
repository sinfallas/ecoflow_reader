import pytest
from unittest.mock import patch, Mock
import requests
from ecoflow_reader.client import EcoFlowClient
from ecoflow_reader.models import DeviceQuota

# Fixture del cliente para no instanciarlo en cada prueba
@pytest.fixture
def client():
    return EcoFlowClient(api_key="TEST_KEY", api_secret="TEST_SECRET")

@patch("ecoflow_reader.client.requests.get")
def test_get_device_quota_returns_model(mock_get, client, mock_ecoflow_response):
    """Verifica que el cliente retorne el modelo Pydantic cuando as_model=True."""
    # Configuramos el mock para que responda con nuestro JSON falso
    mock_response = Mock()
    mock_response.json.return_value = mock_ecoflow_response
    mock_get.return_value = mock_response
    
    result = client.get_device_quota(sn="12345", as_model=True)
    
    assert isinstance(result, DeviceQuota)
    assert result.battery.level == 98
    # Verifica que el request se hizo con los headers de autenticación correctos
    mock_get.assert_called_once()
    args, kwargs = mock_get.call_args
    assert "accessKey" in kwargs["headers"]
    assert "sign" in kwargs["headers"]

@patch("ecoflow_reader.client.requests.get")
def test_get_device_quota_returns_dict(mock_get, client, mock_ecoflow_response):
    """Verifica que el cliente retorne un diccionario crudo cuando as_model=False."""
    mock_response = Mock()
    mock_response.json.return_value = mock_ecoflow_response
    mock_get.return_value = mock_response
    
    result = client.get_device_quota(sn="12345", as_model=False)
    
    assert isinstance(result, dict)
    assert result["code"] == "0"

@patch("ecoflow_reader.client.requests.get")
def test_get_device_quota_handles_http_errors(mock_get, client):
    """Verifica que un error HTTP (ej. 401 o Timeout) retorne None limpiamente."""
    # Hacemos que la petición lance una excepción (simulando un error de red)
    mock_get.side_effect = requests.exceptions.Timeout("Timeout reaching EcoFlow API")
    
    result = client.get_device_quota(sn="12345")
    
    assert result is None
