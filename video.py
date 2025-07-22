import cv2
import mediapipe as mp
import math

cam = cv2.VideoCapture(0)#default camera
frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

hands = mp.solutions.hands.Hands()
draw = mp.solutions.drawing_utils

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (frame_width, frame_height))

def distance(pt1, pt2):
    return math.hypot(pt2[0] - pt1[0], pt2[1] - pt1[1])

while True:
    ret, frame = cam.read()

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            h, w, c = frame.shape

            # Get thumb tip (4), index tip (8), middle tip (12)
            thumb_tip = hand_landmarks.landmark[4]
            index_tip = hand_landmarks.landmark[8]
            middle_tip = hand_landmarks.landmark[12]

            thumb_xy = (int(thumb_tip.x * w), int(thumb_tip.y * h))
            middle_xy = (int(middle_tip.x * w), int(middle_tip.y * h))
            index_xy = (int(index_tip.x * w), int(index_tip.y * h))

            # Check if thumb and middle finger tips are touching
            if distance(index_xy, middle_xy) < 15:  # pixel distance threshold (tweak if needed)
                print(f"Landmark 8 (index tip) - X: {index_xy[0]}, Y: {index_xy[1]}, Z: {index_tip.z:.4f}")
                cv2.circle(frame, index_xy, 10, (0, 255, 0), cv2.FILLED)  # green circle for index tip
            else:
                cv2.circle(frame, index_xy, 10, (0, 0, 255), 2)  # red circle if condition not met

            draw.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)

    out.write(frame)#write frame to output file
    cv2.imshow('Camera', frame)#diplay captured frame

    if cv2.waitKey(1) & 0xFF == 27:#press escape to exit
        break

cam.release()
out.release()
cv2.destroyAllWindows()