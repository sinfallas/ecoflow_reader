from pydantic import BaseModel, Field, ConfigDict

# 1. Creamos una clase base para que todos los modelos hereden esta configuración
class EcoFlowBaseModel(BaseModel):
    """Clase base para todos los modelos de EcoFlow, permitiendo instanciación por nombre o alias."""
    model_config = ConfigDict(populate_by_name=True)

class BatteryStatus(EcoFlowBaseModel):
    """Estado de la batería."""
    level: int = Field(default=0, alias="pd.soc", description="Nivel de batería actual en %")
    target_level: float = Field(default=0.0, alias="bms_bmsStatus.targetSoc", description="Nivel de carga objetivo configurado en %")
    cycles: int = Field(default=0, alias="bms_bmsStatus.cycles", description="Número de ciclos de la batería")
    health: int = Field(default=0, alias="bms_bmsInfo.soh", description="Estado de salud de la batería (State of Health) en %")
    temp_c: int = Field(default=0, alias="bms_bmsStatus.temp", description="Temperatura actual en grados Celsius")

class PowerIn(EcoFlowBaseModel):
    """Estado de la entrada de energía (Carga)."""
    total_watts: int = Field(default=0, alias="pd.wattsInSum", description="Total de watts entrando al dispositivo")
    solar_watts: int = Field(default=0, alias="mppt.inWatts", description="Watts de entrada desde el puerto solar/vehículo (MPPT)")
    ac_watts: int = Field(default=0, alias="inv.inputWatts", description="Watts de entrada desde la corriente alterna (AC)")
    time_remaining_mins: int = Field(default=0, alias="bms_emsStatus.chgRemainTime", description="Minutos restantes para carga completa")

class PowerOut(EcoFlowBaseModel):
    """Estado de la salida de energía (Descarga)."""
    total_watts: int = Field(default=0, alias="pd.wattsOutSum", description="Total de watts saliendo del dispositivo")
    ac_watts: int = Field(default=0, alias="inv.outputWatts", description="Watts de salida por los puertos de corriente alterna (AC)")
    dc_car_watts: int = Field(default=0, alias="mppt.carOutWatts", description="Watts de salida por el puerto del vehículo")
    time_remaining_mins: int = Field(default=0, alias="pd.remainTime", description="Minutos restantes hasta agotar la batería (valor negativo)")

class DeviceQuota(EcoFlowBaseModel):
    """Modelo principal que agrupa toda la información relevante del dispositivo."""
    battery: BatteryStatus
    power_in: PowerIn
    power_out: PowerOut
    raw_data: dict = Field(default_factory=dict, exclude=True, description="El JSON original completo, excluido de la serialización por defecto")

    @classmethod
    def from_ecoflow_json(cls, data_dict: dict) -> 'DeviceQuota':
        """Construye el modelo a partir del diccionario 'data' del JSON de EcoFlow."""
        return cls(
            battery=BatteryStatus(**data_dict),
            power_in=PowerIn(**data_dict),
            power_out=PowerOut(**data_dict),
            raw_data=data_dict
        )
