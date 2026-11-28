# PARKVISION UNIVERSITY
# Comprobacion de analitica y Smart Assistant
# Responsable: Erick

import time
import tempfile
from pathlib import Path

import gestion as g
from analitica import resumen


def mostrar(c, titulo, online):
    datos = resumen(c, online)
    e = datos["statistics"]

    print("\n" + "=" * 45)
    print(titulo)
    print("=" * 45)
    print("Total:", e["total"])
    print("Ocupados:", e["ocupados"])
    print("Libres fisicos:", e["disponibles"])
    print("Porcentaje de ocupacion:", e["porcentaje_ocupacion"], "%")
    print("Cupos directos:", datos["available"])
    print("Bloqueados:", datos["blocked"])
    print("Reservas y ofertas:", datos["holds"])
    print("Usuarios en espera:", datos["waiting"])
    print("Visitas finalizadas:", datos["completed"])
    print("Tiempo promedio:", datos["average_minutes"], "minutos")

    print("\nROTACION POR ESPACIO")
    for espacio in datos["rotation"]:
        print(f'P{espacio["space"]:02}:', espacio["total"], "visitas")

    print("\nSMART ASSISTANT")
    for alerta in datos["alerts"]:
        print("-", alerta)

    return datos


def ejecutar():
    db_original = g.DB
    try:
        with tempfile.TemporaryDirectory() as carpeta:
            g.DB = Path(carpeta) / "prueba.db"
            g.init()

            with g.tx() as c:
                # Escenario 1: estacionamiento vacio
                datos = mostrar(c, "ESCENARIO 1 - ESTACIONAMIENTO VACIO", True)
                assert datos["available"] == 6

                # Escenario 2: ocupacion parcial
                c.execute(
                    """UPDATE spaces SET occupied = 1
                    WHERE id IN (1, 3, 5)"""
                )
                datos = mostrar(c, "ESCENARIO 2 - OCUPACION PARCIAL", True)
                assert datos["available"] == 3
                assert datos["statistics"]["ocupados"] == 3

                # Escenario 3: demanda alta
                c.execute(
                    """UPDATE spaces SET occupied = 1
                    WHERE id IN (2, 4)"""
                )
                datos = mostrar(c, "ESCENARIO 3 - DEMANDA ALTA", True)
                assert datos["available"] == 1

                # Escenario 4: estacionamiento lleno
                c.execute("UPDATE spaces SET occupied = 1")
                datos = mostrar(c, "ESCENARIO 4 - SIN DISPONIBILIDAD", True)
                assert datos["available"] == 0

                # Escenario 5: camara desconectada
                datos = mostrar(c, "ESCENARIO 5 - CAMARA DESCONECTADA", False)
                assert not datos["online"]

                # Escenario 6: historial de visitas
                ahora = time.time()
                c.execute("UPDATE spaces SET occupied = 0")
                c.executemany(
                    """INSERT INTO visits
                    (plate, space, entered, parked, exited, status)
                    VALUES (?, ?, ?, ?, ?, 'closed')""",
                    [
                        ("DEMO001", 1, ahora - 1800, ahora - 1700, ahora),
                        ("DEMO002", 2, ahora - 3600, ahora - 3500, ahora),
                    ],
                )
                c.execute(
                    """INSERT INTO incidents
                    (space, description, created)
                    VALUES (1, 'Incidente de prueba', ?)""",
                    (ahora,),
                )
                datos = mostrar(c, "ESCENARIO 6 - HISTORIAL DE VISITAS", True)
                assert datos["completed"] == 2
                assert datos["average_minutes"] == 45.0
                assert datos["incidents"] == 1

                # Escenario 7: capacidad comprometida
                c.execute("UPDATE spaces SET blocked = 1 WHERE id = 6")
                c.execute(
                    """INSERT INTO reservations
                    (uid, vid, code, expires, status)
                    VALUES (1, 1, 'DEMO', ?, 'active')""",
                    (ahora + 600,),
                )
                c.execute(
                    """INSERT INTO queue
                    (uid, vid, status)
                    VALUES (2, 2, 'waiting')"""
                )
                datos = mostrar(c, "ESCENARIO 7 - RESERVAS Y ESPERA", True)
                assert datos["blocked"] == 1
                assert datos["holds"] == 1
                assert datos["available"] == 4
                assert datos["waiting"] == 1

            print("\nCOMPROBACIONES FINALIZADAS CORRECTAMENTE")
    finally:
        g.DB = db_original


if __name__ == "__main__":
    ejecutar()