import argparse
import json
import logging
import os
import sys

from dotenv import load_dotenv

from ecoflow_reader.client import EcoFlowClient
from ecoflow_reader.models import DeviceQuota

logging.basicConfig(level=logging.ERROR, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(description="CLI interactiva para la API de EcoFlow")
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Devuelve el payload JSON original y sin parsear de EcoFlow (Ideal para debugging)",
    )
    args = parser.parse_args()

    load_dotenv()

    key = os.getenv("ECOFLOW_API_KEY")
    secret = os.getenv("ECOFLOW_API_SECRET")
    sn = os.getenv("ECOFLOW_DEVICE_SN")

    # Explicitud absoluta para Mypy
    if key is None or secret is None or sn is None:
        log.error(
            "Faltan credenciales. Verifica que el archivo .env contiene "
            "ECOFLOW_API_KEY, ECOFLOW_API_SECRET y ECOFLOW_DEVICE_SN."
        )
        sys.exit(1)

    client = EcoFlowClient(api_key=key, api_secret=secret)

    # Modo diagnóstico para extraer variables específicas (ej. mapeo de parámetros de escritura)
    if args.raw:
        raw_data = client.get_device_quota(sn=sn, as_model=False)
        if raw_data:
            print(json.dumps(raw_data, indent=2))
        else:
            log.error("No se pudo obtener el JSON original del equipo.")
        return

    quota = client.get_device_quota(sn=sn)

    # Mypy ahora sabe con certeza que "quota" es un objeto Pydantic
    if isinstance(quota, DeviceQuota):
        print("=== ESTADO DEL EQUIPO ECOFLOW ===")
        print(f"Batería: {quota.battery.level}% (Salud: {quota.battery.health}%)")
        print(f"Capacidad: {quota.battery.remain_cap_mah} / {quota.battery.full_cap_mah} mAh")
        print(f"Temperatura: {quota.battery.temp_c}°C")

        print("\n--- ENTRADA DE ENERGÍA ---")
        print(f"Total Entrando: {quota.power_in.total_watts} W")

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
