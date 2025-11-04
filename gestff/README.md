# 🎤 Gesture & Voice Control System

A unified control system that allows you to control your computer using **gestures** and **voice commands**. Built with Python, MediaPipe, and speech recognition.

## ✨ Features

- **Gesture Control**: Use hand gestures to move cursor, click, scroll, drag, and control brightness/volume
- **Voice Control**: Natural language commands for mouse, keyboard, applications, and media
- **Unified Command System**: Single source of truth for all commands
- **Fuzzy String Matching**: Understands variations in voice commands
- **Extensible Architecture**: Easy to add new commands
- **Cross-Modal Integration**: Use gestures and voice together seamlessly

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd gestff

# Install dependencies
pip install -r requirements.txt
```

### Usage

#### Voice Control Only
```bash
cd src
python Proton.py
```

#### Gesture Control Only
```bash
cd src
python Gesture_Controller.py
```

#### Full System (Recommended)
```bash
cd src
python Proton.py
# Then say: "Proton, launch gesture recognition"
```

## 📋 Voice Commands

After running `Proton.py`, say: **"Proton, [command]"**

### 🖱️ Mouse Control
- "move cursor up/down/left/right"
- "click" or "press left button"
- "right click" or "context click"
- "double click"
- "scroll up/down/left/right"

### 🌐 Browser Control (NEW!)
- "go back" / "previous page"
- "go forward" / "next page"
- "refresh" / "reload"
- "new tab" / "close tab"
- "next tab" / "previous tab"
- "home page"

### 📁 File Operations (NEW!)
- "save" / "save as"
- "open file" / "new file"
- "print"

### ✏️ Text Formatting (NEW!)
- "bold" / "italic" / "underline"
- "strikethrough"
- "find" / "replace"

### 🪟 Window Management (NEW!)
- "snap left" / "snap right"
- "show desktop" / "minimize" / "maximize"
- "switch window" / "task view"
- "lock screen"

### 🖥️ Virtual Desktops (NEW!)
- "new desktop"
- "switch desktop left/right"
- "close desktop"

### ⚙️ System Control
- "open app notepad/calculator/chrome"
- "task manager" / "settings"
- "start menu" / "windows search"
- "take screenshot" / "screenshot region"

### 📧 Email (NEW!)
- "new email" / "compose"
- "send email" / "reply" / "reply all"
- "forward"

### 🌐 Internet & Search
- "google [query]" or "search [query]"
- "youtube [query]"

### 🎵 Media Control
- "play music" / "pause music"
- "next song" / "previous song"
- "volume up" / "volume down" / "mute"

### ⚡ Power Management (NEW!)
- "shutdown" / "restart" / "sleep"
- "hibernate" / "log off"

### 🎯 Gesture Integration
- "launch gesture recognition"
- "stop gesture recognition"

📚 **See [QUICK_REFERENCE.md](src/QUICK_REFERENCE.md) for complete command list**  
🆕 **See [NEW_COMMANDS.md](src/NEW_COMMANDS.md) for new commands added**

## 🎯 How It Works

```
┌─────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  Voice Assistant│────▶│ Command Handler  │◀────│ Gesture Controller│
│   (Proton.py)   │     │ (command_handler)│     │  Gesture_Controller│
└─────────────────┘     └──────────────────┘     └──────────────────┘
```

1. **Voice Input**: Speech recognition captures voice commands
2. **Command Parsing**: Fuzzy string matching interprets commands
3. **Unified Handler**: `command_handler.py` executes commands
4. **Gesture Input**: MediaPipe tracks hand gestures
5. **Same Commands**: Both use the same command functions

## 📁 Project Structure

```
gestff/
├── src/
│   ├── app.py                      # Web UI backend
│   ├── Proton.py                   # Voice assistant (modified)
│   ├── Gesture_Controller.py       # Hand gesture recognition
│   ├── command_handler.py          # Unified command system (NEW)
│   ├── USAGE_GUIDE.md              # Detailed documentation
│   ├── IMPLEMENTATION_SUMMARY.md    # Technical details
│   └── QUICK_REFERENCE.md          # Command reference
├── requirements.txt                # Dependencies
└── README.md                       # This file
```

## 🔧 Architecture

### Command Handler (`command_handler.py`)

Centralized functions for all system control:

- **Mouse Control**: `move_cursor()`, `left_click()`, `right_click()`, `scroll()`, `drag()`
- **Keyboard Commands**: `copy()`, `paste()`, `cut()`, `undo()`, `redo()`
- **System Control**: `open_app()`, `close_window()`, `take_screenshot()`
- **Internet**: `google_search()`, `youtube_search()`
- **Media**: `play_music()`, `next_song()`, `volume_up()`

### Voice Assistant (`Proton.py`)

Enhanced with unified command integration:

- Parses voice commands using fuzzy matching
- Executes commands via unified handler
- Handles wake words: "Proton", "rohan", "wake up"
- GUI and voice input support

### Gesture Controller (`Gesture_Controller.py`)

Hand gesture recognition and control:

- MediaPipe hand tracking
- Hand landmarks and gesture detection
- Gesture-to-command mapping
- Real-time camera feed

## 🎨 Gesture Mappings

| Gesture | Command |
|---------|---------|
| ✋ Palm (5 fingers up) | Move cursor |
| ✊ Fist (all closed) | Click & drag |
| ✌️ V Sign (index+middle) | Prepare to click |
| 👆 Index finger | Right click |
| 👇 Middle finger | Left click |
| 🤏 Pinch (thumb+index) | Scroll / Adjust brightness/volume |

## 💡 Key Features

### 1. Fuzzy String Matching
```python
# Understands variations:
"click" ≈ "press left button" → left_click()
"google Python" ≈ "search Python" → google_search()
```

### 2. Natural Language Processing
```python
# Parses voice commands:
"Proton, move cursor right" → move_cursor('right')
"Proton, open app notepad" → open_app('notepad')
```

### 3. Unified Commands
```python
# Same functions for both systems:
voice: "click" → left_click()
gesture: V gesture → left_click()
```

## 🔌 Extending the System

### Adding New Commands

1. Add function to `command_handler.py`:
```python
def my_command(param):
    """Execute custom command."""
    pyautogui.hotkey('ctrl', 'shift', 'm')
```

2. Update parser:
```python
elif 'custom' in command:
    return (my_command, ['param'])
```

3. Test it:
```bash
python Proton.py
# Say: "Proton, custom"
```

## 🐛 Troubleshooting

**Problem**: Voice commands not recognized
- **Solution**: Speak clearly, check microphone permissions
- Ensure wake word is used: "Proton, [command]"

**Problem**: Gestures not working
- **Solution**: Check camera permissions
- Ensure good lighting
- Keep hands visible to camera

**Problem**: Apps not opening
- **Solution**: Use exact app names
- Try: "open app calculator"

**Problem**: Search not working
- **Solution**: Check internet connection
- Try: "Proton, google test"

## 📚 Documentation

- [USAGE_GUIDE.md](src/USAGE_GUIDE.md) - Complete usage guide
- [IMPLEMENTATION_SUMMARY.md](src/IMPLEMENTATION_SUMMARY.md) - Technical details
- [QUICK_REFERENCE.md](src/QUICK_REFERENCE.md) - Command reference

## 🔮 Future Enhancements

- [ ] AI-based NLP for sophisticated command understanding
- [ ] Voice context and multi-step commands
- [ ] Custom user-defined commands
- [ ] Multi-language support
- [ ] Machine learning for intent recognition
- [ ] Voice profiles for multiple users
- [ ] Gesture-to-voice command integration
- [ ] Advanced media control (spotify, youtube specific)

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - feel free to use and modify!

## 🙏 Acknowledgments

- MediaPipe by Google for hand tracking
- pyttsx3 and SpeechRecognition for voice handling
- pyautogui for system automation

## 📞 Support

For issues or questions:
- Check the documentation in `src/` folder
- Review `USAGE_GUIDE.md` for detailed usage
- See `IMPLEMENTATION_SUMMARY.md` for technical details

## ⚡ Quick Demo

```bash
# 1. Start the system
python src/Proton.py

# 2. Wait for "I am Proton, how may I help you?"

# 3. Try these commands:
"Proton, hello"                          # Greeting
"Proton, launch gesture recognition"     # Enable gestures
"Proton, move cursor right"              # Move mouse
"Proton, click"                          # Click
"Proton, open app notepad"               # Open Notepad
"Proton, google Python"                  # Search Google
"Proton, play music"                     # Play/pause music
"Proton, take screenshot"                # Screenshot
"Proton, bye"                            # Exit

# Press ENTER in gesture window to stop gestures
```

Enjoy controlling your computer with gestures and voice! 🎉

