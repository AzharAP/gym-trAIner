import numpy as np
import pyttsx3

tts_engine = pyttsx3.init()

def calculate_angle(a, b, c):
    """
    Calculate the angle between three points.
    :param a: First point (e.g., hip)
    :param b: Second point (e.g., knee)
    :param c: Third point (e.g., ankle)
    :return: Angle in degrees
    """
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

def give_feedback(message):
    """
    Provide audio feedback to the user.
    :param message: Text message to speak
    """
    print(message)
    tts_engine.say(message)
    tts_engine.runAndWait()
