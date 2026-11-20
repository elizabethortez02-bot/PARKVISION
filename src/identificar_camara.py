import cv2

for indice in range(5):
    print(f"Probando camara {indice}...")

    camara = cv2.VideoCapture(indice, cv2.CAP_DSHOW)

    if camara.isOpened():
        correcto, imagen = camara.read()

        if correcto and imagen is not None:
            print(f"Camara {indice}: disponible")
            cv2.imshow(f"Camara {indice}", imagen)
            cv2.waitKey(1500)
        else:
            print(f"Camara {indice}: sin imagen")
    else:
        print(f"Camara {indice}: no disponible")

    camara.release()
    cv2.destroyAllWindows()