# gesture.py
import mediapipe as mp
import cv2

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

def detect_gesture(frame):
    import mediapipe as mp
    import cv2

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    mp_draw = mp.solutions.drawing_utils

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            fingers_up = []

            # Get coordinates of necessary landmarks
            lm = hand_landmarks.landmark

            # THUMB (x axis instead of y, because it bends sideways)
            if lm[4].x < lm[3].x:
                fingers_up.append(1)  # thumb is open
            else:
                fingers_up.append(0)

            # For other fingers (compare tip.y < pip.y)
            fingers_up.append(1 if lm[8].y < lm[6].y else 0)   # Index
            fingers_up.append(1 if lm[12].y < lm[10].y else 0) # Middle
            fingers_up.append(1 if lm[16].y < lm[14].y else 0) # Ring
            fingers_up.append(1 if lm[20].y < lm[18].y else 0) # Pinky

            # Convert to a string for easy comparison
            finger_code = ''.join(map(str, fingers_up))  # e.g., "01100"

            # Map to gestures
            if finger_code == "11111":
                return "Hello"
            elif finger_code == "00000":
                return "No"
            elif finger_code == "01000":
                return "Yes"
            elif finger_code == "01100":
                return "Peace"
            elif finger_code == "10101":
                return "Help"
            else:
                return "Unrecognized"

    return "No Gesture"
