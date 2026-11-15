
# PARKVISION
# Seleccion de las areas de estacionamiento

import cv2
from pathlib import Path

RUTA = Path(__file__).resolve().parent.parent / "prueba.jpg"

imagen = cv2.imread(str(RUTA))

if imagen is None:
    print("No se encontro prueba.jpg")
    raise SystemExit

espacios = []
punto_inicial = None

def seleccionar_espacio(evento, x, y, flags, param):
    global punto_inicial

    if len(espacios) >= 6:
        return

    if evento == cv2.EVENT_LBUTTONDOWN:
        if punto_inicial is None:
            punto_inicial = (x, y)
            print("Primera esquina:", punto_inicial)
        else:
            x1, y1 = punto_inicial
            x2, y2 = x, y

            izquierda = min(x1, x2)
            arriba = min(y1, y2)
            derecha = max(x1, x2)
            abajo = max(y1, y2)

            rectangulo = (
                izquierda,
                arriba,
                derecha - izquierda,
                abajo - arriba
            )

            espacios.append(rectangulo)

            cv2.rectangle(
                imagen,
                (izquierda, arriba),
                (derecha, abajo),
                (0, 255, 0),
                2
            )

            cv2.putText(
                imagen,
                str(len(espacios)),
                (izquierda, arriba - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

            print(f"Espacio {len(espacios)}: {rectangulo}")
            punto_inicial = None

cv2.namedWindow("PARKVISION - Marcar espacios")
cv2.setMouseCallback(
    "PARKVISION - Marcar espacios",
    seleccionar_espacio
)

print("Marca dos esquinas por estacionamiento.")
print("Selecciona un total de 6 estacionamientos.")

while True:
    cv2.imshow("PARKVISION - Marcar espacios", imagen)

    tecla = cv2.waitKey(1) & 0xFF

    if tecla == ord("q") or len(espacios) == 6:
        break

cv2.destroyAllWindows()

print("Rectangulos:", espacios)
