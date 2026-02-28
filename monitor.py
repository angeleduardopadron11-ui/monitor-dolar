import requests
from bs4 import BeautifulSoup
from datetime import datetime

def consultar_bcv():
    url = "https://www.bcv.org.ve/"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }
    
    try:
        
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status() 
        
        soup = BeautifulSoup(response.content, "html.parser")
        
        
        dolar_container = soup.find("div", {"id": "dolar"})
        if dolar_container:
            valor = dolar_container.find("strong").text.strip()
            return valor
        else:
            return "No se encontro el contenedor del precio."
            
    except Exception as e:
        return f"Error de conexion: {e}"

if __name__ == "__main__":
    precio = consultar_bcv()
    fecha_hoy = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    
    print("\n" + "="*30)
    print(f" MONITOR DE DIVISAS BCV")
    print("="*30)
    print(f"Fecha: {fecha_hoy}")
    print(f"Precio del Dolar: {precio} Bs.")
    print("="*30 + "\n")