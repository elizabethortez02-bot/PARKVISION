# PARKVISION - Modulo de camara (Alejandro)
# La configuracion puede variar segun la computadora.
import os
import cv2

METODOS = {
    "MSMF": cv2.CAP_MSMF,
    "DSHOW": cv2.CAP_DSHOW,
    "AUTO": cv2.CAP_ANY,
}


def abrir_camara(indice=None, metodo=None):
    """Abre la camara indicada. No confunde 'abierta' con video real."""
    if indice is None:
        indice = int(os.environ.get("PARKVISION_CAMARA_INDICE", "1"))
    if metodo is None:
        metodo = os.environ.get("PARKVISION_CAMARA_METODO", "MSMF")

    metodo = str(metodo).upper()
    if metodo not in METODOS:
        raise ValueError("Metodo no valido: use MSMF, DSHOW o AUTO")

    camara = cv2.VideoCapture(int(indice), METODOS[metodo])
    if not camara.isOpened():
        print(f"No se pudo abrir la camara {indice} con {metodo}.")
        camara.release()
        return None

    print(f"Dispositivo abierto: indice {indice}, metodo {metodo}.")
    print("IMPORTANTE: confirme visualmente que se ve el iPhone, no 'Start DroidCam'.")
    return camara


def capturar_fotografia(indice=None, metodo=None):
    """Obtiene un fotograma; el usuario debe confirmar que es video real."""
    camara = abrir_camara(indice, metodo)
    if camara is None:
        return None

    try:
        imagen = None
        for _ in range(8):
            correcto, fotograma = camara.read()
            if correcto and fotograma is not None and fotograma.size:
                imagen = fotograma
        if imagen is None:
            print("No se recibieron fotogramas validos.")
        return imagen
    finally:
        camara.release()


def iniciar_camara(indice=None, metodo=None):
    """Abre una vista previa. Q para salir."""
    camara = abrir_camara(indice, metodo)
    if camara is None:
        return

    try:
        print("Presione Q en la ventana de video para salir.")
        while True:
            correcto, imagen = camara.read()
            if not correcto or imagen is None:
                print("Se perdio la captura de video.")
                break
            cv2.imshow("PARKVISION - Camara", imagen)
            if (cv2.waitKey(1) & 0xFF) == ord("q"):
                break
    finally:
        camara.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    iniciar_camara()
