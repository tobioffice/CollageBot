# NBKRIST ATTENDENCE Bot

Try the bot at: [@nbkrist_attendence](https://t.me/nbkrist_attendence)

A Telegram bot built with Pyrogram to help manage college-related tasks such as student registration, attendance tracking, and general communications.

## Features

- Automated Attendance Checking System
- AI-Powered Responses using Google's Gemini Model
- Student Registration System
- Admin Notifications

## Key Functionalities

### Attendance Checking
- Check attendance status using roll number
- Real-time attendance updates

### AI Integration
- Powered by Google's Gemini AI model
- Natural language understanding
- Intelligent responses to queries
- Enhanced user interaction

## Prerequisites

- Python 3.7 or higher
- A Telegram Account
- A Telegram Bot Token (get it from [@BotFather](https://t.me/botfather))

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd CollageBot
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Setup**
   Create a `.env` file in the root directory with the following variables:
   ```env
   BOT_TOKEN=your_bot_token_here
   ADMIN_CHAT_ID=your_admin_chat_id_here
   API_ID=your_api_id_here
   API_HASH=your_api_hash_here
   ```

   To get these values:
   - `BOT_TOKEN`: Create a new bot on Telegram using [@BotFather](https://t.me/botfather)
   - `ADMIN_CHAT_ID`: Your Telegram user ID (you can get it from [@userinfobot](https://t.me/userinfobot))
   - `API_ID` and `API_HASH`: Get from [my.telegram.org](https://my.telegram.org)

4. **Database Setup**
   The bot uses SQLite for data storage. The database will be automatically created when you first run the bot.

## Running the Bot

1. Start the bot:
   ```bash
   python main.py
   ```

2. Once running, the bot will be available on Telegram with the username you set up with BotFather.

## Available Commands

- `/start` - Start the bot and get welcome message
- `/register` - Register as a student
- `/cmds` - View available commands
- (Add other commands available in your bot)

## Project Structure

```
CollageBot/
├── main.py              # Main bot file
├── requirements.txt     # Python dependencies
├── .env                # Environment variables (create this)
└── plugins/
    ├── register.py     # Registration functionality
    ├── attendence.py   # Attendance tracking
    ├── greetings.py    # Greeting messages
    └── db_connection.py # Database operations
```

## Contributing

Feel free to fork this repository and submit pull requests for any improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Created with ❤️ by [tobioffice](https://github.com/tobioffice)
