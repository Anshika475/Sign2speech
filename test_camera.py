import cv2
from gesture import detect_gesture

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gesture = detect_gesture(frame)

    # Display the gesture on the frame
    cv2.putText(frame, f'Gesture: {gesture}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Sign2Speech - Live Feed", frame)

    # Quit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
