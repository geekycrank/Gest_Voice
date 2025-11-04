"""
Central Command Handler for Gesture and Voice Control

This module provides unified functions for executing commands that can be triggered
by both gesture recognition and voice commands. It serves as a bridge between
the gesture controller and voice assistant for consistent functionality.

TODO: Integrate AI-based NLP for more sophisticated command interpretation
TODO: Add more natural language commands (e.g., "take a screenshot", "minimize window")
"""

import pyautogui
from pynput.keyboard import Key, Controller
import webbrowser
import subprocess
import os
import time
from difflib import SequenceMatcher

pyautogui.FAILSAFE = False
keyboard = Controller()


def similarity(a, b):
    """Calculate similarity ratio between two strings."""
    return SequenceMatcher(None, a, b).ratio()


def find_best_match(command, keyword_list):
    """
    Find the best matching keyword from a list using fuzzy string matching.
    
    Args:
        command: The voice command string
        keyword_list: List of keywords to match against
    
    Returns:
        The best matching keyword or None
    """
    best_match = None
    best_similarity = 0.0
    
    for keyword in keyword_list:
        sim = similarity(command.lower(), keyword.lower())
        if sim > best_similarity and sim > 0.6:  # 60% similarity threshold
            best_similarity = sim
            best_match = keyword
    
    return best_match


# ==================== MOUSE CONTROL FUNCTIONS ====================

def move_cursor(direction=None, x=None, y=None):
    """
    Move the mouse cursor.
    
    Args:
        direction: String direction ('up', 'down', 'left', 'right') - optional
        x: X coordinate - optional
        y: Y coordinate - optional
    """
    current_x, current_y = pyautogui.position()
    step = 50  # pixels to move
    
    if x is not None and y is not None:
        pyautogui.moveTo(x, y, duration=0.1)
    elif direction:
        direction = direction.lower()
        if 'up' in direction:
            pyautogui.moveRel(0, -step, duration=0.1)
        elif 'down' in direction:
            pyautogui.moveRel(0, step, duration=0.1)
        elif 'left' in direction:
            pyautogui.moveRel(-step, 0, duration=0.1)
        elif 'right' in direction:
            pyautogui.moveRel(step, 0, duration=0.1)


def left_click():
    """Perform a left mouse click."""
    pyautogui.click()


def right_click():
    """Perform a right mouse click."""
    pyautogui.click(button='right')


def double_click():
    """Perform a double left click."""
    pyautogui.doubleClick()


def middle_click():
    """Perform a middle mouse click."""
    pyautogui.click(button='middle')


def mouse_down(button='left'):
    """
    Press and hold mouse button.
    
    Args:
        button: 'left', 'right', or 'middle'
    """
    pyautogui.mouseDown(button=button)


def mouse_up(button='left'):
    """
    Release mouse button.
    
    Args:
        button: 'left', 'right', or 'middle'
    """
    pyautogui.mouseUp(button=button)


def drag(start_x, start_y, end_x, end_y):
    """
    Drag mouse from start to end position.
    
    Args:
        start_x: Starting X coordinate
        start_y: Starting Y coordinate
        end_x: Ending X coordinate
        end_y: Ending Y coordinate
    """
    pyautogui.moveTo(start_x, start_y)
    pyautogui.dragTo(end_x, end_y, duration=0.5)


def scroll(direction='down', amount=3):
    """
    Scroll the mouse wheel.
    
    Args:
        direction: 'up' or 'down'
        amount: Number of scroll units
    """
    if direction.lower() in ['up', 'down']:
        scroll_amount = amount if direction.lower() == 'down' else -amount
        pyautogui.scroll(scroll_amount)
    elif direction.lower() in ['left', 'right']:
        # Horizontal scroll
        pyautogui.keyDown('shift')
        scroll_amount = -amount if direction.lower() == 'right' else amount
        pyautogui.scroll(scroll_amount)
        pyautogui.keyUp('shift')


# ==================== KEYBOARD FUNCTIONS ====================

def press_key(key):
    """Press and release a key."""
    pyautogui.press(key)


def key_combination(*keys):
    """
    Press a combination of keys simultaneously.
    
    Args:
        *keys: Variable number of keys
    """
    pyautogui.hotkey(*keys)


def type_text(text):
    """Type text using keyboard."""
    pyautogui.typewrite(text)


def copy():
    """Copy selected text."""
    pyautogui.hotkey('ctrl', 'c')


def paste():
    """Paste clipboard content."""
    pyautogui.hotkey('ctrl', 'v')


def cut():
    """Cut selected text."""
    pyautogui.hotkey('ctrl', 'x')


def undo():
    """Undo last action."""
    pyautogui.hotkey('ctrl', 'z')


def redo():
    """Redo last action."""
    pyautogui.hotkey('ctrl', 'y')


def select_all():
    """Select all."""
    pyautogui.hotkey('ctrl', 'a')


# ==================== SYSTEM CONTROL FUNCTIONS ====================

def open_app(app_name):
    """
    Open an application.
    
    Args:
        app_name: Name of the application to open
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Common Windows apps
        app_map = {
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'paint': 'mspaint.exe',
            'chrome': 'chrome.exe',
            'firefox': 'firefox.exe',
            'explorer': 'explorer.exe',
            'cmd': 'cmd.exe',
            'command prompt': 'cmd.exe',
            'vs code': 'code',
            'visual studio code': 'code',
            'steam': 'steam.exe',
            'spotify': 'spotify.exe',
            'music': 'spotify.exe',
        }
        
        app_name_lower = app_name.lower()
        if app_name_lower in app_map:
            subprocess.Popen(app_map[app_name_lower])
            return True
        else:
            # Try to open with the name directly
            subprocess.Popen(app_name)
            return True
    except Exception as e:
        print(f"Error opening app: {e}")
        return False


def close_current_window():
    """Close current active window."""
    pyautogui.hotkey('alt', 'f4')


def minimize_window():
    """Minimize current window."""
    pyautogui.hotkey('win', 'down')


def maximize_window():
    """Maximize current window."""
    pyautogui.hotkey('win', 'up')


def switch_window():
    """Switch to next window."""
    pyautogui.hotkey('alt', 'tab')


# ==================== INTERNET FUNCTIONS ====================

def google_search(query):
    """
    Perform a Google search.
    
    Args:
        query: Search query string
    """
    url = 'https://www.google.com/search?q=' + '+'.join(query.split())
    webbrowser.get().open(url)


def youtube_search(query):
    """
    Perform a YouTube search.
    
    Args:
        query: Search query string
    """
    url = 'https://www.youtube.com/results?search_query=' + '+'.join(query.split())
    webbrowser.get().open(url)


def open_website(url):
    """
    Open a website.
    
    Args:
        url: Website URL
    """
    if not url.startswith('http'):
        url = 'https://' + url
    webbrowser.get().open(url)


# ==================== MUSIC CONTROL FUNCTIONS ====================

def play_music():
    """Play/pause music in currently playing app."""
    pyautogui.press('space')


def next_song():
    """Skip to next song."""
    pyautogui.press('media_next')


def previous_song():
    """Go to previous song."""
    pyautogui.press('media_previous')


def volume_up():
    """Increase volume."""
    pyautogui.press('volumeup')


def volume_down():
    """Decrease volume."""
    pyautogui.press('volumedown')


def mute():
    """Mute/unmute volume."""
    pyautogui.press('volumemute')


# ==================== UTILITY FUNCTIONS ====================

def take_screenshot():
    """Take a screenshot."""
    screenshot = pyautogui.screenshot()
    screenshot.save('screenshot_' + str(time.time()) + '.png')
    return 'screenshot_' + str(time.time()) + '.png'


def get_time():
    """Get current time."""
    import datetime
    return datetime.datetime.now().strftime("%H:%M:%S")


def get_date():
    """Get current date."""
    import datetime
    return datetime.datetime.now().strftime("%B %d, %Y")


# ==================== BROWSER CONTROL FUNCTIONS ====================

def browser_back():
    """Go back in browser history."""
    pyautogui.hotkey('alt', 'left')


def browser_forward():
    """Go forward in browser history."""
    pyautogui.hotkey('alt', 'right')


def browser_refresh():
    """Refresh current page."""
    pyautogui.hotkey('ctrl', 'r')


def browser_new_tab():
    """Open new tab in browser."""
    pyautogui.hotkey('ctrl', 't')


def browser_close_tab():
    """Close current tab in browser."""
    pyautogui.hotkey('ctrl', 'w')


def browser_next_tab():
    """Switch to next tab."""
    pyautogui.hotkey('ctrl', 'tab')


def browser_previous_tab():
    """Switch to previous tab."""
    pyautogui.hotkey('ctrl', 'shift', 'tab')


def browser_home():
    """Go to browser home page."""
    pyautogui.hotkey('alt', 'home')


def browser_search_bar():
    """Focus on browser search bar."""
    pyautogui.hotkey('ctrl', 'l')


# ==================== FILE OPERATION FUNCTIONS ====================

def save_file():
    """Save current file."""
    pyautogui.hotkey('ctrl', 's')


def open_file():
    """Open file dialog."""
    pyautogui.hotkey('ctrl', 'o')


def new_file():
    """Create new file."""
    pyautogui.hotkey('ctrl', 'n')


def print_file():
    """Print current file."""
    pyautogui.hotkey('ctrl', 'p')


# ==================== TEXT FORMATTING FUNCTIONS ====================

def bold_text():
    """Make text bold."""
    pyautogui.hotkey('ctrl', 'b')


def italic_text():
    """Make text italic."""
    pyautogui.hotkey('ctrl', 'i')


def underline_text():
    """Underline text."""
    pyautogui.hotkey('ctrl', 'u')


def strikethrough_text():
    """Strikethrough text."""
    pyautogui.hotkey('ctrl', 'shift', 'x')


# ==================== WINDOW MANAGEMENT FUNCTIONS ====================

def snap_window_left():
    """Snap window to left half of screen."""
    pyautogui.hotkey('win', 'left')


def snap_window_right():
    """Snap window to right half of screen."""
    pyautogui.hotkey('win', 'right')


def center_window():
    """Center window on screen."""
    pyautogui.hotkey('win', 'up')


def task_view():
    """Open Windows Task View."""
    pyautogui.hotkey('win', 'tab')


def show_desktop():
    """Show desktop (minimize all windows)."""
    pyautogui.hotkey('win', 'd')


def lock_screen():
    """Lock the screen."""
    pyautogui.hotkey('win', 'l')


def screenshot_region():
    """Take screenshot of selected region."""
    pyautogui.hotkey('win', 'shift', 's')


# ==================== VIRTUAL DESKTOP FUNCTIONS ====================

def new_desktop():
    """Create new virtual desktop."""
    pyautogui.hotkey('win', 'ctrl', 'd')


def close_desktop():
    """Close current virtual desktop."""
    pyautogui.hotkey('win', 'ctrl', 'f4')


def switch_desktop_right():
    """Switch to right virtual desktop."""
    pyautogui.hotkey('win', 'ctrl', 'right')


def switch_desktop_left():
    """Switch to left virtual desktop."""
    pyautogui.hotkey('win', 'ctrl', 'left')


# ==================== SEARCH & QUICK ACCESS FUNCTIONS ====================

def open_start_menu():
    """Open Windows Start menu."""
    pyautogui.press('win')


def open_search():
    """Open Windows Search."""
    pyautogui.hotkey('win', 's')


def open_run():
    """Open Run dialog."""
    pyautogui.hotkey('win', 'r')


def open_settings():
    """Open Windows Settings."""
    pyautogui.hotkey('win', 'i')


def open_task_manager():
    """Open Task Manager."""
    pyautogui.hotkey('ctrl', 'shift', 'esc')


def open_action_center():
    """Open Windows Action Center."""
    pyautogui.hotkey('win', 'a')


def open_notifications():
    """Open notification panel."""
    pyautogui.hotkey('win', 'n')


# ==================== TEXT EDITING ADVANCED FUNCTIONS ====================

def find_text():
    """Open find dialog."""
    pyautogui.hotkey('ctrl', 'f')


def find_replace():
    """Open find and replace dialog."""
    pyautogui.hotkey('ctrl', 'h')


def save_as():
    """Save file with new name."""
    pyautogui.hotkey('ctrl', 'shift', 's')


# ==================== EMAIL FUNCTIONS ====================

def new_email():
    """Compose new email (works in most email clients)."""
    pyautogui.hotkey('ctrl', 'n')


def send_email():
    """Send email (works in most email clients)."""
    pyautogui.hotkey('ctrl', 'enter')


def reply_email():
    """Reply to email."""
    pyautogui.press('r')


def reply_all():
    """Reply all to email."""
    pyautogui.press('shift', 'r')


def forward_email():
    """Forward email."""
    pyautogui.press('f')


# ==================== POWER FUNCTIONS ====================

def shutdown():
    """Shutdown the computer."""
    os.system('shutdown /s /t 0')


def restart():
    """Restart the computer."""
    os.system('shutdown /r /t 0')


def sleep():
    """Put computer to sleep."""
    os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')


def hibernate():
    """Hibernate the computer."""
    os.system('shutdown /h')


def logoff():
    """Log off current user."""
    os.system('shutdown /l')


# ==================== VOICE COMMAND PARSER ====================

def parse_voice_command(command):
    """
    Parse voice command and determine the appropriate action.
    
    Args:
        command: The voice command string
    
    Returns:
        Tuple of (action_function, args) or None if no match
    """
    command_lower = command.lower()
    
    # Mouse movement commands
    if any(word in command_lower for word in ['move', 'cursor', 'pointer', 'mouse']):
        if 'up' in command_lower:
            return (move_cursor, ['up'])
        elif 'down' in command_lower:
            return (move_cursor, ['down'])
        elif 'left' in command_lower:
            return (move_cursor, ['left'])
        elif 'right' in command_lower:
            return (move_cursor, ['right'])
    
    # Click commands
    elif any(word in command_lower for word in ['click', 'press']):
        if any(word in command_lower for word in ['left', 'single']):
            return (left_click, [])
        elif any(word in command_lower for word in ['right', 'context']):
            return (right_click, [])
        elif 'double' in command_lower or 'two' in command_lower:
            return (double_click, [])
        elif 'middle' in command_lower:
            return (middle_click, [])
        else:
            return (left_click, [])  # default to left click
    
    # Scroll commands
    elif any(word in command_lower for word in ['scroll', 'wheel']):
        direction = 'down'
        if 'up' in command_lower:
            direction = 'up'
        elif 'left' in command_lower:
            direction = 'left'
        elif 'right' in command_lower:
            direction = 'right'
        return (scroll, [direction])
    
    # Keyboard commands
    elif 'copy' in command_lower:
        return (copy, [])
    elif any(word in command_lower for word in ['paste', 'page']):
        return (paste, [])
    elif 'cut' in command_lower:
        return (cut, [])
    elif 'undo' in command_lower:
        return (undo, [])
    elif 'redo' in command_lower:
        return (redo, [])
    
    # System commands
    elif 'open' in command_lower and 'app' in command_lower:
        # Extract app name from command
        parts = command_lower.split()
        try:
            app_idx = parts.index('app') + 1
            if app_idx < len(parts):
                app_name = ' '.join(parts[app_idx:])
                return (open_app, [app_name])
        except ValueError:
            pass
    
    elif any(word in command_lower for word in ['google', 'search']):
        # Extract search query
        query = command_lower.replace('google', '').replace('search', '').strip()
        return (google_search, [query])
    
    elif 'play music' in command_lower or 'pause music' in command_lower:
        return (play_music, [])
    elif any(word in command_lower for word in ['next song', 'skip']):
        return (next_song, [])
    elif 'previous song' in command_lower or 'back song' in command_lower:
        return (previous_song, [])
    
    elif 'volume up' in command_lower or 'increase volume' in command_lower:
        return (volume_up, [])
    elif 'volume down' in command_lower or 'decrease volume' in command_lower:
        return (volume_down, [])
    elif 'mute' in command_lower:
        return (mute, [])
    
    elif 'screenshot' in command_lower or 'take screenshot' in command_lower:
        return (take_screenshot, [])
    
    elif 'close window' in command_lower or 'close active window' in command_lower:
        return (close_current_window, [])
    elif 'minimize' in command_lower:
        return (minimize_window, [])
    elif 'maximize' in command_lower:
        return (maximize_window, [])
    elif 'switch window' in command_lower or 'alt tab' in command_lower:
        return (switch_window, [])
    
    # Browser control commands
    elif any(word in command_lower for word in ['go back', 'back page', 'previous page']):
        return (browser_back, [])
    elif any(word in command_lower for word in ['go forward', 'forward page', 'next page']):
        return (browser_forward, [])
    elif any(word in command_lower for word in ['refresh', 'reload']):
        return (browser_refresh, [])
    elif 'new tab' in command_lower or 'open tab' in command_lower:
        return (browser_new_tab, [])
    elif any(word in command_lower for word in ['close tab', 'shut tab']):
        return (browser_close_tab, [])
    elif 'next tab' in command_lower:
        return (browser_next_tab, [])
    elif 'previous tab' in command_lower or 'last tab' in command_lower:
        return (browser_previous_tab, [])
    elif 'home page' in command_lower or 'go home' in command_lower:
        return (browser_home, [])
    elif 'search bar' in command_lower or 'address bar' in command_lower:
        return (browser_search_bar, [])
    
    # File operation commands
    elif 'save' in command_lower and 'as' not in command_lower:
        return (save_file, [])
    elif 'save as' in command_lower:
        return (save_as, [])
    elif 'open file' in command_lower:
        return (open_file, [])
    elif 'new file' in command_lower or 'create file' in command_lower:
        return (new_file, [])
    elif 'print' in command_lower:
        return (print_file, [])
    
    # Text formatting commands
    elif any(word in command_lower for word in ['bold', 'bold text']):
        return (bold_text, [])
    elif any(word in command_lower for word in ['italic', 'italic text']):
        return (italic_text, [])
    elif any(word in command_lower for word in ['underline', 'underlined']):
        return (underline_text, [])
    elif 'strikethrough' in command_lower or 'strike through' in command_lower:
        return (strikethrough_text, [])
    
    # Window management commands
    elif any(word in command_lower for word in ['snap left', 'window left', 'move left']):
        return (snap_window_left, [])
    elif any(word in command_lower for word in ['snap right', 'window right', 'move right']):
        return (snap_window_right, [])
    elif 'center window' in command_lower or 'center' in command_lower:
        return (center_window, [])
    elif 'task view' in command_lower or 'task manager view' in command_lower:
        return (task_view, [])
    elif any(word in command_lower for word in ['show desktop', 'desktop', 'hide windows']):
        return (show_desktop, [])
    elif any(word in command_lower for word in ['lock screen', 'lock', 'lock computer']):
        return (lock_screen, [])
    elif 'screenshot region' in command_lower or 'snip' in command_lower:
        return (screenshot_region, [])
    
    # Virtual desktop commands
    elif 'new desktop' in command_lower or 'create desktop' in command_lower:
        return (new_desktop, [])
    elif 'close desktop' in command_lower:
        return (close_desktop, [])
    elif 'switch desktop right' in command_lower or 'desktop right' in command_lower:
        return (switch_desktop_right, [])
    elif 'switch desktop left' in command_lower or 'desktop left' in command_lower:
        return (switch_desktop_left, [])
    
    # Windows system commands
    elif 'start menu' in command_lower or 'windows key' in command_lower:
        return (open_start_menu, [])
    elif 'windows search' in command_lower or 'search windows' in command_lower:
        return (open_search, [])
    elif 'run dialog' in command_lower or 'open run' in command_lower:
        return (open_run, [])
    elif any(word in command_lower for word in ['settings', 'windows settings']):
        return (open_settings, [])
    elif any(word in command_lower for word in ['task manager', 'open task manager']):
        return (open_task_manager, [])
    elif 'action center' in command_lower:
        return (open_action_center, [])
    elif 'notifications' in command_lower or 'notification' in command_lower:
        return (open_notifications, [])
    
    # Text editing advanced commands
    elif any(word in command_lower for word in ['find', 'find text']):
        return (find_text, [])
    elif any(word in command_lower for word in ['replace', 'find and replace']):
        return (find_replace, [])
    
    # Email commands
    elif any(word in command_lower for word in ['new email', 'compose email', 'compose']):
        return (new_email, [])
    elif 'send email' in command_lower or 'send message' in command_lower:
        return (send_email, [])
    elif 'reply' in command_lower and 'all' not in command_lower:
        return (reply_email, [])
    elif 'reply all' in command_lower:
        return (reply_all, [])
    elif 'forward' in command_lower and 'email' not in command_lower:
        return (forward_email, [])
    
    # Power management commands
    elif any(word in command_lower for word in ['shutdown', 'shut down', 'turn off computer']):
        return (shutdown, [])
    elif any(word in command_lower for word in ['restart', 'reboot', 'restart computer']):
        return (restart, [])
    elif any(word in command_lower for word in ['sleep', 'computer sleep', 'put to sleep']):
        return (sleep, [])
    elif any(word in command_lower for word in ['hibernate', 'hibernate computer']):
        return (hibernate, [])
    elif any(word in command_lower for word in ['log off', 'logoff', 'sign out']):
        return (logoff, [])
    
    return None

