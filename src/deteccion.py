# PARKVISION
# Modulo de deteccion de estacionamientos
 
TOTAL_ESPACIOS = 6
 
def detectar_espacios():
    # True = ocupado, False = libre
    estados = [False, True, False, True, False, False]
    return estados
 
 
if __name__ == "__main__":
    resultado = detectar_espacios()
 
    for numero, ocupado in enumerate(resultado, start=1):
        estado = "Ocupado" if ocupado else "Libre"
        print(f"Espacio {numero}: {estado}")