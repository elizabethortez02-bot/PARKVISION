import cv2

camara = cv2.VideoCapture(1, cv2.CAP_MSMF)

if not camara.isOpened():
    print("No se pudo abrir la camara 1.")
else:
    print("Camara 1 conectada.")
    print("Presiona Q para salir.")

    while True:
        correcto, imagen = camara.read()

        if not correcto:
            print("No se pudo obtener imagen.")
            break

        cv2.imshow("PARKVISION - DroidCam", imagen)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

camara.release()
cv2.destroyAllWindows()