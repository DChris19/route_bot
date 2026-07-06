# Route Bot

A Telegram bot for controlling your PC remotely — open files, launch programs, and more, all from your phone.

---

## Features

- Open any file or program by name — no need to type the full path
- Take a screenshot of your PC and get it sent straight to the chat
- Shutdown / reboot your PC remotely
- Access restricted to your Telegram account only
- Windows support

---

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/DChris19/route_bot.git
cd route_bot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create your bot
- Open Telegram and message [@BotFather](https://t.me/BotFather)
- Send `/newbot` and follow the instructions
- Copy the bot token

### 4. Get your Telegram ID
- Message [@userinfobot](https://t.me/userinfobot)
- Copy the numeric ID

### 5. Configure environment
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

### 6. Add your game/program folders
Open `handlers/pc_commands.py` and add your folders to `SEARCH_DIRS`:
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

### 7. Run the bot
```bash
python main.py
```

The bot will run as long as your PC is on and the script is running.

---

## Project Structure

```
route_bot/
├── handlers/
│   ├── pc_commands.py   # PC control functions
│   └── route.py         # Bot handlers and FSM
├── .env                 # Your secrets (not on GitHub)
├── .env.example         # Template for .env
├── main.py              # Entry point
└── requirements.txt     # Dependencies
```

---

## Security

- The bot only responds to Telegram accounts with an ID matching `MY_TELEGRAM_ID` or the optional `SECOND_TELEGRAM_ID`
- Your `.env` file is excluded from Git via `.gitignore`
- Each user creates their own bot token — no shared access

---

## Requirements

- Python 3.10+
- Windows OS
- Telegram account

The screenshot feature uses [Pillow](https://pypi.org/project/Pillow/), which is included in `requirements.txt`.

---

## Author

[@DChris19](https://github.com/DChris19)
