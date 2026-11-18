

from pathlib import Path
import cv2
 
from procesamiento import procesar_imagen
 
BASE_DIR = Path(__file__).resolve().parent.parent
 

ENTRADA = BASE_DIR / "pruebas_procesamiento" / "entrada"
SALIDA = BASE_DIR / "pruebas_procesamiento" / "salida"
 
SALIDA.mkdir(parents=True, exist_ok=True)
 
 
def probar():
 
    imagenes = [
        "maqueta_1.jpg",
        "maqueta_2.jpg",
        "maqueta_3.jpg"
    ]
 
    for nombre in imagenes:
 
        ruta = ENTRADA / nombre
 
        print("Procesando:", nombre)
 
        imagen = cv2.imread(str(ruta))
 
        if imagen is None:
            print("ERROR: No se encontro:", ruta)
            continue

        resultado = procesar_imagen(imagen)
 
        destino = SALIDA / f"procesada_{nombre}"
 
        if cv2.imwrite(str(destino), resultado):
            print("Guardada correctamente:", destino)
        else:
            print("ERROR: No se pudo guardar:", destino)
 
    print("Proceso terminado.")
 
 
if __name__ == "__main__":
    probar()