import os
import json
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
    payload = client.get_device_quota(sn=sn)
    
    if payload:
        print(json.dumps(payload, indent=2))
    else:
        print("No se pudo obtener la información del equipo.")

if __name__ == "__main__":
    main()
