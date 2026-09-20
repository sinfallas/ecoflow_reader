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
    
    # Ahora obtenemos por defecto el objeto Pydantic estructurado (DeviceQuota)
    quota = client.get_device_quota(sn=sn)
    
    if quota:
        # Accedemos a los datos de forma limpia y autocompletable
        print("=== ESTADO DEL EQUIPO ECOFLOW ===")
        print(f"Batería: {quota.battery.level}% (Salud: {quota.battery.health}%)")
        print(f"Temperatura: {quota.battery.temp_c}°C")
        
        print("\n--- ENTRADA DE ENERGÍA ---")
        print(f"Total Entrando: {quota.power_in.total_watts} W")
        print(f"  - AC (Pared): {quota.power_in.ac_watts} W")
        print(f"  - Solar/Coche: {quota.power_in.solar_watts} W")
        if quota.power_in.total_watts > 0:
            print(f"Tiempo estimado para carga completa: {quota.power_in.time_remaining_mins} min")
            
        print("\n--- SALIDA DE ENERGÍA ---")
        print(f"Total Saliendo: {quota.power_out.total_watts} W")
        print(f"  - AC (Enchufes): {quota.power_out.ac_watts} W")
        if quota.power_out.total_watts > 0:
            # El tiempo restante suele venir en negativo cuando se está descargando
            mins_restantes = abs(quota.power_out.time_remaining_mins)
            print(f"Tiempo estimado de batería restante: {mins_restantes} min")
            
        # Nota: Si el usuario del CLI quisiera ver el JSON estructurado, 
        # bastaría con imprimir: print(quota.model_dump_json(indent=2))
    else:
        print("No se pudo obtener la información del equipo.")

if __name__ == "__main__":
    main()
