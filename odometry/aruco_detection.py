import cv2
import cv2.aruco as aruco
import numpy as np

# Parámetros de la cámara (usa los tuyos después de calibrarla)
camera_matrix = np.array([[1.01112869e+03, 0.00000000e+00, 6.25027187e+02],
                          [0.00000000e+00, 1.00939931e+03, 3.55205263e+02],
                          [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
dist_coeffs = np.array([[-0.0031836, -0.10976409, 0.00019764, -0.001902, -0.13254417]])

# Tamaño de los ArUcos (en metros)
aruco_size = 0.04

# Diccionario y parámetros de ArUco
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_250)
parameters = cv2.aruco.DetectorParameters()

# Iniciar la cámara
cap = cv2.VideoCapture(1)  # Cambiar a tu cámara

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Detección de ArUcos
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    if ids is not None:
        # Dibujar ArUcos detectados
        frame = cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        # Calcular poses de los ArUcos
        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, aruco_size, camera_matrix, dist_coeffs)

        for i, id in enumerate(ids.flatten()):
            # Dibujar un círculo en el centro del marcador
            center = tuple(corners[i][0].mean(axis=0).astype(int))
            cv2.circle(frame, center, 10, (0, 255, 0), -1)  # Círculo verde en el centro del marcador

            # Dibujar ejes del sistema de coordenadas del marcador
            axis_length = 0.02  # Longitud del eje en metros
            axis = np.float32([[axis_length, 0, 0], [0, axis_length, 0], [0, 0, axis_length]]).reshape(-1, 3)
            imgpts, _ = cv2.projectPoints(axis, rvecs[i], tvecs[i], camera_matrix, dist_coeffs)

            imgpts = np.int32(imgpts).reshape(-1, 2)
            frame = cv2.line(frame, center, tuple(imgpts[0]), (255, 0, 0), 5)  # Eje X en rojo
            frame = cv2.line(frame, center, tuple(imgpts[1]), (0, 255, 0), 5)  # Eje Y en verde
            frame = cv2.line(frame, center, tuple(imgpts[2]), (0, 0, 255), 5)  # Eje Z en azul

            # Imprimir la posición del marcador en la terminal
            print(f"ID {id}: x={tvecs[i][0][0]:.2f} m, y={tvecs[i][0][1]:.2f} m, z={tvecs[i][0][2]:.2f} m")

            if id == 1:
                # Pose del tren
                print(f"Tren (ID 1): rvec={rvecs[i]}, tvec={tvecs[i]}")

            elif id in [2, 3, 4]:
                # Poses de las estaciones
                print(f"Estación {id}: rvec={rvecs[i]}, tvec={tvecs[i]}")

    # Mostrar video
    cv2.imshow("ArUco Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

