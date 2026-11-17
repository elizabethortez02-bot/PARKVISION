import cv2

metodos = {
    "DirectShow": cv2.CAP_DSHOW,
    "Media Foundation": cv2.CAP_MSMF,
    "Automatico": cv2.CAP_ANY
}

for nombre, metodo in metodos.items():
    for indice in range(5):
        print(f"Probando {nombre}, camara {indice}...")

        camara = cv2.VideoCapture(indice, metodo)

        if camara.isOpened():
            correcto, imagen = camara.read()

            if correcto:
                print(f"FUNCIONA: {nombre}, camara {indice}")
                cv2.imshow(
                    f"{nombre} - Camara {indice}",
                    imagen
                )
                cv2.waitKey(1500)

        camara.release()

cv2.destroyAllWindows()