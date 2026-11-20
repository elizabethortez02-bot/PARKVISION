# PARKVISION - Prueba de detección con maqueta real
# Responsable: David

import cv2
import numpy as np
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
CARPETA = BASE / "calibracion_maqueta"

ESPACIOS = [
    (311, 319, 67, 101),
    (397, 321, 63, 98),
    (481, 322, 63, 96),
    (546, 251, 92, 68),
    (547, 163, 92, 68),
    (545, 77, 93, 67)
]

ARCHIVOS = {
    "vacia": "maqueta_vacia.jpg",
    "parcial": "maqueta_parcial.jpg",
    "llena": "maqueta_llena.jpg",
    "validacion": "maqueta_validacion.jpg"
}

imagenes = {}

for nombre, archivo in ARCHIVOS.items():
    ruta = CARPETA / archivo
    imagen = cv2.imread(str(ruta))

    if imagen is None:
        raise SystemExit(f"No se pudo abrir: {ruta}")

    imagenes[nombre] = imagen

referencia = imagenes["vacia"]
alto, ancho = referencia.shape[:2]

for nombre, imagen in imagenes.items():
    if imagen.shape != referencia.shape:
        raise SystemExit(
            f"La imagen {nombre} tiene otra resolución."
        )

for i, (x, y, w, h) in enumerate(ESPACIOS, 1):
    if x < 0 or y < 0 or x + w > ancho or y + h > alto:
        raise SystemExit(
            f"El espacio {i} está fuera de la imagen."
        )

print("Resolución:", ancho, "x", alto)

# Guardar una vista para comprobar las coordenadas
vista = referencia.copy()

for i, (x, y, w, h) in enumerate(ESPACIOS, 1):
    cv2.rectangle(
        vista, (x, y), (x + w, y + h),
        (0, 255, 0), 2
    )
    cv2.putText(
        vista, str(i), (x + 5, y + 22),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65, (0, 255, 0), 2
    )

ruta_vista = CARPETA / "espacios_marcados.jpg"
cv2.imwrite(str(ruta_vista), vista)
print("Vista guardada:", ruta_vista)


def obtener_puntajes(imagen):
    puntajes = []

    for x, y, w, h in ESPACIOS:
        vacio = referencia[y:y+h, x:x+w]
        actual = imagen[y:y+h, x:x+w]

        gris_vacio = cv2.cvtColor(
            vacio, cv2.COLOR_BGR2GRAY
        )
        gris_actual = cv2.cvtColor(
            actual, cv2.COLOR_BGR2GRAY
        )

        gris_vacio = cv2.GaussianBlur(
            gris_vacio, (5, 5), 0
        )
        gris_actual = cv2.GaussianBlur(
            gris_actual, (5, 5), 0
        )

        diferencia = cv2.absdiff(
            gris_vacio, gris_actual
        )

        # Fracción de píxeles que cambiaron
        _, mascara = cv2.threshold(
            diferencia, 25, 255, cv2.THRESH_BINARY
        )

        puntaje = np.count_nonzero(mascara) / mascara.size
        puntajes.append(float(puntaje))

    return puntajes


# Usar la imagen llena como referencia de cambio
puntajes_llena = obtener_puntajes(imagenes["llena"])

umbrales = [
    max(0.015, puntaje * 0.45)
    for puntaje in puntajes_llena
]


def probar(nombre, esperados):
    print("\n================================")
    print("PRUEBA:", nombre.upper())
    print("================================")

    puntajes = obtener_puntajes(imagenes[nombre])
    resultados = []

    for i, puntaje in enumerate(puntajes):
        ocupado = puntaje > umbrales[i]
        resultados.append(ocupado)

        estado = "OCUPADO" if ocupado else "LIBRE"
        correcto = ocupado == esperados[i]

        print(
            f"Espacio {i+1}: {estado} | "
            f"Cambio: {puntaje:.3f} | "
            f"Umbral: {umbrales[i]:.3f} | "
            f"{'OK' if correcto else 'ERROR'}"
        )

    libres = resultados.count(False)
    ocupados = resultados.count(True)

    print("Disponibles:", libres)
    print("Ocupados:", ocupados)

    aprobada = resultados == esperados

    print(
        "RESULTADO:",
        "APROBADA" if aprobada else "REVISAR"
    )

    return aprobada


pruebas = [
    probar("vacia", [False] * 6),
 
    probar(
        "parcial",
        [True, False, True, False, False, True]
    ),
 
    probar("llena", [True] * 6),
 
    probar(
        "validacion",
        [False, True, False, True, True, False]
    )
]

print("\n================================")
print("RESULTADO GENERAL")
print("================================")

if all(pruebas):
    print("LAS TRES PRUEBAS PASARON")
else:
    print("HAY ESPACIOS QUE NECESITAN AJUSTES")

# Comprobar si los vehículos de la imagen llena
# producen suficiente diferencia
for i, puntaje in enumerate(puntajes_llena, 1):
    if puntaje < 0.03:
        print(
            f"ADVERTENCIA: espacio {i} "
            "presenta poca diferencia con la imagen vacía"
        )