
# PARKVISION
# Servidor web principal
# Integracion: Xiomara

import os
from pathlib import Path

import cv2
from flask import Flask, render_template, jsonify

from deteccion import clasificar_espacios
from camara import iniciar_camara
from procesamiento import procesar_imagen
from estadisticas import calcular_estadisticas


# UBICACION DEL PROYECTO
RUTA_PROYECTO = Path(__file__).resolve().parent.parent

# FUENTE DE IMAGEN
# "prueba" = utiliza prueba.jpg
# "camara" = utiliza el modulo de Alejandro
FUENTE_IMAGEN = os.getenv("PARKVISION_FUENTE", "prueba")


# CONFIGURAR FLASK
app = Flask(
    __name__,
    template_folder=str(RUTA_PROYECTO / "templates")
)


# OBTENER IMAGEN SEGUN LA FUENTE
def obtener_imagen():

    if FUENTE_IMAGEN == "prueba":

        ruta_imagen = RUTA_PROYECTO / "prueba.jpg"
        imagen = cv2.imread(str(ruta_imagen))

        if imagen is None:
            raise RuntimeError("No se pudo cargar prueba.jpg")

        return imagen

    elif FUENTE_IMAGEN == "camara":

        # Modulo de Alejandro
        from camara import capturar_fotografia

        imagen = capturar_fotografia()

        if imagen is None:
            raise RuntimeError(
                "No se pudo capturar la imagen de la camara"
            )

        return imagen

    else:
        raise ValueError(
            f"Fuente de imagen no reconocida: {FUENTE_IMAGEN}"
        )


# PAGINA PRINCIPAL - CONDUCTORES
@app.route("/")
def inicio():

    try:
        imagen = obtener_imagen()

        # Deteccion del modulo de David
        estados = clasificar_espacios(imagen)

        # Estadisticas del modulo de Erick
        estadisticas = calcular_estadisticas(estados)

        # Enviar datos a la pagina de Fernanda
        return render_template(
            "index.html",
            estados=estados,
            disponibles=estadisticas["disponibles"],
            ocupados=estadisticas["ocupados"],
            total=estadisticas["total"],
            porcentaje_ocupacion=estadisticas["porcentaje_ocupacion"],
            porcentaje_disponibilidad=estadisticas["porcentaje_disponibilidad"]
        )

    except (ValueError, KeyError, RuntimeError) as error:
        app.logger.error("Error en pagina principal: %s", error)
        return "No se pudo obtener el estado del estacionamiento", 503


# API - ESTADO DE LOS ESTACIONAMIENTOS
@app.route("/api/estado")
def api_estado():

    try:
        # Obtener imagen configurada
        imagen = obtener_imagen()

        # Detectar los seis espacios
        estados = clasificar_espacios(imagen)

        # Calcular estadisticas
        estadisticas = calcular_estadisticas(estados)

        # Entregar resultados en JSON
        return jsonify({
            "total": estadisticas["total"],
            "disponibles": estadisticas["disponibles"],
            "ocupados": estadisticas["ocupados"],
            "porcentaje_ocupacion": estadisticas["porcentaje_ocupacion"],
            "porcentaje_disponibilidad": estadisticas["porcentaje_disponibilidad"],
            "estados": estados,
            "fuente": FUENTE_IMAGEN
        })

    except (ValueError, KeyError, RuntimeError) as error:
        app.logger.error("Error en API: %s", error)

        return jsonify({
            "error": "No se pudo obtener el estado de los estacionamientos"
        }), 503


# ABRIR CAMARA - FUNCION DE ALEJANDRO
@app.route("/camara")
def abrir_camara():

    iniciar_camara()
    return "La camara se ha cerrado correctamente."


# PRUEBA DE PROCESAMIENTO DE CAMARA
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
