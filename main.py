# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import cv2
from gesture import detect_gesture
from tts import speak

app = FastAPI()

# CORS settings – allows frontend on another PC
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for hackathon use
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize webcam once (global object)
cap = cv2.VideoCapture(0)


@app.get("/")
def root():
    return {"message": "Sign2Speech API running"}


@app.get("/predict")
def predict():
    ret, frame = cap.read()
    if not ret:
        return {"error": "Webcam read failed"}

    gesture = detect_gesture(frame)
    return {"gesture": gesture}


@app.get("/speak")
def speak_gesture(text: str):
    speak(text)
    return {"status": "spoken", "text": text}


# -------- Webcam Raw Stream Route --------
def gen_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.get("/video_feed")
def video_feed():
    return StreamingResponse(gen_frames(), media_type='multipart/x-mixed-replace; boundary=frame')


# -------- Webcam + Gesture Overlay Route --------
def gen_prediction():
    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        gesture = detect_gesture(frame)

        # Overlay gesture text
        cv2.putText(frame, f'Gesture: {gesture}', (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 255, 0), 3)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.get("/predict_stream")
def predict_stream():
    return StreamingResponse(gen_prediction(), media_type='multipart/x-mixed-replace; boundary=frame')
