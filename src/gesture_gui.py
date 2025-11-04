import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import cv2
from PIL import Image, ImageTk
import mediapipe as mp
from custom_gesture_manager import CustomGestureManager
import threading
import time

class GestureGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gesture Control Configurator")
        self.root.geometry("900x600")
        self.root.configure(bg='#2c3e50')
        
        # Initialize gesture manager
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
        
        # Camera state
        self.camera_active = False
        self.current_frame = None
        self.recording = False
        self.samples_collected = 0
        self.samples_needed = 5
        self.current_gesture_data = None
        
        # Setup GUI
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the main GUI layout"""
        # Create main frames
        self.left_frame = tk.Frame(self.root, bg='#34495e', width=300)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        self.right_frame = tk.Frame(self.root, bg='#2c3e50')
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left frame - Controls
        self.setup_controls_frame()
        
        # Right frame - Camera and info
        self.setup_camera_frame()
        self.setup_info_frame()
        
    def setup_controls_frame(self):
        """Setup the controls panel"""
        # Title
        title_label = tk.Label(self.left_frame, text="Gesture Configurator", 
                              font=('Arial', 16, 'bold'), bg='#34495e', fg='white')
        title_label.pack(pady=20)
        
        # Control buttons
        button_style = {'font': ('Arial', 12), 'bg': '#3498db', 'fg': 'white', 
                       'width': 20, 'height': 2, 'bd': 0}
        
        self.create_btn = tk.Button(self.left_frame, text="➕ Create New Gesture", 
                                   command=self.show_create_gesture, **button_style)
        self.create_btn.pack(pady=10)
        
        self.list_btn = tk.Button(self.left_frame, text="📋 List All Gestures", 
                                 command=self.show_gesture_list, **button_style)
        self.list_btn.pack(pady=10)
        
        self.test_btn = tk.Button(self.left_frame, text="🎥 Test Gestures", 
                                 command=self.start_test_mode, **button_style)
        self.test_btn.pack(pady=10)
        
        self.camera_btn = tk.Button(self.left_frame, text="📷 Start Camera", 
                                   command=self.toggle_camera, **button_style)
        self.camera_btn.pack(pady=10)
        
        # Gestures list
        gestures_label = tk.Label(self.left_frame, text="Your Gestures:", 
                                 font=('Arial', 12, 'bold'), bg='#34495e', fg='white')
        gestures_label.pack(pady=(20, 10))
        
        self.gestures_listbox = tk.Listbox(self.left_frame, height=10, font=('Arial', 10))
        self.gestures_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        
        delete_btn = tk.Button(self.left_frame, text="🗑️ Delete Selected", 
                              command=self.delete_selected_gesture,
                              font=('Arial', 10), bg='#e74c3c', fg='white')
        delete_btn.pack(pady=10)
        
        # Status
        self.status_label = tk.Label(self.left_frame, text="Ready", 
                                    font=('Arial', 10), bg='#34495e', fg='#2ecc71')
        self.status_label.pack(pady=10)
        
        self.update_gestures_list()
        
    def setup_camera_frame(self):
        """Setup the camera display frame"""
        camera_frame = tk.Frame(self.right_frame, bg='#2c3e50')
        camera_frame.pack(fill=tk.BOTH, expand=True)
        
        # Camera title
        camera_title = tk.Label(camera_frame, text="Camera Feed", 
                               font=('Arial', 14, 'bold'), bg='#2c3e50', fg='white')
        camera_title.pack(pady=10)
        
        # Camera display
        self.camera_label = tk.Label(camera_frame, text="Camera not active", 
                                    bg='black', fg='white', font=('Arial', 12),
                                    width=80, height=20)
        self.camera_label.pack(pady=10)
        
    def setup_info_frame(self):
        """Setup the information display frame"""
        info_frame = tk.Frame(self.right_frame, bg='#2c3e50')
        info_frame.pack(fill=tk.X, pady=10)
        
        # Info text area
        self.info_text = scrolledtext.ScrolledText(info_frame, height=8, 
                                                  font=('Arial', 10),
                                                  bg='#1a1a1a', fg='white',
                                                  insertbackground='white')
        self.info_text.pack(fill=tk.X)
        self.info_text.insert(tk.END, "Welcome to Gesture Control Configurator!\n\n")
        self.info_text.insert(tk.END, "• Click 'Start Camera' to begin\n")
        self.info_text.insert(tk.END, "• Create custom gestures with 'Create New Gesture'\n")
        self.info_text.insert(tk.END, "• Test your gestures in real-time\n")
        self.info_text.config(state=tk.DISABLED)
        
    def show_create_gesture(self):
        """Show gesture creation dialog"""
        self.create_window = tk.Toplevel(self.root)
        self.create_window.title("Create New Gesture")
        self.create_window.geometry("500x600")
        self.create_window.configure(bg='#34495e')
        self.create_window.transient(self.root)
        self.create_window.grab_set()
        
        # Gesture name
        tk.Label(self.create_window, text="Gesture Name:", 
                font=('Arial', 12, 'bold'), bg='#34495e', fg='white').pack(pady=10)
        self.gesture_name_entry = tk.Entry(self.create_window, font=('Arial', 12), width=30)
        self.gesture_name_entry.pack(pady=5)
        
        # Action type
        tk.Label(self.create_window, text="Action Type:", 
                font=('Arial', 12, 'bold'), bg='#34495e', fg='white').pack(pady=10)
        
        self.action_type = tk.StringVar(value="keyboard")
        action_frame = tk.Frame(self.create_window, bg='#34495e')
        action_frame.pack(pady=5)
        
        tk.Radiobutton(action_frame, text="Keyboard", variable=self.action_type, 
                      value="keyboard", bg='#34495e', fg='white', 
                      selectcolor='#2c3e50').pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(action_frame, text="Mouse", variable=self.action_type, 
                      value="mouse", bg='#34495e', fg='white',
                      selectcolor='#2c3e50').pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(action_frame, text="System", variable=self.action_type, 
                      value="system", bg='#34495e', fg='white',
                      selectcolor='#2c3e50').pack(side=tk.LEFT, padx=10)
        
        # Action value
        self.setup_action_values()
        
        # Record button
        record_btn = tk.Button(self.create_window, text="🎬 Start Recording", 
                              command=self.start_recording,
                              font=('Arial', 12), bg='#e67e22', fg='white',
                              width=20, height=2)
        record_btn.pack(pady=20)
        
        # Recording status
        self.record_status = tk.Label(self.create_window, text="", 
                                     font=('Arial', 10), bg='#34495e', fg='#f39c12')
        self.record_status.pack(pady=10)
        
    def setup_action_values(self):
        """Setup action value selection based on type"""
        self.action_value_frame = tk.Frame(self.create_window, bg='#34495e')
        self.action_value_frame.pack(pady=10, fill=tk.X)
        
        tk.Label(self.action_value_frame, text="Action Value:", 
                font=('Arial', 12, 'bold'), bg='#34495e', fg='white').pack(pady=5)
        
        # Keyboard actions
        self.keyboard_frame = tk.Frame(self.action_value_frame, bg='#34495e')
        self.keyboard_entry = tk.Entry(self.keyboard_frame, font=('Arial', 12), width=30)
        self.keyboard_entry.pack(pady=5)
        self.keyboard_entry.insert(0, "press:ctrl+s")
        
        # Mouse actions
        self.mouse_var = tk.StringVar(value="click_left")
        self.mouse_frame = tk.Frame(self.action_value_frame, bg='#34495e')
        mouse_actions = [
            ("Left Click", "click_left"),
            ("Right Click", "click_right"),
            ("Double Click", "double_click"),
            ("Scroll Up", "scroll_up"),
            ("Scroll Down", "scroll_down")
        ]
        for text, value in mouse_actions:
            tk.Radiobutton(self.mouse_frame, text=text, variable=self.mouse_var,
                          value=value, bg='#34495e', fg='white',
                          selectcolor='#2c3e50').pack(anchor=tk.W)
        
        # System actions
        self.system_var = tk.StringVar(value="volume_up")
        self.system_frame = tk.Frame(self.action_value_frame, bg='#34495e')
        system_actions = [
            ("Volume Up", "volume_up"),
            ("Volume Down", "volume_down"),
            ("Brightness Up", "brightness_up"),
            ("Brightness Down", "brightness_down")
        ]
        for text, value in system_actions:
            tk.Radiobutton(self.system_frame, text=text, variable=self.system_var,
                          value=value, bg='#34495e', fg='white',
                          selectcolor='#2c3e50').pack(anchor=tk.W)
        
        # Show keyboard by default
        self.show_action_values()
        
        # Bind action type change
        self.action_type.trace('w', self.on_action_type_change)
    
    def on_action_type_change(self, *args):
        """Handle action type change"""
        self.show_action_values()
    
    def show_action_values(self):
        """Show appropriate action value controls"""
        # Hide all frames
        self.keyboard_frame.pack_forget()
        self.mouse_frame.pack_forget()
        self.system_frame.pack_forget()
        
        # Show selected frame
        if self.action_type.get() == "keyboard":
            self.keyboard_frame.pack(fill=tk.X)
        elif self.action_type.get() == "mouse":
            self.mouse_frame.pack(fill=tk.X)
        elif self.action_type.get() == "system":
            self.system_frame.pack(fill=tk.X)
    
    def get_action_value(self):
        """Get the selected action value"""
        if self.action_type.get() == "keyboard":
            return self.keyboard_entry.get().strip()
        elif self.action_type.get() == "mouse":
            return self.mouse_var.get()
        elif self.action_type.get() == "system":
            return self.system_var.get()
        return ""
    
    def start_recording(self):
        """Start recording gesture samples"""
        gesture_name = self.gesture_name_entry.get().strip()
        action_value = self.get_action_value()
        
        if not gesture_name:
            messagebox.showerror("Error", "Please enter a gesture name")
            return
        
        if not action_value:
            messagebox.showerror("Error", "Please select an action value")
            return
        
        if gesture_name in self.gesture_manager.gestures_db:
            messagebox.showerror("Error", "Gesture name already exists!")
            return
        
        # Store gesture data
        self.current_gesture_data = {
            'name': gesture_name,
            'action_type': self.action_type.get(),
            'action_value': action_value
        }
        
        # Start recording
        self.recording = True
        self.samples_collected = 0
        self.samples_needed = 5
        
        self.record_status.config(text=f"Recording... 0/{self.samples_needed} samples")
        self.update_status(f"Recording gesture: {gesture_name}")
        
        # Close creation window
        self.create_window.destroy()
        
    def toggle_camera(self):
        """Toggle camera on/off"""
        if not self.camera_active:
            self.start_camera()
        else:
            self.stop_camera()
    
    def start_camera(self):
        """Start camera feed"""
        self.camera_active = True
        self.camera_btn.config(text="📷 Stop Camera", bg='#e74c3c')
        self.update_status("Camera started")
        self.update_camera()
    
    def stop_camera(self):
        """Stop camera feed"""
        self.camera_active = False
        self.camera_btn.config(text="📷 Start Camera", bg='#3498db')
        self.update_status("Camera stopped")
        self.camera_label.config(image='', text="Camera not active")
    
    def update_camera(self):
        """Update camera feed"""
        if self.camera_active:
            ret, frame = self.cap.read()
            if ret:
                # Process frame
                frame = cv2.flip(frame, 1)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.hands.process(rgb_frame)
                
                # Handle different modes
                if self.recording:
                    frame = self.handle_recording_mode(frame, results)
                else:
                    frame = self.handle_normal_mode(frame, results)
                
                # Convert to PhotoImage
                frame = cv2.resize(frame, (640, 480))
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                
                self.camera_label.imgtk = imgtk
                self.camera_label.configure(image=imgtk)
            
            # Schedule next update
            self.root.after(10, self.update_camera)
    
    def handle_recording_mode(self, frame, results):
        """Handle frame processing in recording mode"""
        # Draw recording info
        cv2.putText(frame, f"Recording: {self.current_gesture_data['name']}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, f"Samples: {self.samples_collected}/{self.samples_needed}", 
                   (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "Show gesture and press SPACE to capture", 
                   (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
            
            cv2.putText(frame, "Hand detected - Press SPACE", 
                       (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
        
        return frame
    
    def handle_normal_mode(self, frame, results):
        """Handle frame processing in normal mode"""
        cv2.putText(frame, "Normal Mode - Press 'q' in window to stop", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                
                # Check for gestures
                gesture_name, similarity = self.gesture_manager.recognize_gesture(hand_landmarks)
                if gesture_name and similarity > 0.85:
                    cv2.putText(frame, f"Gesture: {gesture_name} ({similarity:.2f})", 
                               (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        return frame
    
    def start_test_mode(self):
        """Start gesture testing mode"""
        if not self.camera_active:
            self.start_camera()
        
        self.update_status("Testing mode - Show gestures to camera")
        self.add_info("Testing mode started. Show gestures to camera.")
    
    def show_gesture_list(self):
        """Show detailed gesture list"""
        if not self.gesture_manager.gestures_db:
            messagebox.showinfo("Gestures", "No gestures created yet!")
            return
        
        list_window = tk.Toplevel(self.root)
        list_window.title("All Gestures")
        list_window.geometry("600x400")
        
        # Create treeview
        tree = ttk.Treeview(list_window, columns=('Name', 'Type', 'Action'), show='headings')
        tree.heading('Name', text='Gesture Name')
        tree.heading('Type', text='Action Type')
        tree.heading('Action', text='Action Value')
        
        for name, data in self.gesture_manager.gestures_db.items():
            tree.insert('', tk.END, values=(name, data['action_type'], data['action_value']))
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def update_gestures_list(self):
        """Update the gestures listbox"""
        self.gestures_listbox.delete(0, tk.END)
        for name in self.gesture_manager.gestures_db.keys():
            self.gestures_listbox.insert(tk.END, name)
    
    def delete_selected_gesture(self):
        """Delete selected gesture"""
        selection = self.gestures_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a gesture to delete")
            return
        
        gesture_name = self.gestures_listbox.get(selection[0])
        if messagebox.askyesno("Confirm", f"Delete gesture '{gesture_name}'?"):
            self.gesture_manager.delete_gesture(gesture_name)
            self.update_gestures_list()
            self.update_status(f"Deleted gesture: {gesture_name}")
    
    def update_status(self, message):
        """Update status label"""
        self.status_label.config(text=message)
        self.root.update()
    
    def add_info(self, message):
        """Add message to info text area"""
        self.info_text.config(state=tk.NORMAL)
        self.info_text.insert(tk.END, f"\n{message}")
        self.info_text.see(tk.END)
        self.info_text.config(state=tk.DISABLED)
    
    def on_key_press(self, event):
        """Handle key presses for recording"""
        if self.recording and event.keysym == 'space':
            self.capture_sample()
    
    def capture_sample(self):
        """Capture a gesture sample"""
        if self.recording and self.samples_collected < self.samples_needed:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.hands.process(rgb_frame)
                
                if results.multi_hand_landmarks:
                    self.gesture_manager.record_gesture_sample(results.multi_hand_landmarks[0])
                    self.samples_collected += 1
                    
                    self.update_status(f"Sample {self.samples_collected}/{self.samples_needed} captured")
                    
                    if self.samples_collected >= self.samples_needed:
                        self.finish_recording()
    
    def finish_recording(self):
        """Finish recording and save gesture"""
        self.recording = False
        
        if self.samples_collected >= 3:
            self.gesture_manager.current_gesture = {
                'name': self.current_gesture_data['name'],
                'action_type': self.current_gesture_data['action_type'],
                'action_value': self.current_gesture_data['action_value'],
                'threshold': 0.85
            }
            
            if self.gesture_manager.finalize_gesture():
                self.update_gestures_list()
                self.add_info(f"✅ Created gesture: {self.current_gesture_data['name']}")
                self.update_status(f"Gesture '{self.current_gesture_data['name']}' created!")
            else:
                self.update_status("Failed to create gesture")
        else:
            messagebox.showwarning("Warning", "Not enough samples collected")
            self.update_status("Recording cancelled - not enough samples")
    
    def __del__(self):
        """Cleanup when closing"""
        if self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()

def main():
    root = tk.Tk()
    app = GestureGUI(root)
    
    # Bind key events
    root.bind('<KeyPress>', app.on_key_press)
    root.focus_set()
    
    # Handle window close
    def on_closing():
        app.stop_camera()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()