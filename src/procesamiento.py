# PARKVISION
# Modulo de procesamiento de imagenes
 
import cv2
 
 
def procesar_imagen(imagen):
    # Convertir la imagen a escala de grises
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
 
    # Reducir el ruido de la imagen
    suavizada = cv2.GaussianBlur(gris, (5, 5), 0)
 
    return suavizada
 
 
if __name__ == "__main__":
    imagen = cv2.imread("prueba.jpg")
 
    if imagen is None:
        print("No se encontro la imagen prueba.jpg")
    else:
        resultado = procesar_imagen(imagen)
 
        cv2.imshow("Imagen original", imagen)
        cv2.imshow("PARKVISION - Procesamiento", resultado)
 
        cv2.waitKey(0)
        cv2.destroyAllWindows()