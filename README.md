# Route Bot

A Telegram bot for controlling your PC remotely — open files, launch programs, and more, all from your phone.

---

## Features

- Open any file or program by name — no need to type the full path
- Take a screenshot of your PC and get it sent straight to the chat
- Shutdown / reboot your PC remotely
- Access restricted to your Telegram account only
- Windows and Linux support

---

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/DChris19/route_bot.git
cd route_bot
```

### 2. Pick your OS

The `handlers/` folder ships with PC-control files split by platform:

- `pc_commands_windows.py`
- `pc_commands_linux.py` — **currently removed from the repo, work in progress. Linux support is temporarily unavailable until this is fixed.**

`route.py` auto-detects which file is present and imports from it — it tries the Windows file first, falls back to the Linux file if that one's missing, and only raises an error if neither is present.

| Your OS | Status |
|---|---|
| Windows | Supported — `pc_commands_windows.py` is used automatically |
| Linux | Not currently supported — `pc_commands_linux.py` was removed while a bug is being fixed |

If you're on Windows, no action needed — just keep `pc_commands_windows.py` in place. If you're on Linux, hold off until `pc_commands_linux.py` is restored in a future commit.

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create your bot
- Open Telegram and message [@BotFather](https://t.me/BotFather)
- Send `/newbot` and follow the instructions
- Copy the bot token

### 5. Get your Telegram ID
- Message [@userinfobot](https://t.me/userinfobot)
- Copy the numeric ID

### 6. Configure environment
```bash
cp .env.example .env
```
Fill in `.env`:
```
BOT_TOKEN=your_bot_token_from_botfather
MY_TELEGRAM_ID=your_telegram_id
SECOND_TELEGRAM_ID=second_person_telegram_id
```
`SECOND_TELEGRAM_ID` is optional — leave it empty or remove the line if only one person will use the bot.

### 7. Add your game/program folders

Open whichever `pc_commands_*.py` file you kept and add your folders to `SEARCH_DIRS`.

**Windows** (`pc_commands_windows.py`):
```python
SEARCH_DIRS = [
    os.path.expanduser("~\\Desktop"),
    os.path.expanduser("~\\Downloads"),
    os.path.expanduser("~\\Documents"),
    "C:\\Program Files",
    "C:\\Program Files (x86)",
    r"D:\cteam\steamapps\common",  # your Steam folder
    # add more folders here
]
```

**Linux** (`pc_commands_linux.py`):
```python
SEARCH_DIRS = [
    os.path.expanduser("~/Desktop"),
    os.path.expanduser("~/Downloads"),
    os.path.expanduser("~/Documents"),
    "/usr/share/applications",
    "/opt",
    os.path.expanduser("~/.steam/steam/steamapps/common"),  # your Steam folder
    # add more folders here
]
```

### 8. Run the bot
```bash
python main.py
```

The bot will run as long as your PC is on and the script is running.

---

## Project Structure

```
route_bot/
├── handlers/
│   ├── pc_commands_windows.py   # PC control functions — Windows only
│   ├── pc_commands_linux.py     # PC control functions — Linux only (temporarily removed, WIP)
│   └── route.py                 # Bot handlers and FSM (auto-picks whichever file above is present)
├── .env                 # Your secrets (not on GitHub)
├── .env.example         # Template for .env
├── main.py              # Entry point
└── requirements.txt     # Dependencies
```

---

## Platform Notes

- **File opening**: Windows uses `os.startfile`, Linux uses `xdg-open`.
- **Shutdown / reboot**: Windows uses the built-in `shutdown` command, no elevated rights needed by default. On Linux, `shutdown -h +0` / `shutdown -r +0` typically require root or a configured polkit rule — without that, the command will silently fail to actually power off the machine, though the bot will still report success.
- **Screenshot**: uses [Pillow](https://pypi.org/project/Pillow/)'s `ImageGrab`, which only works on X11. On Wayland sessions (default on most modern Linux distros, e.g. GNOME/KDE by default), screenshot capture will fail and the bot will report an error instead of crashing.
- **Missing both files**: if you delete (or rename) both `pc_commands_windows.py` and `pc_commands_linux.py`, the bot will fail to start and print a clear error telling you to restore one of them — it won't crash mid-conversation.
- **Linux status**: `pc_commands_linux.py` is currently removed from the repo while a bug is being fixed. Windows users are unaffected.

---

## Security

- The bot only responds to Telegram accounts with an ID matching `MY_TELEGRAM_ID` or the optional `SECOND_TELEGRAM_ID`
- Your `.env` file is excluded from Git via `.gitignore`
- Each user creates their own bot token — no shared access

---

## Requirements

- Python 3.10+
- Windows or Linux (X11 session recommended for screenshots)
- Telegram account

The screenshot feature uses [Pillow](https://pypi.org/project/Pillow/), which is included in `requirements.txt`.

---

## Author

[@DChris19](https://github.com/DChris19)