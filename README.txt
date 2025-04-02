📅 Telegram Habit Tracking Bot

Want to build better habits and stay consistent? This bot helps you track your daily habits, set reminders, and monitor your progress—all within Telegram!
With this bot, you can create a structured routine and develop good habits effortlessly.

✅ What does it do?

 • 📊 Helps you set and track daily, weekly, or monthly habits
 • 🔔 Sends reminders to keep you on track
 • 📈 Displays progress reports to keep you motivated
 • 🎯 Supports custom habit categories and streak tracking

🔧 Features

✅ Easy-to-use interface for adding and tracking habits
✅ Automated reminders to keep you accountable
✅ Progress visualization to monitor your streaks

📩 Want to take control of your habits and boost productivity?

Contact me on Telegram, and I’ll help you set up this bot to improve your daily routine! 🚀

# HOW TO LAUNCH A TELEGRAM BOT TO TRACK HABITS

## Content
1. Getting a token for the bot
2. Instructions for Windows
3. Instructions for Linux
4. How to use the bot

##1. GETTING A TOKEN FOR A BOT

Before you start, you need to get a token for your bot.:

1. Open Telegram and find the user @BotFather
2. Send a command /newbot
3. Follow the instructions of the BotFather:
   - Specify the bot's display name (for example, "My Habit Tracker")
- Come up with a unique username for the bot (it must end with "bot", for example, "my_habits_tracker_bot")
4. BotFather will send you a message with a token. It looks something like this: `1234567890:ABCDefGhIJKlmnOPQRstUVwxYZ`
5. Save this token - you will need it when setting up the bot.

## 2. INSTRUCTIONS FOR WINDOWS

### Step 1: Install Python 3.9

1. Download Python 3.9 from the official website: https://www.python.org/downloads/release/python-3912 /
- Scroll down and select "Windows installer (64-bit)" or "Windows installer (32-bit)" depending on your system
   - If you don't know which system you have, choose 64-bit

2. Run the downloaded file
   - **IMPORTANT**: Check the box "Add Python 3.9 to PATH" before clicking "Install Now"
- Click "Install Now"
- Wait for the installation to complete and click "Close"

### Step 2: Download and configure the bot

1. Create a folder named "HabitsBot" on your desktop

2. Save the file with the bot code to this folder with the name "bot.py "

3. Open the file "bot.py " in Notepad or another text editor

4. Find the string `API_TOKEN = 'YOUR_BOT_TOKEN_HERE'

5. Replace 'YOUR_BOT_TOKEN_HERE' with the token you received from BotFather (along with the quotes)
   - It should look something like this: `API_TOKEN = '1234567890:ABCDefGhIJKlmnOPQRstUVwxYZ'

6. Save and close the file

### Step 3: Install dependencies and launch the bot

1. Press Win+R, type "cmd" and press Enter
   - The Windows command prompt opens

2. At the command prompt, go to the folder with the bot:
``
   cd Desktop\HabitsBot
   ```

3. Install the necessary libraries:
``
   pip install aiogram==3.0.0
   ```

4. Launch the bot:
   ```
   python bot.py
   ```

5. If everything was successful, you will see messages about the launch of the bot.
   - Leave the command prompt open while you want the bot to work.
   - To stop the bot, press Ctrl+C in the command prompt

## 3. INSTRUCTIONS FOR LINUX

### Step 1: Install Python 3.9

1. Open the terminal (Ctrl+Alt+T in most distributions)

2. Update the package list:
   ```
   sudo apt update
   ```

3. Install the necessary packages to build Python:
   ```
   sudo apt install software-properties-common -y
   ```

4. Add a repository with Python 3.9:
``
   sudo add-apt-repository ppa:deadsnakes/ppa -y
   sudo apt update
   ```

5. Install Python 3.9 and pip:
``
   sudo apt install python3.9 python3.9-venv python3.9-dev python3-pip -y
   ```

### Step 2: Create a folder for the bot and configure

1. Create a folder for the bot:
   ```
   mkdir ~/HabitsBot
   cd ~/HabitsBot
   ```

2. Create a virtual environment:
   ```
   python3.9 -m venv venv
   source venv/bin/activate
   ```

3. Create a file with the bot code:
   ```
   nano bot.py
   ```

4. Paste the bot code into the editor that opens

5. Replace the string `API_TOKEN = 'YOUR_BOT_TOKEN_HERE' with your BotFather token

6. Press Ctrl+O, then Enter to save the file.

7. Press Ctrl+X to exit the editor.

### Step 3: Install dependencies and launch the bot

1. Install the necessary libraries:
``
   pip install aiogram==3.0.0
   ```

2. Launch the bot:
   ```
   python bot.py
   ```

3. If everything was successful, you will see messages about the launch of the bot
- Leave the terminal open while you want the bot to work.
   - To stop the bot, press Ctrl+C in the terminal

### Optional: Auto-start setting (optional)

If you want the bot to start automatically when the server is turned on:

1. Create a system service:
   ```
   sudo nano /etc/systemd/system/habitsbot.service
   ```

2. Insert the following text (replace USER with your username):
   ```
   [Unit]
   Description=Telegram Habits Tracker Bot
   After=network.target

   [Service]
   User=USER
   WorkingDirectory=/home/USER/HabitsBot
   ExecStart=/home/USER/HabitsBot/venv/bin/python bot.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

3. Save and close the file (Ctrl+O, Enter, Ctrl+X)

4. Turn on and start the service:
   ```
   sudo systemctl enable habitsbot.service
   sudo systemctl start habitsbot.service
   ```

5. Check the job status:
   ```
   sudo systemctl status habitsbot.service
   ```

##4. HOW TO USE A BOT

After launching the bot:

1. Open Telegram and find your bot by the name you specified when creating it.

2. Start a dialogue with the bot by sending the command `/start`

3. The bot will greet you and show you the available commands.:
   - `/add` - add a new habit
   - `/done` - mark the completion of a habit
   - `/stats` - view statistics

4. To add a habit:
- Send the command `/add`
   - Write the name of the habit (for example, "Drink 2 liters of water")
- The bot will confirm the addition of the habit

5. To mark the completion of a habit:
- Send the command `/done`
   - Select the desired habit from the list
   - The bot will confirm the fulfillment of the habit

6. To view the statistics:
   - Send the `/stats` command
   - The bot will show you how many times you have completed each habit.

Now you can track your habits every day!
