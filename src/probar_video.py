# PARKVISION
# Prueba de video y captura con DroidCam

import cv2
from pathlib import Path
from datetime import datetime

# Carpeta principal del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Carpeta donde se guardaran las fotografias
CARPETA_FOTOS = BASE_DIR / "pruebas_camara"
CARPETA_FOTOS.mkdir(parents=True, exist_ok=True)

# Camara DroidCam
camara = cv2.VideoCapture(1, cv2.CAP_MSMF)

if not camara.isOpened():
    print("Error: No se pudo abrir DroidCam.")

else:
    print("DroidCam conectado correctamente.")
    print("Presiona F para guardar una fotografia.")
    print("Presiona Q para salir.")

    try:
        while True:
            correcto, imagen = camara.read()

            if not correcto:
                print("Error al capturar imagen.")
                break

            cv2.imshow("PARKVISION - DroidCam", imagen)

            tecla = cv2.waitKey(1) & 0xFF

            if tecla == ord("f"):

                # Fecha y hora para crear nombres diferentes
                fecha = datetime.now().strftime(
                    "%Y%m%d_%H%M%S_%f"
                )

                nombre = f"foto_{fecha}.jpg"

                ruta = CARPETA_FOTOS / nombre

                # Guardar fotografia
                guardada = cv2.imwrite(str(ruta), imagen)

                if guardada:
                    print("Fotografia guardada correctamente.")
                    print("Ubicacion:", ruta)
                else:
                    print("Error al guardar fotografia.")

            elif tecla == ord("q"):
                print("Cerrando DroidCam...")
                break

    finally:
        camara.release()
        cv2.destroyAllWindows()