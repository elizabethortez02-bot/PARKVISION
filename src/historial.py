"""PARKVISION - Registro de cambios de ocupacion.
Responsable: Erick. No modifica Flask ni la deteccion.
"""

import csv
from datetime import datetime
from pathlib import Path

from estadisticas import calcular_estadisticas

RUTA_PREDETERMINADA = (
    Path(__file__).resolve().parent.parent
    / "datos" / "historial_estacionamientos.csv"
)

COLUMNAS = [
    "fecha", "total", "ocupados", "disponibles",
    "porcentaje_ocupacion", "porcentaje_disponibilidad", "estados"
]


def _validar_seis(estados):
    if not isinstance(estados, (list, tuple)) or len(estados) != 6:
        raise ValueError("PARKVISION necesita exactamente 6 estados.")
    if not all(type(valor) is bool for valor in estados):
        raise ValueError("Cada estado debe ser True (ocupado) o False (libre).")


def registrar_cambio(estados, ruta=None, fecha=None):
    """Guarda un registro CSV solo si cambia algun espacio.

    Devuelve True si se guardo un registro y False si no hubo cambios.
    No se llama automaticamente: Xiomara lo integrara en el servidor.
    """
    _validar_seis(estados)
    destino = Path(ruta) if ruta is not None else RUTA_PREDETERMINADA
    destino.parent.mkdir(parents=True, exist_ok=True)
    codigos = "".join("1" if valor else "0" for valor in estados)

    if destino.exists() and destino.stat().st_size > 0:
        with destino.open("r", newline="", encoding="utf-8") as archivo:
            registros = list(csv.DictReader(archivo))
        if registros and registros[-1].get("estados") == codigos:
            return False

    datos = calcular_estadisticas(estados)
    momento = fecha if fecha is not None else datetime.now().astimezone()
    marca = momento.isoformat(timespec="seconds") if isinstance(momento, datetime) else str(momento)
    nuevo = {
        "fecha": marca,
        "total": datos["total"],
        "ocupados": datos["ocupados"],
        "disponibles": datos["disponibles"],
        "porcentaje_ocupacion": datos["porcentaje_ocupacion"],
        "porcentaje_disponibilidad": datos["porcentaje_disponibilidad"],
        "estados": codigos,
    }
    crear_cabecera = not destino.exists() or destino.stat().st_size == 0
    with destino.open("a", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=COLUMNAS)
        if crear_cabecera:
            escritor.writeheader()
        escritor.writerow(nuevo)
    return True


def leer_historial(ruta=None, limite=100):
    """Devuelve los ultimos registros como diccionarios para futuras graficas."""
    if not isinstance(limite, int) or limite < 1:
        raise ValueError("El limite debe ser un entero positivo.")
    destino = Path(ruta) if ruta is not None else RUTA_PREDETERMINADA
    if not destino.exists():
        return []
    with destino.open("r", newline="", encoding="utf-8") as archivo:
        filas = list(csv.DictReader(archivo))
    resultado = []
    for fila in filas[-limite:]:
        resultado.append({
            "fecha": fila["fecha"],
            "total": int(fila["total"]),
            "ocupados": int(fila["ocupados"]),
            "disponibles": int(fila["disponibles"]),
            "porcentaje_ocupacion": float(fila["porcentaje_ocupacion"]),
            "porcentaje_disponibilidad": float(fila["porcentaje_disponibilidad"]),
            "estados": [caracter == "1" for caracter in fila["estados"]],
        })
    return resultado


def resumen_historial(ruta=None):
    """Resumen de registros de cambios, NO de tiempo de permanencia."""
    registros = leer_historial(ruta, limite=1000000)
    if not registros:
        return {"registros": 0, "ocupacion_promedio_registros": 0.0,
                "ocupacion_maxima": 0, "ultima_lectura": None}
    return {
        "registros": len(registros),
        "ocupacion_promedio_registros": round(
            sum(r["porcentaje_ocupacion"] for r in registros) / len(registros), 2
        ),
        "ocupacion_maxima": max(r["ocupados"] for r in registros),
        "ultima_lectura": registros[-1],
    }
