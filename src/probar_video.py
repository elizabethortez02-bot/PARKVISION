# PARKVISION - Diagnostico visual de DroidCam
# Ejecutar desde la carpeta raiz: python src/probar_video.py
import cv2
from pathlib import Path
from datetime import datetime
from camara import abrir_camara

BASE_DIR = Path(__file__).resolve().parent.parent
CARPETA_FOTOS = BASE_DIR / "pruebas_camara"
CARPETA_FOTOS.mkdir(parents=True, exist_ok=True)

print("\nPARKVISION - PRUEBA DE DROIDCAM")
print("1. Primero conecte el iPhone en DroidCam Client.")
print("2. Verifique que el video se vea en el cliente de Windows.")
print("3. Cierre otras aplicaciones que esten usando la camara.")

try:
    texto_indice = input("Indice de camara [1]: ").strip()
    indice = int(texto_indice) if texto_indice else 1
    metodo = input("Metodo MSMF / DSHOW / AUTO [MSMF]: ").strip().upper() or "MSMF"
except ValueError:
    raise SystemExit("Indice invalido: escriba un numero entero.")

camara = abrir_camara(indice, metodo)
if camara is None:
    raise SystemExit("No se abrio la camara. Pruebe otro indice o metodo.")

print("\nObserve la ventana de video.")
print("Si aparece 'Start DroidCam', la conexion con el telefono NO funciona.")
print("F = guardar foto; Q = cerrar. Guarde solo si se ve la maqueta.")

try:
    while True:
        correcto, imagen = camara.read()
        if not correcto or imagen is None:
            print("No se recibio un fotograma valido.")
            break

        cv2.imshow("PARKVISION - Verificar video real", imagen)
        tecla = cv2.waitKey(1) & 0xFF

        if tecla == ord("f"):
            nombre = "foto_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f") + ".jpg"
            ruta = CARPETA_FOTOS / nombre
            if cv2.imwrite(str(ruta), imagen):
                print("Fotografia guardada:", ruta)
                print("Resolucion:", imagen.shape[1], "x", imagen.shape[0])
                print("Compruebe que se vea la maqueta en la foto.")
            else:
                print("Error al guardar la fotografia.")
        elif tecla == ord("q"):
            break
finally:
    camara.release()
    cv2.destroyAllWindows()
