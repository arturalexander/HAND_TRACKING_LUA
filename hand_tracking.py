import cv2
import mediapipe as mp
import requests

# Inicializa MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Configura la cámara
cap = cv2.VideoCapture(0)
# 🔹 Intentamos aumentar la resolución a 1280x720 (HD) o 1920x1080 (Full HD)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Ancho
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # Alto
# URL del servidor Flask
FLASK_SERVER_URL = "http://127.0.0.1:5000/get_position"

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    hand_points = {}

    if results.multi_hand_landmarks and results.multi_handedness:
        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            # 🔍 Obtener si es la mano izquierda o derecha
            label = results.multi_handedness[idx].classification[0].label  # "Left" o "Right"
            hand_prefix = "L" if label == "Left" else "R"

            # Guardar los 21 puntos de la mano con la etiqueta "L" o "R"
            for i, landmark in enumerate(hand_landmarks.landmark):
                hand_points[f"{hand_prefix}{i}"] = {
                    "x": int(landmark.x * frame.shape[1]), 
                    "y": int(landmark.y * frame.shape[0])
                }

    # 🔍 Verificar si los datos ahora tienen "L" o "R"
    print("Enviando datos a Flask:", hand_points)

    # Enviar datos a Flask
    try:
        requests.post(FLASK_SERVER_URL, json=hand_points)
    except requests.exceptions.RequestException:
        print("No se pudo conectar al servidor Flask")

    cv2.imshow("Hand Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
