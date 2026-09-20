from pydantic import BaseModel, Field, ConfigDict

class EcoFlowBaseModel(BaseModel):
    """Clase base para todos los modelos de EcoFlow, permitiendo instanciación por nombre o alias."""
    model_config = ConfigDict(populate_by_name=True)

class BatteryStatus(EcoFlowBaseModel):
    """Estado y salud de la batería."""
    level: int = Field(default=0, alias="pd.soc", description="Nivel de batería actual en %")
    target_level: float = Field(default=0.0, alias="bms_bmsStatus.targetSoc", description="Nivel de carga objetivo en %")
    cycles: int = Field(default=0, alias="bms_bmsStatus.cycles", description="Número de ciclos de la batería")
    health: int = Field(default=0, alias="bms_bmsInfo.soh", description="Estado de salud (SOH) en %")
    temp_c: int = Field(default=0, alias="bms_bmsStatus.temp", description="Temperatura de la batería en °C")
    
    # Nuevos campos de capacidad y voltaje
    remain_cap_mah: int = Field(default=0, alias="bms_bmsStatus.remainCap", description="Capacidad restante en mAh")
    full_cap_mah: int = Field(default=0, alias="bms_bmsStatus.fullCap", description="Capacidad total actual en mAh")
    voltage_mv: int = Field(default=0, alias="bms_bmsStatus.vol", description="Voltaje de la batería en mV")

class PowerIn(EcoFlowBaseModel):
    """Estado de la entrada de energía (Carga)."""
    total_watts: int = Field(default=0, alias="pd.wattsInSum", description="Total de watts entrando")
    solar_watts: int = Field(default=0, alias="mppt.inWatts", description="Watts de entrada solar/vehículo")
    ac_watts: int = Field(default=0, alias="inv.inputWatts", description="Watts de entrada AC (Pared)")
    time_remaining_mins: int = Field(default=0, alias="bms_emsStatus.chgRemainTime", description="Minutos para carga completa")
    
    # Nuevos campos de telemetría de red eléctrica
    ac_in_voltage: int = Field(default=0, alias="inv.acInVol", description="Voltaje de entrada AC (en mV)")
    ac_in_freq: int = Field(default=0, alias="inv.acInFreq", description="Frecuencia de entrada AC (en Hz)")

class PowerOut(EcoFlowBaseModel):
    """Estado de la salida de energía (Descarga)."""
    total_watts: int = Field(default=0, alias="pd.wattsOutSum", description="Total de watts saliendo")
    time_remaining_mins: int = Field(default=0, alias="pd.remainTime", description="Minutos de batería restante (negativo)")
    
    # Interruptores (Switches)
    ac_enabled: int = Field(default=0, alias="inv.cfgAcEnabled", description="Estado de los enchufes AC (1=Encendido, 0=Apagado)")
    dc_enabled: int = Field(default=0, alias="pd.dcOutState", description="Estado de los puertos DC/USB (1=Encendido, 0=Apagado)")
    
    # Desglose de AC y DC (Coche)
    ac_watts: int = Field(default=0, alias="inv.outputWatts", description="Watts de salida AC")
    dc_car_watts: int = Field(default=0, alias="mppt.carOutWatts", description="Watts de salida por el puerto de coche")
    
    # Desglose de Puertos USB
    usb_c_1_watts: int = Field(default=0, alias="pd.typec1Watts", description="Watts en puerto USB-C 1")
    usb_c_2_watts: int = Field(default=0, alias="pd.typec2Watts", description="Watts en puerto USB-C 2")
    usb_a_1_watts: int = Field(default=0, alias="pd.usb1Watts", description="Watts en puerto USB-A 1")
    usb_a_2_watts: int = Field(default=0, alias="pd.usb2Watts", description="Watts en puerto USB-A 2")
    usb_a_qc_watts: int = Field(default=0, alias="pd.qcUsb1Watts", description="Watts en puerto USB-A QuickCharge")

class DeviceQuota(EcoFlowBaseModel):
    """Modelo principal que agrupa toda la información relevante del dispositivo."""
    battery: BatteryStatus
    power_in: PowerIn
    power_out: PowerOut
    raw_data: dict = Field(default_factory=dict, exclude=True, description="El JSON original completo")

    @classmethod
    def from_ecoflow_json(cls, data_dict: dict) -> 'DeviceQuota':
        """Construye el modelo a partir del diccionario 'data' del JSON de EcoFlow."""
        return cls(
            battery=BatteryStatus(**data_dict),
            power_in=PowerIn(**data_dict),
            power_out=PowerOut(**data_dict),
            raw_data=data_dict
        )
