import json
import time
import cv2
import numpy as np
import mediapipe as mp
from datetime import datetime

class CustomGestureManager:
    """
    Allows users to create and manage custom gestures with associated actions
    """
    
    def __init__(self):
        self.gestures_db = {}
        self.current_gesture = None
        self.recording = False
        self.gesture_samples = []
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.7)
        self.load_gestures()
    
    def load_gestures(self):
        """Load custom gestures from JSON file"""
        try:
            with open('custom_gestures.json', 'r') as f:
                self.gestures_db = json.load(f)
            print(f"Loaded {len(self.gestures_db)} custom gestures")
        except FileNotFoundError:
            self.gestures_db = {}
            print("No existing gestures found. Starting fresh.")
    
    def save_gestures(self):
        """Save custom gestures to JSON file"""
        with open('custom_gestures.json', 'w') as f:
            json.dump(self.gestures_db, f, indent=4)
        print(f"Saved {len(self.gestures_db)} gestures to custom_gestures.json")
    
    def extract_landmark_features(self, hand_landmarks):
        """Extract normalized landmark features for gesture recognition"""
        features = []
        
        # Get all landmark coordinates relative to wrist
        wrist = hand_landmarks.landmark[0]
        
        for landmark in hand_landmarks.landmark:
            # Normalize coordinates relative to wrist
            x = landmark.x - wrist.x
            y = landmark.y - wrist.y
            z = landmark.z - wrist.z
            features.extend([x, y, z])
        
        return features
    
    def calculate_similarity(self, features1, features2):
        """Calculate similarity between two gesture feature sets"""
        if len(features1) != len(features2):
            return 0
        
        # Convert to numpy arrays
        arr1 = np.array(features1)
        arr2 = np.array(features2)
        
        # Calculate cosine similarity
        dot_product = np.dot(arr1, arr2)
        norm1 = np.linalg.norm(arr1)
        norm2 = np.linalg.norm(arr2)
        
        if norm1 == 0 or norm2 == 0:
            return 0
        
        similarity = dot_product / (norm1 * norm2)
        return similarity
    
    def record_gesture_sample(self, hand_landmarks):
        """Record a sample of the current gesture"""
        features = self.extract_landmark_features(hand_landmarks)
        self.gesture_samples.append(features)
    
    def create_gesture(self, gesture_name, action_type, action_value, samples_needed=5):
        """Create a new custom gesture"""
        print(f"Recording gesture: {gesture_name}")
        print(f"Please show the gesture {samples_needed} times...")
        
        self.current_gesture = {
            'name': gesture_name,
            'action_type': action_type,
            'action_value': action_value,
            'samples': [],
            'threshold': 0.85  # Similarity threshold
        }
        
        self.recording = True
        self.gesture_samples = []
        return samples_needed
    
    def finalize_gesture(self):
        """Finalize the gesture creation after collecting samples"""
        if len(self.gesture_samples) < 3:
            print("Not enough samples collected!")
            return False
        
        # Store the average features
        avg_features = np.mean(self.gesture_samples, axis=0).tolist()
        
        self.gestures_db[self.current_gesture['name']] = {
            'features': avg_features,
            'action_type': self.current_gesture['action_type'],
            'action_value': self.current_gesture['action_value'],
            'threshold': self.current_gesture['threshold'],
            'created_at': datetime.now().isoformat()
        }
        
        self.save_gestures()
        self.recording = False
        print(f"Gesture '{self.current_gesture['name']}' created successfully!")
        return True
    
    def recognize_gesture(self, hand_landmarks):
        """Recognize if current hand landmarks match any custom gesture"""
        if not self.gestures_db:
            return None, 0
        
        current_features = self.extract_landmark_features(hand_landmarks)
        best_match = None
        highest_similarity = 0
        
        for gesture_name, gesture_data in self.gestures_db.items():
            similarity = self.calculate_similarity(current_features, gesture_data['features'])
            
            if similarity > gesture_data['threshold'] and similarity > highest_similarity:
                highest_similarity = similarity
                best_match = gesture_name
        
        return best_match, highest_similarity
    
    def execute_gesture_action(self, gesture_name):
        """Execute the action associated with a recognized gesture"""
        if gesture_name not in self.gestures_db:
            return False
        
        gesture_data = self.gestures_db[gesture_name]
        action_type = gesture_data['action_type']
        action_value = gesture_data['action_value']
        
        try:
            if action_type == "keyboard":
                self._execute_keyboard_action(action_value)
            elif action_type == "mouse":
                self._execute_mouse_action(action_value)
            elif action_type == "system":
                self._execute_system_action(action_value)
            elif action_type == "custom":
                self._execute_custom_action(action_value)
            
            print(f"Executed: {gesture_name} -> {action_type}: {action_value}")
            return True
            
        except Exception as e:
            print(f"Error executing action for {gesture_name}: {e}")
            return False
    
    def _execute_keyboard_action(self, action_value):
        """Execute keyboard-related actions"""
        import pyautogui
        
        if action_value.startswith("press:"):
            keys = action_value.replace("press:", "").split("+")
            pyautogui.hotkey(*keys)
        elif action_value.startswith("type:"):
            text = action_value.replace("type:", "")
            pyautogui.write(text)
    
    def _execute_mouse_action(self, action_value):
        """Execute mouse-related actions"""
        import pyautogui
        
        if action_value == "click_left":
            pyautogui.click()
        elif action_value == "click_right":
            pyautogui.click(button='right')
        elif action_value == "double_click":
            pyautogui.doubleClick()
        elif action_value == "scroll_up":
            pyautogui.scroll(100)
        elif action_value == "scroll_down":
            pyautogui.scroll(-100)
    
    def _execute_system_action(self, action_value):
        """Execute system-related actions - FIXED VERSION"""
        try:
            if action_value == "volume_up":
                self._change_volume(10)
            elif action_value == "volume_down":
                self._change_volume(-10)
            elif action_value == "brightness_up":
                self._change_brightness(10)
            elif action_value == "brightness_down":
                self._change_brightness(-10)
            else:
                print(f"Unknown system action: {action_value}")
        except Exception as e:
            print(f"Error in system action {action_value}: {e}")
    
    def _execute_custom_action(self, action_value):
        """Execute custom Python code or functions"""
        print(f"Custom action executed: {action_value}")
    
    def _change_volume(self, delta):
        """Change system volume"""
        try:
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            
            current_volume = volume.GetMasterVolumeLevelScalar()
            new_volume = max(0.0, min(1.0, current_volume + delta/100.0))
            volume.SetMasterVolumeLevelScalar(new_volume, None)
            print(f"Volume changed to {int(new_volume * 100)}%")
            
        except Exception as e:
            print(f"Error changing volume: {e}")
    
    def _change_brightness(self, delta):
        """Change system brightness - FIXED VERSION"""
        try:
            import screen_brightness_control as sbc
            
            current_brightness = sbc.get_brightness()
            
            # Handle different return types from sbc.get_brightness()
            if isinstance(current_brightness, list):
                # If it returns a list, take the first value
                current = current_brightness[0] if current_brightness else 50
            elif isinstance(current_brightness, int):
                # If it returns a single integer
                current = current_brightness
            else:
                # Default fallback
                current = 50
            
            new_brightness = max(0, min(100, current + delta))
            sbc.set_brightness(new_brightness)
            print(f"Brightness changed from {current}% to {new_brightness}%")
            
        except Exception as e:
            print(f"Error changing brightness: {e}")
    
    def list_gestures(self):
        """List all available custom gestures"""
        if not self.gestures_db:
            print("No custom gestures available.")
            return
        
        print("\n=== Custom Gestures ===")
        for i, (name, data) in enumerate(self.gestures_db.items(), 1):
            print(f"{i}. {name}: {data['action_type']} -> {data['action_value']}")
    
    def delete_gesture(self, gesture_name):
        """Delete a custom gesture"""
        if gesture_name in self.gestures_db:
            del self.gestures_db[gesture_name]
            self.save_gestures()
            print(f"Gesture '{gesture_name}' deleted.")
        else:
            print(f"Gesture '{gesture_name}' not found.")