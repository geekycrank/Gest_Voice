# Imports
import cv2
import mediapipe as mp
import pyautogui
import math
import os # NEW: Added for launching system commands (e.g., opening Spotify)
import time # Optional, for command execution delay/cooldown
from enum import IntEnum
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from google.protobuf.json_format import MessageToDict
import screen_brightness_control as sbcontrol

# NOTE ON FIREBASE INTEGRATION:
# In a real setup, a Python library (like firebase-admin or a REST client) 
# would fetch these mappings from the Firestore collection:
# /artifacts/{appId}/users/{userId}/custom_gestures
# We simulate this data fetch with a placeholder dictionary below.

# --- CUSTOMIZATION MAPPINGS PLACEHOLDER ---
# This dictionary represents data fetched from your web UI via Firestore.
# The keys are the names of the custom gestures you define.
# The values are the action commands they are mapped to.
CUSTOM_MAPPINGS = {
    "Two Finger Spread": "Launch Spotify",
    "Fist-to-Palm Swipe": "Toggle Play/Pause",
    # Add more custom mappings here as users define them in the UI.
}

# --- COMMAND EXECUTION MAPPER ---
# This dictionary maps the action strings from the UI (CUSTOM_MAPPINGS) 
# to the actual Python functions that perform the action.
def launch_spotify():
    """Simulates launching an application."""
    print("EXECUTING: Launch Spotify (Placeholder: os.system('start spotify'))")
    # os.system("start spotify") # Uncomment this for Windows
    pyautogui.hotkey('win', 's')
    pyautogui.write('spotify')
    pyautogui.press('enter')

def toggle_play_pause():
    """Toggles media play/pause."""
    print("EXECUTING: Toggle Play/Pause")
    pyautogui.press('playpause')

COMMAND_ACTIONS = {
    "Launch Spotify": launch_spotify,
    "Toggle Play/Pause": toggle_play_pause,
    "Volume Up": lambda: Controller.changesystemvolume(amount=0.1), # Example using lambda for existing controller function
    "Volume Down": lambda: Controller.changesystemvolume(amount=-0.1), # Example using lambda for existing controller function
    # NOTE: You'll need to define functions for other commands
}
# -------------------------------------------


pyautogui.FAILSAFE = False
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Gesture Encodings 
class Gest(IntEnum):
    # Binary Encoded
    """
    Enum for mapping all hand gesture to binary number.
    """

    FIST = 0
    PINKY = 1
    RING = 2
    MID = 4
    LAST3 = 7
    INDEX = 8
    FIRST2 = 12
    LAST4 = 15
    THUMB = 16 
    PALM = 31
    
    # Extra Mappings
    V_GEST = 33
    TWO_FINGER_CLOSED = 34
    PINCH_MAJOR = 35
    PINCH_MINOR = 36
    
    # --- NEW CUSTOM GESTURE CODES ---
    # We define a custom action code and a sample custom pattern code (1 | 16 = 17)
    CUSTOM_ACTION = 99 # Code to signal that a custom action is being executed
    CUSTOM_PATTERN_TWO_FINGER_SPREAD = 17 # PINKY(1) | THUMB(16)
    # -----------------------------------

# Multi-handedness Labels
class HLabel(IntEnum):
    MINOR = 0
    MAJOR = 1

# Convert Mediapipe Landmarks to recognizable Gestures
class HandRecog:
    """
    Convert Mediapipe Landmarks to recognizable Gestures.
    """
    
    def __init__(self, hand_label):
        """
        Constructs all the necessary attributes for the HandRecog object.
        ... (existing comments)
        """

        self.finger = 0
        self.ori_gesture = Gest.PALM
        self.prev_gesture = Gest.PALM
        self.frame_count = 0
        self.hand_result = None
        self.hand_label = hand_label
        self.detected_command = None # NEW: Stores the command string for custom gestures
    
    # --- EXISTING HELPER METHODS (update_hand_result, get_signed_dist, get_dist, get_dz) ---
    def update_hand_result(self, hand_result):
        self.hand_result = hand_result

    def get_signed_dist(self, point):
        """returns signed euclidean distance between 'point'."""
        sign = -1
        if self.hand_result.landmark[point[0]].y < self.hand_result.landmark[point[1]].y:
            sign = 1
        dist = (self.hand_result.landmark[point[0]].x - self.hand_result.landmark[point[1]].x)**2
        dist += (self.hand_result.landmark[point[0]].y - self.hand_result.landmark[point[1]].y)**2
        dist = math.sqrt(dist)
        return dist*sign
    
    def get_dist(self, point):
        """returns euclidean distance between 'point'."""
        dist = (self.hand_result.landmark[point[0]].x - self.hand_result.landmark[point[1]].x)**2
        dist += (self.hand_result.landmark[point[0]].y - self.hand_result.landmark[point[1]].y)**2
        dist = math.sqrt(dist)
        return dist
    
    def get_dz(self,point):
        """returns absolute difference on z-axis between 'point'."""
        return abs(self.hand_result.landmark[point[0]].z - self.hand_result.landmark[point[1]].z)
    
    # --- END EXISTING HELPER METHODS ---

    # Function to find Gesture Encoding using current finger_state.
    def set_finger_state(self):
        """
        set 'finger' by computing ratio of distance between finger tip 
        , middle knuckle, base knuckle.
        """
        if self.hand_result == None:
            return

        points = [[8,5,0],[12,9,0],[16,13,0],[20,17,0]]
        self.finger = 0
        self.finger = self.finger | 0 #thumb
        for idx,point in enumerate(points):
            
            dist = self.get_signed_dist(point[:2])
            dist2 = self.get_signed_dist(point[1:])
            
            try:
                ratio = round(dist/dist2,1)
            except:
                # Fallback in case dist2 is zero; use small epsilon with current dist
                ratio = round(dist/0.01,1)

            self.finger = self.finger << 1
            if ratio > 0.5 :
                self.finger = self.finger | 1
    
    # --- NEW: Check for Custom Gesture Patterns ---
    def check_custom_gesture(self):
        """
        Checks the current 'finger' encoding against user-defined custom patterns.
        In a real application, this would iterate through a list of learned 
        patterns and complex criteria (like timing, speed, position) stored in 
        Firestore's training_data_ref.
        """
        self.detected_command = None # Reset command

        # Example 1: Check for "Two Finger Spread" pattern (Pinky and Thumb open = 17)
        if self.finger == Gest.CUSTOM_PATTERN_TWO_FINGER_SPREAD:
            # Check if this gesture name exists in the mappings
            gesture_name = "Two Finger Spread"
            if gesture_name in CUSTOM_MAPPINGS:
                self.detected_command = CUSTOM_MAPPINGS[gesture_name]
                return Gest.CUSTOM_ACTION

        # Example 2: Check for "Fist-to-Palm Swipe" (This is a sequence, not a static pose)
        # NOTE: For sequences like "Fist-to-Palm Swipe", you would need state machine logic 
        # (checking if prev_gesture was FIST and current_gesture is PALM within X frames).
        # We will keep it simple for now, using only static poses.

        return Gest.PALM # No custom gesture detected

    # Handling Fluctations due to noise
    def get_gesture(self):
        """
        returns int representing gesture corresponding to Enum 'Gest'.
        sets 'frame_count', 'ori_gesture', 'prev_gesture', 
        handles fluctations due to noise.
        """
        if self.hand_result == None:
            return Gest.PALM

        current_gesture = Gest.PALM

        # --- NEW: Prioritize Custom Gesture Recognition ---
        custom_gest_result = self.check_custom_gesture()
        if custom_gest_result == Gest.CUSTOM_ACTION:
            current_gesture = Gest.CUSTOM_ACTION
        # ----------------------------------------------------

        elif self.finger in [Gest.LAST3,Gest.LAST4] and self.get_dist([8,4]) < 0.05:
            if self.hand_label == HLabel.MINOR :
                current_gesture = Gest.PINCH_MINOR
            else:
                current_gesture = Gest.PINCH_MAJOR

        elif Gest.FIRST2 == self.finger :
            point = [[8,12],[5,9]]
            dist1 = self.get_dist(point[0])
            dist2 = self.get_dist(point[1])
            ratio = dist1/dist2
            if ratio > 1.7:
                current_gesture = Gest.V_GEST
            else:
                if self.get_dz([8,12]) < 0.1:
                    current_gesture = Gest.TWO_FINGER_CLOSED
                else:
                    current_gesture = Gest.MID
            
        else:
            current_gesture = self.finger
        
        if current_gesture == self.prev_gesture:
            self.frame_count += 1
        else:
            self.frame_count = 0

        self.prev_gesture = current_gesture

        if self.frame_count > 4 :
            self.ori_gesture = current_gesture
        return self.ori_gesture

# Executes commands according to detected gestures
class Controller:
    """
    Executes commands according to detected gestures.
    ... (existing attributes)
    """

    tx_old = 0
    ty_old = 0
    trial = True
    flag = False
    grabflag = False
    pinchmajorflag = False
    pinchminorflag = False
    pinchstartxcoord = None
    pinchstartycoord = None
    pinchdirectionflag = None
    prevpinchlv = 0
    pinchlv = 0
    framecount = 0
    prev_hand = None
    pinch_threshold = 0.3
    
    def getpinchylv(hand_result):
        """returns distance beween starting pinch y coord and current hand position y coord."""
        dist = round((Controller.pinchstartycoord - hand_result.landmark[8].y)*10,1)
        return dist

    def getpinchxlv(hand_result):
        """returns distance beween starting pinch x coord and current hand position x coord."""
        dist = round((hand_result.landmark[8].x - Controller.pinchstartxcoord)*10,1)
        return dist
    
    def changesystembrightness():
        """sets system brightness based on 'Controller.pinchlv'."""
        currentBrightnessLv = sbcontrol.get_brightness(display=0)/100.0
        currentBrightnessLv += Controller.pinchlv/50.0
        if currentBrightnessLv > 1.0:
            currentBrightnessLv = 1.0
        elif currentBrightnessLv < 0.0:
            currentBrightnessLv = 0.0      
        sbcontrol.fade_brightness(int(100*currentBrightnessLv) , start = sbcontrol.get_brightness(display=0))
    
    # MODIFIED: Added optional 'amount' parameter for custom control
    def changesystemvolume(amount=None):
        """sets system volume based on 'Controller.pinchlv' or an explicit amount."""
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        currentVolumeLv = volume.GetMasterVolumeLevelScalar()
        
        if amount is not None:
            # Used for discrete custom commands (e.g., COMMAND_ACTIONS["Volume Up"])
            currentVolumeLv += amount
        else:
            # Used for continuous pinch control
            currentVolumeLv += Controller.pinchlv/50.0

        if currentVolumeLv > 1.0:
            currentVolumeLv = 1.0
        elif currentVolumeLv < 0.0:
            currentVolumeLv = 0.0
        volume.SetMasterVolumeLevelScalar(currentVolumeLv, None)
    
    def scrollVertical():
        """scrolls on screen vertically."""
        pyautogui.scroll(120 if Controller.pinchlv>0.0 else -120)
        
    
    def scrollHorizontal():
        """scrolls on screen horizontally."""
        pyautogui.keyDown('shift')
        pyautogui.keyDown('ctrl')
        pyautogui.scroll(-120 if Controller.pinchlv>0.0 else 120)
        pyautogui.keyUp('ctrl')
        pyautogui.keyUp('shift')

    # Locate Hand to get Cursor Position
    # Stabilize cursor by Dampening
    def get_position(hand_result):
        """
        returns coordinates of current hand position.
        ... (existing comments)
        """
        point = 9
        position = [hand_result.landmark[point].x ,hand_result.landmark[point].y]
        sx,sy = pyautogui.size()
        x_old,y_old = pyautogui.position()
        x = int(position[0]*sx)
        y = int(position[1]*sy)
        if Controller.prev_hand is None:
            Controller.prev_hand = x,y
        delta_x = x - Controller.prev_hand[0]
        delta_y = y - Controller.prev_hand[1]

        distsq = delta_x**2 + delta_y**2
        ratio = 1
        Controller.prev_hand = [x,y]

        if distsq <= 25:
            ratio = 0
        elif distsq <= 900:
            ratio = 0.07 * (distsq ** (1/2))
        else:
            ratio = 2.1
        x , y = x_old + delta_x*ratio , y_old + delta_y*ratio
        return (x,y)

    def pinch_control_init(hand_result):
        """Initializes attributes for pinch gesture."""
        Controller.pinchstartxcoord = hand_result.landmark[8].x
        Controller.pinchstartycoord = hand_result.landmark[8].y
        Controller.pinchlv = 0
        Controller.prevpinchlv = 0
        Controller.framecount = 0

    # Hold final position for 5 frames to change status
    def pinch_control(hand_result, controlHorizontal, controlVertical):
        """
        calls 'controlHorizontal' or 'controlVertical' based on pinch flags, 
        'framecount' and sets 'pinchlv'.
        ... (existing comments)
        """
        if Controller.framecount == 5:
            Controller.framecount = 0
            Controller.pinchlv = Controller.prevpinchlv

            if Controller.pinchdirectionflag == True:
                controlHorizontal() #x

            elif Controller.pinchdirectionflag == False:
                controlVertical() #y

        lvx = Controller.getpinchxlv(hand_result)
        lvy = Controller.getpinchylv(hand_result)
            
        if abs(lvy) > abs(lvx) and abs(lvy) > Controller.pinch_threshold:
            Controller.pinchdirectionflag = False
            if abs(Controller.prevpinchlv - lvy) < Controller.pinch_threshold:
                Controller.framecount += 1
            else:
                Controller.prevpinchlv = lvy
                Controller.framecount = 0

        elif abs(lvx) > Controller.pinch_threshold:
            Controller.pinchdirectionflag = True
            if abs(Controller.prevpinchlv - lvx) < Controller.pinch_threshold:
                Controller.framecount += 1
            else:
                Controller.prevpinchlv = lvx
                Controller.framecount = 0

    # --- MODIFIED: Handle Custom Actions ---
    def handle_controls(gesture, hand_recog_instance): 
        """
        Impliments all gesture functionality, including custom actions.
        The hand_recog_instance is passed to retrieve the detected command string.
        """ 
        hand_result = hand_recog_instance.hand_result
        x,y = None,None
        if gesture != Gest.PALM :
            x,y = Controller.get_position(hand_result)
        
        # flag reset
        if gesture != Gest.FIST and Controller.grabflag:
            Controller.grabflag = False
            pyautogui.mouseUp(button = "left")

        if gesture != Gest.PINCH_MAJOR and Controller.pinchmajorflag:
            Controller.pinchmajorflag = False

        if gesture != Gest.PINCH_MINOR and Controller.pinchminorflag:
            Controller.pinchminorflag = False

        # --- NEW: Custom Action Implementation ---
        if gesture == Gest.CUSTOM_ACTION:
            command_string = hand_recog_instance.detected_command
            if command_string and command_string in COMMAND_ACTIONS:
                print(f"Executing custom command: {command_string}")
                COMMAND_ACTIONS[command_string]()
                time.sleep(1) # Cooldown to prevent immediate re-triggering
            return # Skip built-in logic for custom actions
        # ----------------------------------------

        # implementation of built-in gestures
        if gesture == Gest.V_GEST:
            Controller.flag = True
            pyautogui.moveTo(x, y, duration = 0.1)

        elif gesture == Gest.FIST:
            if not Controller.grabflag : 
                Controller.grabflag = True
                pyautogui.mouseDown(button = "left")
            pyautogui.moveTo(x, y, duration = 0.1)

        elif gesture == Gest.MID and Controller.flag:
            pyautogui.click()
            Controller.flag = False

        elif gesture == Gest.INDEX and Controller.flag:
            pyautogui.click(button='right')
            Controller.flag = False

        elif gesture == Gest.TWO_FINGER_CLOSED and Controller.flag:
            pyautogui.doubleClick()
            Controller.flag = False

        elif gesture == Gest.PINCH_MINOR:
            if Controller.pinchminorflag == False:
                Controller.pinch_control_init(hand_result)
                Controller.pinchminorflag = True
            Controller.pinch_control(hand_result,Controller.scrollHorizontal, Controller.scrollVertical)
        
        elif gesture == Gest.PINCH_MAJOR:
            if Controller.pinchmajorflag == False:
                Controller.pinch_control_init(hand_result)
                Controller.pinchmajorflag = True
            Controller.pinch_control(hand_result,Controller.changesystembrightness, Controller.changesystemvolume)
        
'''
----------------------------------------  Main Class  ----------------------------------------
    Entry point of Gesture Controller
'''


class GestureController:
    """
    Handles camera, obtain landmarks from mediapipe, entry point
    for whole program.
    ... (existing attributes)
    """
    gc_mode = 0
    cap = None
    CAM_HEIGHT = None
    CAM_WIDTH = None
    hr_major = None # Right Hand by default
    hr_minor = None # Left hand by default
    dom_hand = True

    def __init__(self):
        """Initilaizes attributes."""
        GestureController.gc_mode = 1
        GestureController.cap = cv2.VideoCapture(0)
        GestureController.CAM_HEIGHT = GestureController.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        GestureController.CAM_WIDTH = GestureController.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    
    def classify_hands(results):
        """
        sets 'hr_major', 'hr_minor' based on classification(left, right) of 
        hand obtained from mediapipe, uses 'dom_hand' to decide major and
        minor hand.
        """
        left , right = None,None
        try:
            handedness_dict = MessageToDict(results.multi_handedness[0])
            if handedness_dict['classification'][0]['label'] == 'Right':
                right = results.multi_hand_landmarks[0]
            else :
                left = results.multi_hand_landmarks[0]
        except:
            pass

        try:
            handedness_dict = MessageToDict(results.multi_handedness[1])
            if handedness_dict['classification'][0]['label'] == 'Right':
                right = results.multi_hand_landmarks[1]
            else :
                left = results.multi_hand_landmarks[1]
        except:
            pass
        
        if GestureController.dom_hand == True:
            GestureController.hr_major = right
            GestureController.hr_minor = left
        else :
            GestureController.hr_major = left
            GestureController.hr_minor = right

    def start(self):
        """
        Entry point of whole programm, caputres video frame and passes, obtains
        landmark from mediapipe and passes it to 'handmajor' and 'handminor' for
        controlling.
        """
        
        handmajor = HandRecog(HLabel.MAJOR)
        handminor = HandRecog(HLabel.MINOR)

        with mp_hands.Hands(max_num_hands = 2,min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
            while GestureController.cap.isOpened() and GestureController.gc_mode:
                success, image = GestureController.cap.read()

                if not success:
                    print("Ignoring empty camera frame.")
                    continue
                
                image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                results = hands.process(image)
                
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                if results.multi_hand_landmarks: 
                    GestureController.classify_hands(results)
                    
                    # Process Major Hand
                    handmajor.update_hand_result(GestureController.hr_major)
                    handmajor.set_finger_state()
                    gest_major = handmajor.get_gesture()
                    
                    # Process Minor Hand
                    handminor.update_hand_result(GestureController.hr_minor)
                    handminor.set_finger_state()
                    gest_minor = handminor.get_gesture()

                    # Decide which hand/gesture to prioritize for control
                    if gest_minor == Gest.PINCH_MINOR:
                        Controller.handle_controls(gest_minor, handminor)
                    elif gest_major != Gest.PALM:
                        Controller.handle_controls(gest_major, handmajor)
                    elif gest_minor != Gest.PALM:
                        # Fallback for minor hand gestures other than pinch
                        Controller.handle_controls(gest_minor, handminor)
                    else:
                        Controller.prev_hand = None # Reset cursor if no gesture is active

                    
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                else:
                    Controller.prev_hand = None
                cv2.imshow('Gesture Controller', image)
                if cv2.waitKey(5) & 0xFF == 13:
                    break
        GestureController.cap.release()
        cv2.destroyAllWindows()

# uncomment to run directly
if __name__ == "__main__":
    gc1 = GestureController()
    gc1.start()
