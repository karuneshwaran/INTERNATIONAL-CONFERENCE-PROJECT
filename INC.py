import cv2
from fer import FER
import serial
import time

# Change COM port according to your Arduino
arduino = serial.Serial('COM3', 9600)
time.sleep(2)

detector = FER(mtcnn=True)

camera = cv2.VideoCapture(0)

print("Emotion Detection Started...")

while True:

    ret, frame = camera.read()

    if not ret:
        print("Camera not detected")
        break

    result = detector.detect_emotions(frame)

    if result:

        emotions = result[0]["emotions"]
        top_emotion = max(emotions, key=emotions.get)

        print("Detected Emotion:", top_emotion)

        if top_emotion == "happy":
            arduino.write(b'H')

        elif top_emotion == "neutral":
            arduino.write(b'N')

        elif top_emotion in ["sad","angry","fear","disgust"]:
            arduino.write(b'S')

        cv2.putText(frame, top_emotion, (50,50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0,255,0), 2)

    cv2.imshow("Emotion Detection", frame)

    if cv2.waitKey(1) == 27:
        break

camera.release()
cv2.destroyAllWindows()
arduino.close()