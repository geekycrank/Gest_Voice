# custom_gestures.py

import json
import math
import pyautogui

CUSTOM_GESTURE_FILE = "custom_gestures.json"

class CustomGestureManager:
    """
    Allows users to create, save, and recognize custom gestures.
    Each gesture stores key landmark positions (normalized).
    """

    def __init__(self):
        self.custom_gestures = self.load_custom_gestures()

    def load_custom_gestures(self):
        """Load saved gestures from a JSON file."""
        try:
            with open(CUSTOM_GESTURE_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_custom_gestures(self):
        """Save gestures to file."""
        with open(CUSTOM_GESTURE_FILE, 'w') as f:
            json.dump(self.custom_gestures, f, indent=4)

    def record_gesture(self, gesture_name, hand_landmarks):
        """
        Capture and save key landmark coordinates for a new gesture.
        Example: Only fingertip coordinates are stored.
        """
        coords = {}
        key_points = [4, 8, 12, 16, 20]  # Thumb to pinky tips
        for i in key_points:
            coords[i] = {
                'x': hand_landmarks.landmark[i].x,
                'y': hand_landmarks.landmark[i].y,
                'z': hand_landmarks.landmark[i].z
            }

        self.custom_gestures[gesture_name] = coords
        self.save_custom_gestures()
        print(f"✅ Custom gesture '{gesture_name}' recorded and saved!")

    def recognize_custom_gesture(self, hand_landmarks):
        """
        Compare current hand landmarks to stored gestures.
        Uses Euclidean distance for matching.
        """
        if not self.custom_gestures:
            return None

        current = {}
        key_points = [4, 8, 12, 16, 20]
        for i in key_points:
            current[i] = (
                hand_landmarks.landmark[i].x,
                hand_landmarks.landmark[i].y,
                hand_landmarks.landmark[i].z
            )

        for gesture_name, data in self.custom_gestures.items():
            dist_sum = 0
            for i in key_points:
                dx = current[i][0] - data[str(i)]['x']
                dy = current[i][1] - data[str(i)]['y']
                dz = current[i][2] - data[str(i)]['z']
                dist_sum += math.sqrt(dx*dx + dy*dy + dz*dz)
            
            avg_dist = dist_sum / len(key_points)
            if avg_dist < 0.05:  # sensitivity threshold
                return gesture_name
        return None

    def perform_action(self, gesture_name):
        """
        Perform a predefined action for recognized gesture.
        You can expand this mapping as needed.
        """
        actions = {
            "volume_up": lambda: pyautogui.press('volumeup'),
            "volume_down": lambda: pyautogui.press('volumedown'),
            "next_tab": lambda: pyautogui.hotkey('ctrl', 'tab'),
            "screenshot": lambda: pyautogui.hotkey('win', 'prtSc'),
            "custom_click": lambda: pyautogui.click()
        }
        if gesture_name in actions:
            actions[gesture_name]()
            print(f"🎬 Action for '{gesture_name}' executed!")
        else:
            print(f"⚠ No action mapped for '{gesture_name}'")
