
# PARKVISION
# Servidor web principal
# Integracion: Xiomara

import cv2
from flask import Flask, render_template, jsonify
from pathlib import Path

from deteccion import clasificar_espacios
from camara import iniciar_camara
from procesamiento import procesar_imagen
from estadisticas import calcular_estadisticas


# Ubicar la carpeta principal del proyecto
RUTA_PROYECTO = Path(__file__).resolve().parent.parent

# Configurar Flask
app = Flask(
    __name__,
    template_folder=str(RUTA_PROYECTO / "templates")
)


# PAGINA PRINCIPAL
@app.route("/")
def inicio():

    # Cargar la imagen de prueba
    ruta_imagen = RUTA_PROYECTO / "prueba.jpg"
    imagen = cv2.imread(str(ruta_imagen))

    if imagen is None:
        return "Error: No se pudo cargar prueba.jpg", 500

    # Detectar los estados de los estacionamientos
    estados = clasificar_espacios(imagen)

    # Calcular estadisticas usando el modulo de Erick
    estadisticas = calcular_estadisticas(estados)

    # Enviar resultados a la pagina web
    return render_template(
        "index.html",
        estados=estados,
        disponibles=estadisticas["disponibles"],
        ocupados=estadisticas["ocupados"],
        total=estadisticas["total"],
        porcentaje_ocupacion=estadisticas["porcentaje_ocupacion"],
        porcentaje_disponibilidad=estadisticas["porcentaje_disponibilidad"]
    )



# API - ESTADO DE LOS ESTACIONAMIENTOS
@app.route("/api/estado")
def api_estado():

    # Imagen de prueba (temporal)
    ruta_imagen = RUTA_PROYECTO / "prueba.jpg"
    imagen = cv2.imread(str(ruta_imagen))

    if imagen is None:
        return jsonify({
            "error": "No se pudo cargar la imagen de prueba"
        }), 500

    try:
        # Deteccion de los seis estacionamientos
        estados = clasificar_espacios(imagen)

        # Estadisticas del modulo de Erick
        estadisticas = calcular_estadisticas(estados)

        return jsonify({
            "total": estadisticas["total"],
            "disponibles": estadisticas["disponibles"],
            "ocupados": estadisticas["ocupados"],
            "porcentaje_ocupacion": estadisticas["porcentaje_ocupacion"],
            "porcentaje_disponibilidad": estadisticas["porcentaje_disponibilidad"],
            "estados": estados,
            "fuente": "imagen_prueba"
        })

    except (ValueError, KeyError) as error:
        app.logger.error("Error de deteccion: %s", error)
        return jsonify({
            "error": "No se pudieron calcular los estacionamientos"
        }), 500


# ABRIR CAMARA
@app.route("/camara")
def abrir_camara():
    iniciar_camara()
    return "La camara se ha cerrado correctamente."


# PROBAR PROCESAMIENTO DE CAMARA
def probar_procesamiento_camara():

    camara = cv2.VideoCapture(0)

    if not camara.isOpened():
        print("No se pudo abrir la camara.")
        return

    try:
        while True:
            correcto, imagen = camara.read()

            if not correcto:
                print("No se pudo capturar la imagen.")
                break

            procesada = procesar_imagen(imagen)

            cv2.imshow("PARKVISION - Original", imagen)
            cv2.imshow("PARKVISION - Procesada", procesada)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        camara.release()
        cv2.destroyAllWindows()


# INICIAR SERVIDOR
if __name__ == "__main__":
    app.run(debug=True)
