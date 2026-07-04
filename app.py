from gesture_detector import detect_gesture
import cv2
import mediapipe as mp
import numpy as np

from mediapipe.tasks.python import vision
from mediapipe.tasks.python import BaseOptions

# -----------------------------
# MODEL
# -----------------------------
MODEL_PATH = "hand_landmarker.task"

options = vision.HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=vision.RunningMode.IMAGE,
    num_hands=2,
    min_hand_detection_confidence=0.5,
    min_tracking_confidence=0.5,
)

landmarker = vision.HandLandmarker.create_from_options(options)

# -----------------------------
# HAND CONNECTIONS
# -----------------------------
HAND_CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,4),
    (0,5),(5,6),(6,7),(7,8),
    (5,9),(9,10),(10,11),(11,12),
    (9,13),(13,14),(14,15),(15,16),
    (13,17),(17,18),(18,19),(19,20),
    (0,17)
]

# -----------------------------
# CAMERA
# -----------------------------
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open webcam")
    exit()

while True:

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame,1)

    rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb
    )

    result = landmarker.detect(mp_image)

    h,w,_ = frame.shape

    meme = cv2.imread("memes/default.jpg")

    if meme is None:
        meme = np.ones((480,400,3),dtype=np.uint8)*255

    if result.hand_landmarks:

        hand = result.hand_landmarks[0]

        gesture = detect_gesture(hand)

        if gesture == "THUMBS UP":
           meme = cv2.imread("memes/thumbs_up_shinchan.jpg")

        elif gesture == "FIST":
           meme = cv2.imread("memes/fist_cat.jpg")

        elif gesture == "OPEN PALM":
            meme = cv2.imread("memes/open_palm_cat.jpg")

       

        cv2.putText(
            frame,
            gesture,
            (20,80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,255,0),
            2
        )

        for hand in result.hand_landmarks:

            for point in hand:

                x=int(point.x*w)
                y=int(point.y*h)

                cv2.circle(frame,(x,y),6,(0,255,255),-1)

            for start,end in HAND_CONNECTIONS:

                x1=int(hand[start].x*w)
                y1=int(hand[start].y*h)

                x2=int(hand[end].x*w)
                y2=int(hand[end].y*h)

                cv2.line(frame,(x1,y1),(x2,y2),(0,255,0),2)

        cv2.putText(
            frame,
            f"Hands : {len(result.hand_landmarks)}",
            (20,40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255,0,0),
            2
        )
            # -----------------------------
    # Resize Images
    # -----------------------------
    frame = cv2.resize(frame, (640, 480))
    if meme is None:
        meme = np.ones((480,400,3), dtype=np.uint8) * 255
        cv2.putText(
        meme,
        "NO MEME FOUND",
        (40,240),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0,0,255),
        2
    )

   
    meme = cv2.resize(meme, (400, 480))

    # -----------------------------
    # Combine Camera + Meme
    # -----------------------------
    combined = cv2.hconcat([frame, meme])

    # -----------------------------
    # Title
    # -----------------------------
    cv2.putText(
        combined,
        "AI HAND GESTURE MEME CAMERA",
        (220, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2
    )

    # -----------------------------
    # Show Window
    # -----------------------------
    cv2.imshow("AI Hand Gesture Meme Camera", combined)

    # -----------------------------
    # Exit
    # -----------------------------
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# -----------------------------
# Cleanup
# -----------------------------
cap.release()
cv2.destroyAllWindows()