# Voice Assistant - Unified Command System

## Overview

The voice assistant now supports both **gesture-based commands** and **natural language commands** through a unified command handler system. This allows users to control their system entirely by voice, gestures, or a combination of both.

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  Voice Assistant│────▶│ Command Handler  │◀────│ Gesture Controller│
│   (Proton.py)   │     │ (command_handler)│     │  Gesture_Controller│
└─────────────────┘     └──────────────────┘     └──────────────────┘
```

### Key Components

1. **`command_handler.py`**: Centralized functions for all commands (mouse, keyboard, system, internet)
2. **`Proton.py`**: Voice assistant that parses voice commands and executes them
3. **`Gesture_Controller.py`**: Hand gesture recognition system (existing)

## Supported Voice Commands

### Mouse Control Commands

- "move cursor up/down/left/right"
- "click" or "press left button"
- "right click" or "context click"
- "double click"
- "scroll up/down/left/right"
- "drag"

### Keyboard Commands

- "copy"
- "paste"
- "cut"
- "undo"
- "redo"
- "select all"

### System Commands

- "open app notepad"
- "open app calculator"
- "open app chrome"
- "close window"
- "minimize"
- "maximize"
- "switch window" or "alt tab"
- "take screenshot"

### Internet Commands

- "google [query]" or "search [query]"
- "youtube [query]"

### Music/Media Control

- "play music" or "pause music"
- "next song"
- "previous song"
- "volume up"
- "volume down"
- "mute"

### Time and Date

- "what time is it"
- "what's the date"
- "tell me the time"

### Gesture Control Integration

- "launch gesture recognition"
- "start gesture"
- "stop gesture recognition"

## Usage Examples

### Basic Mouse Control

```
User: "Proton, move cursor left"
AI: "Command executed successfully"

User: "Proton, click"
AI: "Command executed successfully"

User: "Proton, scroll down"
AI: "Command executed successfully"
```

### Application Control

```
User: "Proton, open app notepad"
AI: "Command executed successfully"

User: "Proton, open app calculator"
AI: "Command executed successfully"
```

### Internet Search

```
User: "Proton, google Python programming"
AI: "Searching for Python programming"
AI: "This is what I found"

User: "Proton, search machine learning"
AI: "Searching for machine learning"
```

### Media Control

```
User: "Proton, play music"
AI: "Command executed successfully"

User: "Proton, next song"
AI: "Command executed successfully"

User: "Proton, volume up"
AI: "Command executed successfully"
```

## Fuzzy String Matching

The system uses fuzzy string matching to understand similar phrases:

- "click" or "press left button" → left click
- "copy" or "cp" → copy command
- "paste" or "page" → paste command
- "press" or "click" → click action

Similarity threshold: 60% match required

## Future Enhancements (TODOs)

1. **AI-Based NLP**: Implement advanced natural language processing for more sophisticated command understanding
2. **Voice Context**: Maintain conversation context for multi-step commands
3. **Custom Commands**: Allow users to define custom voice commands
4. **Gesture Integration**: Enable voice to trigger specific gestures
5. **Multi-language Support**: Support for multiple languages
6. **Machine Learning**: Implement ML-based intent recognition

## Adding New Commands

To add a new command:

1. Add the function to `command_handler.py`:

```python
def new_command(param):
    """Execute new command."""
    # Implementation here
    pass
```

2. Update `parse_voice_command()` in `command_handler.py`:

```python
def parse_voice_command(command):
    command_lower = command.lower()
    
    # Add your parsing logic
    elif 'new command' in command_lower:
        return (new_command, [param])
```

3. Test with voice assistant:

```
User: "Proton, new command"
AI: "Command executed successfully"
```

## Integration with Gesture Controller

The gesture controller can also use commands from `command_handler.py` for consistency. Example:

```python
# In Gesture_Controller.py
import command_handler as cmd

# Replace direct pyautogui call with:
cmd.left_click()
cmd.move_cursor('right', 50)
```

## Error Handling

All commands are wrapped in try-except blocks to handle errors gracefully:

```python
try:
    result = func(*args)
    reply('Command executed successfully')
except Exception as e:
    print(f"Error executing command: {e}")
    reply('Sorry, I could not execute that command')
```

## Key Features

✅ **Unified Command Interface**: Single source of truth for all commands
✅ **Fuzzy Matching**: Understands variations in voice commands
✅ **Extensible**: Easy to add new commands
✅ **Consistent**: Same functions used by gesture and voice systems
✅ **Robust Error Handling**: Graceful failure with informative messages
✅ **Natural Language**: Support for conversational commands

## Testing

Run the voice assistant:

```bash
python Proton.py
```

Test gestures separately:

```bash
python Gesture_Controller.py
```

## Notes

- Wake word is "Proton" (from original "rohan")
- Commands are case-insensitive
- Use clear, natural language
- Some commands may require specific applications to be open


