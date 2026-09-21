import sys
import pytest
from unittest.mock import patch, MagicMock
from ecoflow_reader.cli import main
from ecoflow_reader.models import DeviceQuota

@patch("sys.argv", ["ecoflow-cli"])
@patch("ecoflow_reader.cli.os.getenv")
def test_cli_missing_credentials_exits(mock_getenv):
    """Verifica que el CLI aborte si faltan variables de entorno."""
    mock_getenv.return_value = None  # Simulamos que el .env está vacío
    
    with pytest.raises(SystemExit) as exc_info:
        main()
        
    assert exc_info.value.code == 1

@patch("sys.argv", ["ecoflow-cli"])
@patch("ecoflow_reader.cli.EcoFlowClient")
@patch("ecoflow_reader.cli.os.getenv")
def test_cli_success_output(mock_getenv, mock_client_class, mock_ecoflow_response, capsys):
    """Verifica que el CLI imprima correctamente el panel si todo funciona."""
    mock_getenv.side_effect = lambda k: "fake_data" if k in ['ECOFLOW_API_KEY', 'ECOFLOW_API_SECRET', 'ECOFLOW_DEVICE_SN'] else None
    
    mock_instance = MagicMock()
    mock_instance.get_device_quota.return_value = DeviceQuota.from_ecoflow_json(mock_ecoflow_response["data"])
    mock_client_class.return_value = mock_instance
    
    main()
    
    captured = capsys.readouterr()
    assert "=== ESTADO DEL EQUIPO ECOFLOW ===" in captured.out
    assert "Total Entrando: 145 W" in captured.out
    assert "Batería: 98%" in captured.out

@patch("sys.argv", ["ecoflow-cli", "--raw"])
@patch("ecoflow_reader.cli.EcoFlowClient")
@patch("ecoflow_reader.cli.os.getenv")
def test_cli_raw_output(mock_getenv, mock_client_class, mock_ecoflow_response, capsys):
    """Verifica que el CLI imprima el JSON crudo cuando se usa --raw."""
    mock_getenv.side_effect = lambda k: "fake_data" if k in ['ECOFLOW_API_KEY', 'ECOFLOW_API_SECRET', 'ECOFLOW_DEVICE_SN'] else None
    
    mock_instance = MagicMock()
    # Para --raw, as_model=False devuelve un diccionario
    mock_instance.get_device_quota.return_value = mock_ecoflow_response["data"]
    mock_client_class.return_value = mock_instance
    
    main()
    
    captured = capsys.readouterr()
    # Verificamos que imprima una clave típica del JSON crudo
    assert '"pd.soc": 98' in captured.out
