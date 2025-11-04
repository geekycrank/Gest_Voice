# Quick Reference: Voice Commands

## 🎤 How to Use

1. Run the voice assistant: `python Proton.py`
2. Wait for "I am Proton, how may I help you?"
3. Say wake word + command: **"Proton, [command]"**

## 📋 Common Commands

### Mouse Control
- **"Proton, move cursor [up/down/left/right]"**
- **"Proton, click"** - Left click
- **"Proton, right click"** - Right click
- **"Proton, double click"** - Double click
- **"Proton, scroll [up/down/left/right]"**

### Keyboard Shortcuts
- **"Proton, copy"**
- **"Proton, paste"**
- **"Proton, cut"**
- **"Proton, undo"**
- **"Proton, redo"**
- **"Proton, select all"**

### Browser Control
- **"Proton, go back"** / **"previous page"**
- **"Proton, go forward"** / **"next page"**
- **"Proton, refresh"** / **"reload"**
- **"Proton, new tab"**
- **"Proton, close tab"**
- **"Proton, next tab"**
- **"Proton, previous tab"**
- **"Proton, home page"**
- **"Proton, search bar"** - Focus address bar

### File Operations
- **"Proton, save"**
- **"Proton, save as"**
- **"Proton, open file"**
- **"Proton, new file"**
- **"Proton, print"**

### Text Formatting
- **"Proton, bold"**
- **"Proton, italic"**
- **"Proton, underline"**
- **"Proton, strikethrough"**
- **"Proton, find"** - Open find dialog
- **"Proton, replace"** - Find and replace

### Window Management
- **"Proton, snap left"** - Snap window left
- **"Proton, snap right"** - Snap window right
- **"Proton, center window"**
- **"Proton, minimize"**
- **"Proton, maximize"**
- **"Proton, close window"**
- **"Proton, show desktop"**
- **"Proton, task view"**
- **"Proton, switch window"** - Alt+Tab

### Virtual Desktops
- **"Proton, new desktop"**
- **"Proton, close desktop"**
- **"Proton, switch desktop right"**
- **"Proton, switch desktop left"**

### Windows System
- **"Proton, start menu"**
- **"Proton, windows search"**
- **"Proton, settings"** - Open Windows Settings
- **"Proton, task manager"**
- **"Proton, action center"**
- **"Proton, notifications"**
- **"Proton, lock screen"**

### Applications
- **"Proton, open app notepad"**
- **"Proton, open app calculator"**
- **"Proton, open app chrome"**
- **"Proton, open app spotify"**

### Internet
- **"Proton, google [query]"**
- **"Proton, search [query]"**

### Media Control
- **"Proton, play music"** / **"pause music"**
- **"Proton, next song"**
- **"Proton, previous song"**
- **"Proton, volume up"** / **"volume down"**
- **"Proton, mute"**

### Email (in email clients)
- **"Proton, new email"** / **"compose"**
- **"Proton, send email"**
- **"Proton, reply"**
- **"Proton, reply all"**
- **"Proton, forward"**

### Screenshots
- **"Proton, screenshot"**
- **"Proton, screenshot region"** / **"snip"**

### Time & Date
- **"Proton, what time is it"** / **"tell me the time"**
- **"Proton, what's the date"**

### Gesture Control
- **"Proton, launch gesture recognition"**
- **"Proton, start gesture"**
- **"Proton, stop gesture recognition"**

### Power Management
- **"Proton, shutdown"**
- **"Proton, restart"**
- **"Proton, sleep"**
- **"Proton, hibernate"**
- **"Proton, log off"**

### Navigation
- **"Proton, hello"** - Greeting
- **"Proton, wake up"** - Wake assistant
- **"Proton, bye"** - Put assistant to sleep
- **"Proton, exit"** - Close application

## 💡 Tips

- Wake words: **"Proton"**, **"rohan"**, or **"wake up"**
- Be clear and natural
- Commands work without wake word in GUI mode
- Commands are case-insensitive
- System uses fuzzy matching - "click" ≈ "press button"

## 🚀 Example Conversation

```
You: "Proton, hello"
AI: "Good morning! I am Proton, how may I help you?"

You: "Proton, open app chrome"
AI: "Command executed successfully"

You: "Proton, new tab"
AI: "Command executed successfully"

You: "Proton, search Python programming"
AI: "Searching for Python programming"
AI: "This is what I found"

You: "Proton, go back"
AI: "Command executed successfully"

You: "Proton, refresh"
AI: "Command executed successfully"

You: "Proton, show desktop"
AI: "Command executed successfully"

You: "Proton, snap left"
AI: "Command executed successfully"

You: "Proton, new desktop"
AI: "Command executed successfully"

You: "Proton, take screenshot"
AI: "Command executed successfully"

You: "Proton, save"
AI: "Command executed successfully"

You: "Proton, lock screen"
AI: "Command executed successfully"

You: "Proton, launch gesture recognition"
AI: "Launched Successfully"

You: "Proton, what time is it"
AI: "14:30:25"

You: "Proton, volume up"
AI: "Command executed successfully"

You: "Proton, play music"
AI: "Command executed successfully"

You: "Proton, bye"
AI: "Good bye! Have a nice day."
```

## ⚙️ Troubleshooting

**Command not recognized?**
- Try speaking clearer
- Check if wake word was detected
- Use natural language variations

**App won't open?**
- Ensure app name is correct
- Try full app name: "calculator" → "calc.exe"

**No response?**
- Check microphone permissions
- Ensure internet connection (for speech recognition)
- Try saying "wake up"

## 📝 Adding Custom Commands

Edit `command_handler.py`:

```python
# Add function
def my_custom_command():
    # your code here
    pass

# Add to parser
def parse_voice_command(command):
    # ... existing code ...
    elif 'custom' in command:
        return (my_custom_command, [])
```

## 🎯 Architecture

```
Voice Input → Proton.py → Command Handler → Execute Command
Gesture Input → Gesture Controller → Execute Command
```

Both use the same **Command Handler** for consistency!

