import cv2
from src.camara import capturar_fotografia

# Cambiar el índice si DroidCam utiliza otro
imagen = capturar_fotografia(indice=1)

if imagen is None:
    print("ERROR: No se pudo capturar la imagen.")
else:
    cv2.imwrite("captura_maqueta.jpg", imagen)
    print("Fotografía guardada correctamente.")
    print("Resolución:", imagen.shape[1], "x", imagen.shape[0])