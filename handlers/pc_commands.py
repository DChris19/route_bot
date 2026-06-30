import os
import subprocess
from io import BytesIO

import os
import subprocess
from io import BytesIO

# Folders to search for files (add your own)

SEARCH_DIRS = [
    os.path.expanduser("~\\Desktop"),
    os.path.expanduser("~\\Downloads"),
    os.path.expanduser("~\\Documents"),
    "C:\\Program Files",
    "C:\\Program Files (x86)",
    r"D:\cteam\steamapps\common",  # like this
]


def find_file(name: str) -> str | None:
    """Search for a file by name in SEARCH_DIRS"""
    for directory in SEARCH_DIRS:
        if not os.path.exists(directory):
            continue
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower() == name.lower():
                    return os.path.join(root, file)
    return None


def open_file(name: str) -> str:
    """Open a file by name — no need to type the full path"""
    path = find_file(name)
    if path is None:
        return f"File not found: {name}"
    try:
        os.startfile(path)
        return f"Opening: {path}"
    except Exception as e:
        return f"Error: {e}"


# shutdown
def shutdown() -> str:
    """Shut down the computer in 5 seconds"""
    os.system("shutdown /s /t 5")
    return "Shutting down in 5 seconds"


def cancel_shutdown() -> str:
    """Cancel shutdown"""
    os.system("shutdown /a")
    return "Shutdown cancelled"


# reboot
def rebooting() -> str:
    """Reboot the computer in 5 seconds"""
    os.system("shutdown /r /t 5")
    return "Rebooting in 5 seconds"


def cancel_rebooting() -> str:
    """Cancel reboot"""
    os.system("shutdown /a")
    return "Reboot cancelled"


# screenshot
def take_screenshot() -> bytes | None:
    """
    Capture the primary screen and return it as PNG bytes.

    Returns None if the capture fails (e.g. Pillow missing or
    no display available), so the caller can report a clean error
    instead of crashing.
    """
    try:
        from PIL import ImageGrab
    except ImportError:
        return None

    try:
        image = ImageGrab.grab()
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        return buffer.getvalue()
    except Exception:
        return None