import pytest

@pytest.fixture
def mock_ecoflow_response():
    """Simula una respuesta exitosa y completa de la API de EcoFlow."""
    return {
        "code": "0",
        "message": "Success",
        "data": {
            "pd.soc": 98,
            "bms_bmsStatus.targetSoc": 97.73,
            "bms_bmsStatus.cycles": 183,
            "bms_bmsInfo.soh": 98,
            "bms_bmsStatus.temp": 34,
            "bms_bmsStatus.remainCap": 19260,
            "bms_bmsStatus.fullCap": 19600,
            "bms_bmsStatus.vol": 54022,
            "pd.wattsInSum": 145,
            "mppt.inWatts": 0,
            "inv.inputWatts": 101,
            "inv.acInVol": 130020,
            "inv.acInFreq": 60,
            "bms_emsStatus.chgRemainTime": 5939,
            "pd.wattsOutSum": 160,
            "inv.outputWatts": 101,
            "mppt.carOutWatts": 0,
            "inv.cfgAcEnabled": 1,
            "pd.dcOutState": 0,
            "pd.typec1Watts": 15, # Valor inyectado para pruebas
            "pd.usb1Watts": 5,    # Valor inyectado para pruebas
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
            # Faltan intencionalmente los datos de watts, ciclos y capacidades
        }
    }
