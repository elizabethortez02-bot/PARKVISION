
# PARKVISION - Servidor principal
# Integracion: Xiomara

import os
import json
import sqlite3
from pathlib import Path
from datetime import datetime

import cv2
from flask import Flask, render_template, jsonify

from deteccion import clasificar_espacios
from deteccion_maqueta import clasificar_espacios_maqueta
from camara import iniciar_camara, capturar_fotografia
from estadisticas import calcular_estadisticas


BASE = Path(__file__).resolve().parent.parent
CARPETA_MAQUETA = BASE / "calibracion_maqueta"
CARPETA_DATOS = BASE / "datos"
BASE_DATOS = CARPETA_DATOS / "parkvision.db"

FUENTE = os.getenv(
    "PARKVISION_FUENTE", "maqueta"
).strip().lower()

INDICE_CAMARA = int(
    os.getenv("PARKVISION_CAMARA_INDICE", "1")
)

app = Flask(
    __name__,
    template_folder=str(BASE / "templates"),
    static_folder=str(BASE / "static")
)


# BASE DE DATOS

def conectar_bd():
    CARPETA_DATOS.mkdir(
        parents=True, exist_ok=True
    )
    return sqlite3.connect(BASE_DATOS, timeout=10)


def crear_tabla():
    with conectar_bd() as conexion:
        conexion.execute("""
            CREATE TABLE IF NOT EXISTS historial (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                ocupados INTEGER NOT NULL,
                disponibles INTEGER NOT NULL,
                estados TEXT NOT NULL,
                fuente TEXT NOT NULL
            )
        """)


def guardar_historial(estados, estadisticas):
    crear_tabla()

    estados_json = json.dumps(estados)

    with conectar_bd() as conexion:
        ultimo = conexion.execute("""
            SELECT estados, fuente
            FROM historial
            ORDER BY id DESC
            LIMIT 1
        """).fetchone()

        # Guardar solamente cuando cambie el estado
        if ultimo is not None:
            if ultimo == (estados_json, FUENTE):
                return

        fecha = datetime.now().astimezone().isoformat(
            timespec="seconds"
        )

        conexion.execute("""
            INSERT INTO historial
            (fecha, ocupados, disponibles, estados, fuente)
            VALUES (?, ?, ?, ?, ?)
        """, (
            fecha,
            estadisticas["ocupados"],
            estadisticas["disponibles"],
            estados_json,
            FUENTE
        ))


# OBTENER FOTOGRAFIA

def obtener_imagen():

    if FUENTE == "prueba":
        ruta = BASE / "prueba.jpg"
        imagen = cv2.imread(str(ruta))

    elif FUENTE == "maqueta":

        # Permite cambiar fotografias durante las pruebas
        ruta_actual = CARPETA_MAQUETA / "actual.jpg"

        if ruta_actual.exists():
            ruta = ruta_actual
        else:
            ruta = (
                CARPETA_MAQUETA /
                "maqueta_validacion.jpg"
            )

        imagen = cv2.imread(str(ruta))

    elif FUENTE == "camara":
        imagen = capturar_fotografia(
            indice=INDICE_CAMARA
        )

    else:
        raise ValueError(
            f"Fuente no reconocida: {FUENTE}"
        )

    if imagen is None:
        raise RuntimeError(
            "No se pudo obtener la fotografia"
        )

    return imagen


# DETECCION Y ESTADISTICAS

def obtener_estado():

    imagen = obtener_imagen()

    if FUENTE == "prueba":
        estados = clasificar_espacios(imagen)
    else:
        estados = clasificar_espacios_maqueta(imagen)

    estadisticas = calcular_estadisticas(estados)

    return estados, estadisticas


# PAGINA WEB

@app.route("/")
def inicio():
    try:
        estados, estadisticas = obtener_estado()

        return render_template(
            "index.html",
            estados=estados,
            **estadisticas
        )

    except (
        ValueError, RuntimeError,
        OSError, cv2.error, sqlite3.Error
    ) as error:
        app.logger.error("Error en inicio: %s", error)
        return "No se pudo cargar PARKVISION", 503


# API DE ESTADO ACTUAL

@app.route("/api/estado")
def api_estado():
    try:
        estados, estadisticas = obtener_estado()

        guardar_historial(estados, estadisticas)

        return jsonify({
            **estadisticas,
            "estados": estados,
            "fuente": FUENTE
        })

    except (
        ValueError, RuntimeError,
        OSError, cv2.error, sqlite3.Error
    ) as error:
        app.logger.error("Error en API: %s", error)

        return jsonify({
            "error": "No se pudo obtener el estado"
        }), 503


# API DE HISTORIAL

@app.route("/api/historial")
def api_historial():
    try:
        crear_tabla()

        with conectar_bd() as conexion:
            filas = conexion.execute("""
                SELECT id, fecha, ocupados,
                       disponibles, fuente
                FROM historial
                ORDER BY id DESC
                LIMIT 100
            """).fetchall()

        registros = []

        for fila in reversed(filas):
            registros.append({
                "id": fila[0],
                "fecha": fila[1],
                "ocupados": fila[2],
                "disponibles": fila[3],
                "fuente": fila[4]
            })

        return jsonify({
            "total_registros": len(registros),
            "historial": registros
        })

    except (OSError, sqlite3.Error) as error:
        app.logger.error(
            "Error consultando historial: %s", error
        )
        return jsonify({
            "error": "No se pudo consultar el historial"
        }), 503


# CAMARA

@app.route("/camara")
def abrir_camara():
    if FUENTE != "camara":
        return "Activa primero el modo camara", 400

    iniciar_camara(indice=INDICE_CAMARA)
    return "Camara cerrada"


if __name__ == "__main__":
    crear_tabla()
    print("PARKVISION iniciado")
    print("Fuente:", FUENTE)
    print("Historial:", BASE_DATOS)
    app.run(debug=True, use_reloader=False)
