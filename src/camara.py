# PARKVISION
# Modulo de captura de camara
 
import cv2
 
 
def iniciar_camara():
    camara = cv2.VideoCapture(0)
 
    if not camara.isOpened():
        print("No se pudo acceder a la camara.")
        return
 
    print("Camara iniciada correctamente.")
    print("Presiona Q para cerrar la ventana.")
 
    while True:
        correcto, imagen = camara.read()
 
        if not correcto:
            print("No se pudo capturar la imagen.")
            break
 
        cv2.imshow("PARKVISION - Camara", imagen)
 
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
 
    camara.release()
    cv2.destroyAllWindows()

def capturar_fotografia():
    camara = cv2.VideoCapture(0)

    if not camara.isOpened():
        print("Error: No se pudo abrir la camara.")
        camara.release()
        return None

    try:
        correcto, imagen = camara.read()

        if not correcto or imagen is None:
            print("Error: No se pudo capturar la fotografia.")
            return None

        print("Fotografia capturada correctamente.")
        return imagen

    finally:
        camara.release()
 
if __name__ == "__main__":
    iniciar_camara()

    
