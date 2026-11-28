
# PARKVISION UNIVERSITY
# Visualizacion de ocupacion en tiempo real
# Responsable: David
 
import cv2
import time
from pathlib import Path
 
from vision import Vision
from camara_continua import Camara
 
 
BASE = Path(__file__).resolve().parent.parent
 
vision = Vision()
camara = None
 
print("\nPARKVISION - VISION ARTIFICIAL")
print("1. Procesar fotografia de calibracion")
print("2. Procesar video de DroidCam")
 
opcion = input("Seleccione una opcion: ").strip()
 
if opcion not in ("1", "2"):
    raise SystemExit("Opcion incorrecta")
 
try:
 
    if opcion == "1":
 
        print("\nFotografias disponibles:")
        print("maqueta_vacia.jpg")
        print("maqueta_llena.jpg")
        print("maqueta_parcial.jpg")
        print("maqueta_validacion.jpg")
 
        nombre = input(
            "Nombre de la fotografia: "
        ).strip()
 
        ruta = BASE / "calibracion_maqueta" / nombre
 
        imagen = cv2.imread(str(ruta))
 
        if imagen is None:
            raise RuntimeError(
                f"No se encontro: {ruta}"
            )
 
    else:
 
        texto = input(
            "Indice de camara [1]: "
        ).strip()
 
        indice = int(texto) if texto else 1
 
        camara = Camara(indice)
 
    print("\nPresione Q para salir")
 
    estados_confirmados = None
 
    while True:
 
        try:
 
            if camara is not None:
 
                imagen = camara.read()
 
            estados, estable, movimiento = (
                vision.process(imagen.copy())
            )
 
            if estable:
 
                estados_confirmados = estados.copy()
 
            if estados_confirmados is None:
 
                resultado = imagen.copy()
 
                cv2.putText(
                    resultado,
                    "Esperando confirmacion...",
                    (10, 25),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 255),
                    2
                )
 
            else:
 
                espacios = []
 
                for numero, ocupado in enumerate(
                    estados_confirmados,
                    1
                ):
 
                    espacios.append({
                        "id": numero,
                        "occupied": ocupado,
                        "blocked": False,
                        "visit": None
                    })
 
                resultado = vision.annotate(
                    imagen.copy(),
                    espacios
                )
 
                cv2.putText(
                    resultado,
                    f"Movimiento: {movimiento:.1f}%",
                    (10, 72),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 255, 255),
                    1
                )
 
                if not estable:
 
                    cv2.putText(
                        resultado,
                        "Confirmando cambios...",
                        (10, 94),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 255, 255),
                        1
                    )
 
            cv2.imshow(
                "PARKVISION - Vision artificial",
                resultado
            )
 
            if cv2.waitKey(100) & 0xFF == ord("q"):
                break
 
        except RuntimeError as error:
 
            if camara is None:
                raise
 
            print("Sin video:", error)
 
            vision.reset()
            estados_confirmados = None
 
            cv2.destroyAllWindows()
 
            time.sleep(1)
 
except KeyboardInterrupt:
 
    print("\nVisualizacion detenida")
 
finally:
 
    if camara is not None:
        camara.close()
 
    cv2.destroyAllWindows()