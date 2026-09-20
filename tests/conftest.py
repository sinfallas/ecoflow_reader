import pytest

@pytest.fixture
def mock_ecoflow_response():
    """Simula una respuesta exitosa y completa de la API de EcoFlow."""
    return {
        "code": "0",
        "message": "Success",
        "data": {
            "pd.soc": 98,
            "bms_bmsStatus.targetSoc": 97.86,
            "bms_bmsStatus.cycles": 183,
            "bms_bmsInfo.soh": 98,
            "bms_bmsStatus.temp": 34,
            "pd.wattsInSum": 145,
            "mppt.inWatts": 0,
            "inv.inputWatts": 101,
            "bms_emsStatus.chgRemainTime": 5939,
            "pd.wattsOutSum": 160,
            "inv.outputWatts": 101,
            "mppt.carOutWatts": 0,
            "pd.remainTime": -5938
        }
    }

@pytest.fixture
def mock_ecoflow_incomplete_response():
    """Simula una respuesta donde el equipo omitió ciertos datos (ej. MPPT)."""
    return {
        "code": "0",
        "message": "Success",
        "data": {
            "pd.soc": 50,
            "bms_bmsStatus.temp": 40
            # Faltan intencionalmente los datos de watts y ciclos
        }
    }
