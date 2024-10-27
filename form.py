import cv2
import mediapipe as mp
import numpy as np
import pyttsx3

# Initialize MediaPipe Pose and Text-to-Speech
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
tts_engine = pyttsx3.init()


def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle


def give_feedback(message):
    print(message)
    tts_engine.say(message)
    tts_engine.runAndWait()


def analyze_squat(landmarks):
    hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
           landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
    knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
            landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
    ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
             landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

    angle = calculate_angle(hip, knee, ankle)
    if angle < 90:
        give_feedback("You're squatting too low, raise a bit.")
    elif angle > 120:
        give_feedback("Try to squat lower for better results.")


def analyze_pushup(landmarks):
    shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
             landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
    wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
             landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

    angle = calculate_angle(shoulder, elbow, wrist)
    if angle < 70:
        give_feedback("Lower yourself more to improve your push-up.")
    elif angle > 160:
        give_feedback("Don't lock your elbows at the top.")


def analyze_bicep_curl(landmarks):
    shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
             landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
    wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
             landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

    angle = calculate_angle(shoulder, elbow, wrist)
    if angle < 30:
        give_feedback("Lower your arm fully for a complete curl.")
    elif angle > 150:
        give_feedback("Bring your hand closer to your shoulder for a full contraction.")


# Run exercise selection and analysis
cap = cv2.VideoCapture(0)
exercise = "squat"  # Change this variable to test each exercise

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    if results.pose_landmarks:
        if exercise == "squat":
            analyze_squat(results.pose_landmarks.landmark)
        elif exercise == "pushup":
            analyze_pushup(results.pose_landmarks.landmark)
        elif exercise == "bicep_curl":
            analyze_bicep_curl(results.pose_landmarks.landmark)

    # Display the image for visual feedback
    cv2.imshow("Pose Detection", frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
