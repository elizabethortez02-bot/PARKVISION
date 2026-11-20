"""Pruebas del historial de PARKVISION. Ejecutar: python src/probar_historial.py"""

from pathlib import Path
from tempfile import TemporaryDirectory

from historial import registrar_cambio, leer_historial, resumen_historial


def ejecutar_pruebas():
    with TemporaryDirectory() as temporal:
        ruta = Path(temporal) / "historial.csv"

        assert leer_historial(ruta) == []
        print("PRUEBA 1 APROBADA: historial inicialmente vacio")

        estados_a = [False, False, True, False, False, True]
        assert registrar_cambio(estados_a, ruta, "2026-11-20T14:00:00-06:00") is True
        print("PRUEBA 2 APROBADA: guarda primera lectura")

        assert registrar_cambio(estados_a, ruta, "2026-11-20T14:01:00-06:00") is False
        assert len(leer_historial(ruta)) == 1
        print("PRUEBA 3 APROBADA: no duplica estados iguales")

        estados_b = [True, False, True, False, False, True]
        assert registrar_cambio(estados_b, ruta, "2026-11-20T14:02:00-06:00") is True
        datos = leer_historial(ruta)
        assert len(datos) == 2
        assert datos[0]["ocupados"] == 2
        assert datos[1]["ocupados"] == 3
        assert datos[1]["disponibles"] == 3
        assert datos[1]["estados"] == estados_b
        print("PRUEBA 4 APROBADA: cambio de ocupacion registrado")

        resumen = resumen_historial(ruta)
        assert resumen["registros"] == 2
        assert resumen["ocupacion_maxima"] == 3
        assert abs(resumen["ocupacion_promedio_registros"] - 41.67) < 0.02
        print("PRUEBA 5 APROBADA: resumen historico")

        assert len(leer_historial(ruta, limite=1)) == 1
        print("PRUEBA 6 APROBADA: limite de lecturas")

        try:
            registrar_cambio([True, False], ruta)
        except ValueError:
            print("PRUEBA 7 APROBADA: rechaza menos de 6 espacios")
        else:
            raise AssertionError("Debio rechazar menos de 6 espacios")

        try:
            registrar_cambio([1, 0, 0, 0, 0, 0], ruta)
        except ValueError:
            print("PRUEBA 8 APROBADA: rechaza valores no booleanos")
        else:
            raise AssertionError("Debio rechazar valores no booleanos")

    print("\nTODAS LAS PRUEBAS DE HISTORIAL APROBADAS")


if __name__ == "__main__":
    ejecutar_pruebas()
