import eel
import os
from queue import Queue
import sys


class ChatBot:
    started = False
    userinputQueue = Queue()

    # ---- Queue Handling ----
    @staticmethod
    def isUserInput():
        """Check if there is any new user input."""
        return not ChatBot.userinputQueue.empty()

    @staticmethod
    def popUserInput():
        """Get the next message from the user input queue."""
        return ChatBot.userinputQueue.get()

    # ---- Eel Bridge ----
    @staticmethod
    def close_callback(route, websockets):
        """Handle window close event."""
        print("UI closed by user.")
        ChatBot.started = False
        sys.exit(0)

    @staticmethod
    @eel.expose
    def getUserInput(msg):
        """Receive user input from the frontend."""
        ChatBot.userinputQueue.put(msg)
        print(f"User: {msg}")

    @staticmethod
    def close():
        """Stop chatbot and close the eel window."""
        ChatBot.started = False
        try:
            eel.close()
        except:
            pass

    @staticmethod
    def addUserMsg(msg):
        """Send a user message to the frontend."""
        try:
            eel.addUserMsg(msg)
        except Exception as e:
            print(f"[UI] Failed to add user message: {e}")

    @staticmethod
    def addAppMsg(msg):
        """Send a chatbot message to the frontend."""
        try:
            eel.addAppMsg(msg)
        except Exception as e:
            print(f"[UI] Failed to add bot message: {e}")

    # ---- UI Initialization ----
    @staticmethod
    def start():
        """Initialize the chatbot web interface."""
        path = os.path.dirname(os.path.abspath(__file__))
        web_dir = os.path.join(path, "web")

        if not os.path.exists(web_dir):
            print(f"[Warning] Web directory not found at: {web_dir}")
            print("Creating a simple fallback interface...")
            os.makedirs(web_dir, exist_ok=True)
            with open(os.path.join(web_dir, "index.html"), "w") as f:
                f.write("<html><body><h2>Proton ChatBot</h2><p>Minimal UI loaded.</p></body></html>")

        eel.init(web_dir, allowed_extensions=['.js', '.html'])

        try:
            eel.start(
                "index.html",
                mode="chrome",  # Can change to "default" if Chrome is not detected
                host="localhost",
                port=27005,
                block=False,
                size=(350, 480),
                position=(10, 100),
                disable_cache=True,
                close_callback=ChatBot.close_callback,
            )

            ChatBot.started = True
            print("✅ ChatBot UI started successfully")

            # Keep eel running while the main thread works
            while ChatBot.started:
                eel.sleep(1.0)

        except Exception as e:
            print(f"[Error] Failed to start Eel UI: {e}")
            ChatBot.started = True  # allow main.py to continue
