import requests
import sys
import getopt
import time
import os

# Función para obtener el fabricante de la MAC
def get_mac_(mac_address):
    try:
        start_time = time.time()
        # Reemplazamos los guiones con dos puntos
        url = f"https://api.maclookup.app/v2/macs/{mac_address.replace('-', ':')}"
        response = requests.get(url)
        response_time = int((time.time() - start_time) * 1000)

        if response.status_code == 200:
            data = response.json()
            # Cambiado de 'vendor' a 'company'
            vendor = data.get('company', 'No encontrado')
            return vendor, response_time
        else:
            return 'No encontrado', response_time
    except requests.exceptions.RequestException as e:
        return f"Error: {e}", None

# Función para mostrar la tabla ARP
def arp_table():
    try:
        # Ejecuta el comando arp -a y captura la salida
        os.system("arp -a")
    except Exception as e:
        print(f"Error al intentar acceder a la tabla ARP: {e}")

# Función principal que maneja los argumentos
def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hm:a", ["help", "mac=", "arp"])
    except getopt.GetoptError:
        print('Use: OUILookup.py --mac <mac> | --arp | [--help]\n'
                + "--mac: MAC a consultar. P.e. aa:bb:cc:00:00:00.\n"
                + "--arp: muestra los fabricantes de los host disponibles en la tabla arp.\n"
                + "--help: muestra este mensaje y termina.")
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('Use: OUILookup.py --mac <mac> | --arp | [--help]\n'
                + "--mac: MAC a consultar. P.e. aa:bb:cc:00:00:00.\n"
                + "--arp: muestra los fabricantes de los host disponibles en la tabla arp.\n"
                + "--help: muestra este mensaje y termina.")
            sys.exit()
        elif opt in ("-m", "--mac"):
            vendor, response_time = get_mac_(arg)
            print(f"MAC address : {arg}")
            print(f"Fabricante : {vendor}")
            if response_time is not None:
                print(f"Tiempo de respuesta: {response_time}ms")
        elif opt in ("-a", "--arp"):
            print("Tabla ARP:")
            arp_table()

if __name__ == "__main__":
    main(sys.argv[1:])
