import cv2
import mediapipe as mp

cam = cv2.VideoCapture(0)#default camera
frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

hands = mp.solutions.hands.Hands()
draw = mp.solutions.drawing_utils

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (frame_width, frame_height))

while True:
    ret, frame = cam.read()

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            landmark = hand_landmarks.landmark[8]

            # Get pixel coordinates
            h, w, c = frame.shape
            cx, cy = int(landmark.x * w), int(landmark.y * h)

            # Draw a circle on the landmark
            cv2.circle(frame, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

            # Optional: print coordinates
            print(f"Landmark 8 - X: {cx}, Y: {cy}, Z: {landmark.z:.4f}")

            draw.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)

    out.write(frame)#write frame to output file
    cv2.imshow('Camera', frame)#diplay captured frame

    if cv2.waitKey(1) & 0xFF == 27:#press escape to exit
        break

cam.release()
out.release()
cv2.destroyAllWindows()