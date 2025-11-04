import cv2
import mediapipe as mp
from custom_gesture_manager import CustomGestureManager

class GestureConfigurator:
    """
    Interactive interface for creating and testing custom gestures
    """
    
    def __init__(self):
        self.gesture_manager = CustomGestureManager()
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.cap = cv2.VideoCapture(0)
    
    def show_menu(self):
        """Display main configuration menu"""
        while True:
            print("\n" + "="*50)
            print("        CUSTOM GESTURE CONFIGURATOR")
            print("="*50)
            print("1. Create New Gesture")
            print("2. List All Gestures")
            print("3. Test Gestures (Live Camera)")
            print("4. Delete Gesture")
            print("5. Exit")
            
            choice = input("\nSelect option (1-5): ").strip()
            
            if choice == '1':
                self.create_gesture_flow()
            elif choice == '2':
                self.gesture_manager.list_gestures()
            elif choice == '3':
                self.test_gestures_live()
            elif choice == '4':
                self.delete_gesture_flow()
            elif choice == '5':
                print("Goodbye!")
                break
            else:
                print("Invalid option! Please try again.")
    
    def create_gesture_flow(self):
        """Guide user through creating a new gesture"""
        print("\n--- Create New Gesture ---")
        
        # Get gesture name
        gesture_name = input("Enter gesture name: ").strip()
        if not gesture_name:
            print("Gesture name cannot be empty!")
            return
        
        if gesture_name in self.gesture_manager.gestures_db:
            print("Gesture name already exists!")
            return
        
        # Get action type
        print("\nAvailable action types:")
        print("1. keyboard - Press keys or type text")
        print("2. mouse - Click, scroll, etc.")
        print("3. system - Volume, brightness control")
        print("4. custom - Custom actions")
        
        action_choice = input("Select action type (1-4): ").strip()
        action_types = {'1': 'keyboard', '2': 'mouse', '3': 'system', '4': 'custom'}
        
        if action_choice not in action_types:
            print("Invalid action type!")
            return
        
        action_type = action_types[action_choice]
        action_value = self.get_action_value(action_type)
        
        if not action_value:
            return
        
        # Start recording gesture
        samples_needed = 5
        print(f"\nGet ready to record gesture '{gesture_name}'")
        print("You'll need to show the gesture 5 times")
        input("Press Enter when ready...")
        
        self.record_gesture_camera(gesture_name, action_type, action_value, samples_needed)
    
    def get_action_value(self, action_type):
        """Get the specific action value based on type"""
        if action_type == "keyboard":
            print("\nKeyboard actions:")
            print("Format: 'press:key' or 'press:ctrl+alt+del' or 'type:text'")
            return input("Enter keyboard action: ").strip()
        
        elif action_type == "mouse":
            print("\nMouse actions:")
            print("1. click_left - Left click")
            print("2. click_right - Right click")
            print("3. double_click - Double click")
            print("4. scroll_up - Scroll up")
            print("5. scroll_down - Scroll down")
            
            mouse_actions = {
                '1': 'click_left', '2': 'click_right', '3': 'double_click',
                '4': 'scroll_up', '5': 'scroll_down'
            }
            
            choice = input("Select mouse action (1-5): ").strip()
            return mouse_actions.get(choice, "")
        
        elif action_type == "system":
            print("\nSystem actions:")
            print("1. volume_up - Increase volume")
            print("2. volume_down - Decrease volume")
            print("3. brightness_up - Increase brightness")
            print("4. brightness_down - Decrease brightness")
            
            system_actions = {
                '1': 'volume_up', '2': 'volume_down',
                '3': 'brightness_up', '4': 'brightness_down'
            }
            
            choice = input("Select system action (1-4): ").strip()
            return system_actions.get(choice, "")
        
        else:  # custom
            return input("Enter custom action description: ").strip()
    
    def record_gesture_camera(self, gesture_name, action_type, action_value, samples_needed):
        """Record gesture samples using camera"""
        samples_collected = 0
        
        print(f"\nRecording {samples_needed} samples for '{gesture_name}'")
        print("Show your gesture clearly to the camera")
        print("Press 'c' to capture sample, 'q' to quit")
        
        while samples_collected < samples_needed:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # Flip and convert frame
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process with mediapipe
            results = self.hands.process(rgb_frame)
            
            # Draw instructions
            cv2.putText(frame, f"Sample {samples_collected+1}/{samples_needed}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, "Press 'c' to capture, 'q' to quit", 
                       (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                
                cv2.putText(frame, "Hand detected - Press 'c'", 
                           (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            
            cv2.imshow('Record Gesture', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('c') and results.multi_hand_landmarks:
                self.gesture_manager.record_gesture_sample(results.multi_hand_landmarks[0])
                samples_collected += 1
                print(f"Captured sample {samples_collected}/{samples_needed}")
                
            elif key == ord('q'):
                break
        
        cv2.destroyAllWindows()
        
        if samples_collected >= 3:
            self.gesture_manager.current_gesture = {
                'name': gesture_name,
                'action_type': action_type,
                'action_value': action_value,
                'threshold': 0.85
            }
            self.gesture_manager.finalize_gesture()
        else:
            print("Not enough samples collected. Gesture creation cancelled.")
    
    def test_gestures_live(self):
        """Test custom gestures in real-time"""
        print("\n--- Testing Gestures Live ---")
        print("Show gestures to camera. Recognized gestures will be executed.")
        print("Press 'q' to quit testing.")
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    
                    # Recognize gesture
                    gesture_name, similarity = self.gesture_manager.recognize_gesture(hand_landmarks)
                    
                    if gesture_name:
                        cv2.putText(frame, f"Gesture: {gesture_name} ({similarity:.2f})", 
                                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        
                        # Execute action (with cooldown)
                        self.gesture_manager.execute_gesture_action(gesture_name)
                    else:
                        cv2.putText(frame, "No gesture recognized", 
                                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            cv2.imshow('Test Gestures', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cv2.destroyAllWindows()
    
    def delete_gesture_flow(self):
        """Guide user through deleting a gesture"""
        self.gesture_manager.list_gestures()
        
        if not self.gesture_manager.gestures_db:
            return
        
        gesture_name = input("\nEnter name of gesture to delete: ").strip()
        self.gesture_manager.delete_gesture(gesture_name)

if __name__ == "__main__":
    configurator = GestureConfigurator()
    configurator.show_menu()