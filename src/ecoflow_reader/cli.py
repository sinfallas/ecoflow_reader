import os
import logging
from dotenv import load_dotenv
from ecoflow_reader.client import EcoFlowClient

logging.basicConfig(level=logging.ERROR, format='%(levelname)s: %(message)s')
log = logging.getLogger(__name__)

def main():
    load_dotenv()
    
    key = os.getenv('ECOFLOW_API_KEY')
    secret = os.getenv('ECOFLOW_API_SECRET')
    sn = os.getenv('ECOFLOW_DEVICE_SN')
    
    if not all([key, secret, sn]):
        log.error("Faltan credenciales. Verifica que el archivo .env contiene ECOFLOW_API_KEY, ECOFLOW_API_SECRET y ECOFLOW_DEVICE_SN.")
        exit(1)
    
    client = EcoFlowClient(api_key=key, api_secret=secret)
    quota = client.get_device_quota(sn=sn)
    
    if quota:
        print("=== ESTADO DEL EQUIPO ECOFLOW ===")
        print(f"Batería: {quota.battery.level}% (Salud: {quota.battery.health}%)")
        print(f"Capacidad: {quota.battery.remain_cap_mah} / {quota.battery.full_cap_mah} mAh")
        print(f"Temperatura: {quota.battery.temp_c}°C")
        
        print("\n--- ENTRADA DE ENERGÍA ---")
        print(f"Total Entrando: {quota.power_in.total_watts} W")
        
        # Matemáticas simples: 130020 mV son ~130.0 V
        if quota.power_in.ac_in_voltage > 0:
            volts_in = quota.power_in.ac_in_voltage / 1000
            print(f"  - AC Pared: {quota.power_in.ac_watts} W ({volts_in:.1f}V @ {quota.power_in.ac_in_freq}Hz)")
        else:
            print(f"  - AC Pared: {quota.power_in.ac_watts} W")
            
        print(f"  - Solar/Coche: {quota.power_in.solar_watts} W")
        if quota.power_in.total_watts > 0:
            print(f"Tiempo estimado para carga completa: {quota.power_in.time_remaining_mins} min")
            
        print("\n--- SALIDA DE ENERGÍA ---")
        print(f"Total Saliendo: {quota.power_out.total_watts} W")
        
        ac_status = "ENCENDIDO" if quota.power_out.ac_enabled else "APAGADO"
        dc_status = "ENCENDIDO" if quota.power_out.dc_enabled else "APAGADO"
        
        print(f"  - Enchufes AC [{ac_status}]: {quota.power_out.ac_watts} W")
        dc_usb_watts = max(0, quota.power_out.total_watts - quota.power_out.ac_watts)
        print(f"  - Puertos DC/USB [{dc_status}]: {dc_usb_watts} W")
        
        if quota.power_out.total_watts > 0:
            mins_restantes = abs(quota.power_out.time_remaining_mins)
            print(f"Tiempo estimado de batería restante: {mins_restantes} min")
    else:
        print("No se pudo obtener la información del equipo.")

if __name__ == "__main__":
    main()
