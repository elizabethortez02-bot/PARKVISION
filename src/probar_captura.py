# PARKVISION
# Prueba de captura de fotografia

import cv2
from camara import capturar_fotografia

imagen = capturar_fotografia()

if imagen is None:
    print("PRUEBA FALLIDA: No se obtuvo una imagen.")
else:
    print("PRUEBA EXITOSA: Imagen recibida.")

    alto, ancho = imagen.shape[:2]

    print(f"Resolucion: {ancho} x {alto}")

    cv2.imshow("PARKVISION - Fotografia capturada", imagen)

    print("Presiona cualquier tecla para cerrar.")

    cv2.waitKey(0)
    cv2.destroyAllWindows()