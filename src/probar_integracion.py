
# PARKVISION
# Pruebas de integración general
# Responsable: Xiomara

from main import app


def probar_integracion():

    print("\n================================")
    print("  PARKVISION - PRUEBA GENERAL")
    print("================================\n")

    cliente = app.test_client()
    errores = []

    # PRUEBA 1: API
    print("1. Comprobando API...")

    respuesta = cliente.get("/api/estado")

    if respuesta.status_code != 200:
        errores.append("La API no responde correctamente")
        print("   ERROR:", respuesta.status_code)
    else:
        print("   API funcionando correctamente")

        datos = respuesta.get_json()

        # PRUEBA 2: DETECCIÓN
        print("\n2. Comprobando estacionamientos...")

        estados = datos.get("estados", [])

        if (
            len(estados) == 6
            and all(type(e) is bool for e in estados)
        ):
            print("   Se detectaron 6 estacionamientos")

            for numero, ocupado in enumerate(estados, 1):
                estado = "OCUPADO" if ocupado else "LIBRE"
                print(f"   Espacio {numero}: {estado}")

        else:
            errores.append("Los seis estados no son válidos")
            print("   ERROR en los estados")

        # PRUEBA 3: ESTADÍSTICAS
        print("\n3. Comprobando estadísticas...")

        total = datos.get("total")
        libres = datos.get("disponibles")
        ocupados = datos.get("ocupados")

        print("   Total:", total)
        print("   Disponibles:", libres)
        print("   Ocupados:", ocupados)

        if (
            total == 6
            and libres == estados.count(False)
            and ocupados == estados.count(True)
            and libres + ocupados == total
        ):
            print("   Estadísticas correctas")
        else:
            errores.append("Las estadísticas no coinciden")
            print("   ERROR en las estadísticas")

        # PRUEBA 4: PORCENTAJES
        print("\n4. Comprobando porcentajes...")

        porcentaje_o = datos.get("porcentaje_ocupacion")
        porcentaje_d = datos.get("porcentaje_disponibilidad")

        if (
            isinstance(porcentaje_o, (int, float))
            and isinstance(porcentaje_d, (int, float))
            and abs(porcentaje_o + porcentaje_d - 100) < 0.02
        ):
            print("   Ocupación:", porcentaje_o, "%")
            print("   Disponibilidad:", porcentaje_d, "%")
            print("   Porcentajes correctos")
        else:
            errores.append("Los porcentajes son incorrectos")
            print("   ERROR en porcentajes")

        # PRUEBA 5: FUENTE
        print("\n5. Comprobando fuente de imagen...")

        fuente = datos.get("fuente")

        print("   Fuente:", fuente)

        if fuente not in ("prueba", "camara"):
            errores.append("Fuente no reconocida")

    # PRUEBA 6: PÁGINA WEB
    print("\n6. Comprobando página principal...")

    pagina = cliente.get("/")

    if pagina.status_code == 200:
        print("   Página web funcionando")
    else:
        errores.append("La página web presenta un error")
        print("   ERROR:", pagina.status_code)

    # RESULTADO FINAL
    print("\n================================")

    if not errores:
        print(" TODAS LAS PRUEBAS PASARON")
    else:
        print(" SE ENCONTRARON ERRORES")

        for error in errores:
            print(" -", error)

    print("================================\n")

    return len(errores) == 0


if __name__ == "__main__":
    correcto = probar_integracion()
    raise SystemExit(0 if correcto else 1)
