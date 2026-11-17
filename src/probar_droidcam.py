# PARKVISION
# Prueba de DroidCam

from pathlib import Path
from datetime import datetime
import time
import cv2

from camara import capturar_fotografia

carpeta = Path("pruebas_camara")
carpeta.mkdir(exist_ok=True)

print("Conecta DroidCam antes de continuar.")
print("Esperando 3 segundos...")
time.sleep(3)

imagen = capturar_fotografia(indice=1)

if imagen is not None:
    fecha = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    archivo = carpeta / f"foto_{fecha}.jpg"

    if cv2.imwrite(str(archivo), imagen):
        print("Fotografia guardada en:", archivo)
    else:
        print("Error al guardar la fotografia.")
else:
    print("No se pudo capturar la fotografia.")