import cv2

# Intenta con los puertos comunes si el 554 no funciona.
rtsp_urls = [
    "rtsp://root:admin@187.190.132.25:554/stream",
    "rtsp://root:admin@187.190.132.25:8554/stream",  # Puerto RTSP alternativo
    "http://root:admin@187.190.132.25:80/video",  # Puerto HTTP común
    "http://root:admin@187.190.132.25:8080/video"  # Puerto HTTP alternativo
]

for rtsp_url in rtsp_urls:
    capture = cv2.VideoCapture(rtsp_url)
    if capture.isOpened():
        print(f"Conexión exitosa usando {rtsp_url}")
        break
    else:
        print(f"Fallo al conectar usando {rtsp_url}")

if not capture.isOpened():
    print("No se puede abrir la cámara con las URLs proporcionadas.")
    exit()

while True:
    ret, frame = capture.read()
    if not ret:
        print("No se puede recibir frame (fin de transmisión?). Exiting ...")
        break

    cv2.imshow('Video en vivo', frame)
    if cv2.waitKey(1) == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
