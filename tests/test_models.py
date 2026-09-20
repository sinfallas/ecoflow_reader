from ecoflow_reader.models import DeviceQuota, BatteryStatus

def test_device_quota_parses_full_json(mock_ecoflow_response):
    """Verifica que el modelo extrae correctamente los datos del JSON original."""
    raw_data = mock_ecoflow_response["data"]
    quota = DeviceQuota.from_ecoflow_json(raw_data)
    
    # Pruebas de Batería
    assert quota.battery.level == 98
    assert quota.battery.target_level == 97.86
    assert quota.battery.cycles == 183
    
    # Pruebas de Energía
    assert quota.power_in.total_watts == 145
    assert quota.power_out.time_remaining_mins == -5938
    assert quota.raw_data == raw_data  # El json original debe preservarse

def test_device_quota_handles_missing_data(mock_ecoflow_incomplete_response):
    """Verifica que si faltan datos en la API, Pydantic asigna 0 por defecto sin crashear."""
    raw_data = mock_ecoflow_incomplete_response["data"]
    quota = DeviceQuota.from_ecoflow_json(raw_data)
    
    assert quota.battery.level == 50
    assert quota.battery.temp_c == 40
    # Como faltaban, deben ser 0 gracias a los default=0 en los modelos
    assert quota.battery.cycles == 0
    assert quota.power_in.total_watts == 0

def test_models_allow_pythonic_instantiation():
    """Verifica que populate_by_name=True permite crear objetos manualmente con nombres limpios."""
    battery = BatteryStatus(level=100, target_level=80.5, temp_c=30)
    
    assert battery.level == 100
    assert battery.target_level == 80.5
    assert battery.temp_c == 30
    assert battery.health == 0 # default
