import cv2
import mediapipe as mp
from utils import give_feedback, calculate_angle

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

def analyze_exercise(exercise):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not access the camera.")
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Convert the BGR frame to RGB for MediaPipe processing
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)

        if results.pose_landmarks:
            # Draw landmarks and connections on the original frame
            mp_drawing.draw_landmarks(
                frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            print("Pose landmarks detected!")  # Console confirmation

            # Call specific analysis function based on exercise
            if exercise == "squat":
                analyze_squat(results.pose_landmarks.landmark)
            elif exercise == "pushup":
                analyze_pushup(results.pose_landmarks.landmark)
            elif exercise == "bicep_curl":
                analyze_bicep_curl(results.pose_landmarks.landmark)
            else:
                print("Exercise not recognized")

        # Display the frame with landmarks
        cv2.imshow("Pose Detection", frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def analyze_squat(landmarks):
    # Extract points for left hip, left knee, and left ankle
    left_hip = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].x,
                landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].y]
    left_knee = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_KNEE.value].x,
                 landmarks[mp.solutions.pose.PoseLandmark.LEFT_KNEE.value].y]
    left_ankle = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value].x,
                  landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value].y]

    # Calculate the knee angle
    knee_angle = calculate_angle(left_hip, left_knee, left_ankle)

    # Feedback based on knee angle
    if knee_angle < 80:
        give_feedback("You're squatting too low. Raise your body slightly.")
    elif knee_angle > 100:
        give_feedback("Try to squat a bit lower for best results.")
    else:
        give_feedback("Great squat form!")


def analyze_pushup(landmarks):
# Extract points for left shoulder, left elbow, and left wrist
    left_shoulder = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].x,
                     landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].y]
    left_elbow = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value].x,
                  landmarks[mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value].y]
    left_wrist = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST.value].x,
                  landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST.value].y]

    # Calculate the elbow angle
    elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)

    # Feedback based on elbow angle
    if elbow_angle < 70:
        give_feedback("Lower yourself a bit more to complete the push-up.")
    elif elbow_angle > 160:
        give_feedback("Don't lock your elbows at the top position.")
    else:
        give_feedback("Good push-up form!")


def analyze_bicep_curl(landmarks):
    # Extract points
    left_shoulder = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].x,
                     landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].y]
    left_elbow = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value].x,
                  landmarks[mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value].y]
    left_wrist = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST.value].x,
                  landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST.value].y]

    # Calculate angle and print it for debugging
    elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
    print(f"Elbow angle: {elbow_angle}")  # Debugging line

    # Feedback
    if elbow_angle < 30:
        give_feedback("Lower your arm fully to complete the curl.")
    elif elbow_angle > 150:
        give_feedback("Bring your hand closer to your shoulder to get a full contraction.")
    else:
        give_feedback("Nice curl!")
