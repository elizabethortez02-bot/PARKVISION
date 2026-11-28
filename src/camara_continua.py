# PARKVISION UNIVERSITY
# Captura continua y deteccion de video congelado
# Responsable: Alejandro
 
import cv2
import os
import time
 
 
class Camara:
 
    def __init__(self, indice=1):
 
        self.indice = indice
        self.cap = None
 
        self.ancho = 640
        self.alto = 480
 
        self.conectada = False
        self.ultimo_error = None
        self.ultima_captura = None
        self.backend = None
 
        # Control de imagen congelada
        self.imagen_anterior = None
        self.ultimo_cambio = None
        self.tiempo_congelado = 5.0
        self.umbral_cambio = 0.05
 
    def conectar(self):
 
        if self.cap is not None:
 
            if self.cap.isOpened():
                return
 
            self.close()
 
        if os.name == "nt":
 
            metodos = [
                cv2.CAP_MSMF,
                cv2.CAP_DSHOW
            ]
 
        else:
 
            metodos = [cv2.CAP_ANY]
 
        for metodo in metodos:
 
            captura = cv2.VideoCapture(
                self.indice,
                metodo
            )
 
            if not captura.isOpened():
 
                captura.release()
                continue
 
            captura.set(
                cv2.CAP_PROP_FRAME_WIDTH,
                self.ancho
            )
 
            captura.set(
                cv2.CAP_PROP_FRAME_HEIGHT,
                self.alto
            )
 
            correcto, imagen = captura.read()
 
            if not correcto or imagen is None:
 
                captura.release()
                continue
 
            if imagen.shape != (480, 640, 3):
 
                captura.release()
                continue
 
            self.cap = captura
            self.backend = metodo
 
            return
 
        raise RuntimeError(
            "No se pudo abrir DroidCam "
            "con resolucion 640x480"
        )
 
    def verificar_imagen(self, imagen):
 
        gris = cv2.cvtColor(
            imagen,
            cv2.COLOR_BGR2GRAY
        )
 
        gris = cv2.resize(gris, (160, 120))
 
        ahora = time.monotonic()
 
        if self.imagen_anterior is None:
 
            self.imagen_anterior = gris.copy()
            self.ultimo_cambio = ahora
 
            self.conectada = False
 
            return False
 
        diferencia = cv2.absdiff(
            self.imagen_anterior,
            gris
        )
 
        cambio = float(diferencia.mean())
 
        if cambio > self.umbral_cambio:
 
            self.ultimo_cambio = ahora
            self.conectada = True
 
        self.imagen_anterior = gris.copy()
 
        segundos = ahora - self.ultimo_cambio
 
        if segundos >= self.tiempo_congelado:
 
            self.conectada = False
 
            raise RuntimeError(
                "Video congelado: posible "
                "desconexion de DroidCam"
            )
 
        return self.conectada
 
    def read(self):
 
        try:
 
            self.conectar()
 
            limite = time.monotonic() + 7
 
            while True:
 
                correcto, imagen = self.cap.read()
 
                if not correcto or imagen is None:
 
                    raise RuntimeError(
                        "No se recibio imagen "
                        "de DroidCam"
                    )
 
                if imagen.size == 0:
 
                    raise RuntimeError(
                        "Imagen vacia"
                    )
 
                if imagen.shape != (480, 640, 3):
 
                    raise RuntimeError(
                        "Resolucion incompatible"
                    )
 
                if self.verificar_imagen(imagen):
 
                    self.ultimo_error = None
                    self.ultima_captura = time.time()
 
                    return imagen
 
                if time.monotonic() >= limite:
 
                    raise RuntimeError(
                        "No se confirmo video activo"
                    )
 
                time.sleep(0.03)
 
        except Exception as error:
 
            self.ultimo_error = str(error)
 
            self.close()
 
            raise RuntimeError(
                self.ultimo_error
            ) from error
 
    def estado(self):
 
        segundos_sin_cambio = None
 
        if self.ultimo_cambio is not None:
 
            segundos_sin_cambio = round(
                time.monotonic() - self.ultimo_cambio,
                2
            )
 
        return {
            "conectada": self.conectada,
            "indice": self.indice,
            "ancho": self.ancho,
            "alto": self.alto,
            "ultima_captura": self.ultima_captura,
            "error": self.ultimo_error,
            "backend": self.backend,
            "segundos_sin_cambio": segundos_sin_cambio
        }
 
    def close(self):
 
        if self.cap is not None:
 
            self.cap.release()
            self.cap = None
 
        self.conectada = False
        self.imagen_anterior = None
        self.ultimo_cambio = None