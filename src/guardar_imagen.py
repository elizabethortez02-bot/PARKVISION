import cv2
from pathlib import Path
from procesamiento import procesar_imagen


def guardar_imagen_procesada():
    # Ubicar la carpeta principal del proyecto
    ruta_proyecto = Path(__file__).resolve().parent.parent

    # Definir las rutas de entrada y salida
    ruta_original = ruta_proyecto / "prueba.jpg"
    ruta_resultado = ruta_proyecto / "imagen_procesada.jpg"

    # Cargar la imagen original
    imagen = cv2.imread(str(ruta_original))

    if imagen is None:
        print("ERROR: No se pudo cargar prueba.jpg")
        return

    print("Imagen original cargada correctamente.")

    # Procesar la imagen utilizando el modulo existente
    imagen_procesada = procesar_imagen(imagen)

    if imagen_procesada is None:
        print("ERROR: No se pudo procesar la imagen.")
        return

    print("Procesamiento realizado correctamente.")

    # Guardar el resultado
    guardada = cv2.imwrite(
        str(ruta_resultado),
        imagen_procesada
    )

    if guardada:
        print("Imagen procesada guardada correctamente.")
        print("Ubicacion:", ruta_resultado)
    else:
        print("ERROR: No se pudo guardar la imagen.")


if __name__ == "__main__":
    guardar_imagen_procesada()
