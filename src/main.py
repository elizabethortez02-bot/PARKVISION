
# PARKVISION
# Servidor web principal

from flask import Flask, render_template
from pathlib import Path
from deteccion import clasificar_espacios
from camara import iniciar_camara
from procesamiento import procesar_imagen

# Ubicar la carpeta templates del proyecto
RUTA_PROYECTO = Path(__file__).resolve().parent.parent

app = Flask(
    __name__,
    template_folder=str(RUTA_PROYECTO / "templates")
)


@app.route("/")
def inicio():
    import cv2

    ruta_imagen = RUTA_PROYECTO / "prueba.jpg"
    imagen = cv2.imread(str(ruta_imagen))

    if imagen is None:
        return "Error: No se pudo cargar prueba.jpg", 500

    estados = clasificar_espacios(imagen)

    disponibles = estados.count(False)
    ocupados = estados.count(True)

    return render_template(
        "index.html",
        estados=estados,
        disponibles=disponibles,
        ocupados=ocupados,
        total=len(estados)
    )

@app.route("/camara")
def abrir_camara():
    iniciar_camara()
    return "La cámara se ha cerrado correctamente."

def probar_procesamiento_camara():
    import cv2

    camara = cv2.VideoCapture(0)

    if not camara.isOpened():
        print("No se pudo abrir la camara.")
        return

    while True:
        correcto, imagen = camara.read()

        if not correcto:
            break

        procesada = procesar_imagen(imagen)

        cv2.imshow("PARKVISION - Original", imagen)
        cv2.imshow("PARKVISION - Procesada", procesada)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camara.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    app.run(debug=True)