from pyrogram import Client, filters, enums
from plugins.db_connection import is_student_registered, register_student
import requests
import os
from dotenv import load_dotenv

# Initialize environment variables for bot configuration
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')


@Client.on_message(filters.command('register'))
async def register(client, message):
    """
    Handles the /register command to register new students.
    - Checks if user is already registered
    - Registers new users in the database
    - Notifies admin about new registrations
    - Sends confirmation to user
    """
    try:
        user_id = message.reply_to_message.from_user.id if message.reply_to_message else message.from_user.id
        user_name = message.from_user.first_name

        if is_student_registered(user_id):
            await message.reply_text(
                "<b>You are already registered!\n"
                "Use /cmds to see available commands</b>",
                parse_mode=enums.ParseMode.HTML
            )
            return

        register_student(user_id)
        notification_text = (
            f'<a href="tg://user?id={user_id}">{user_name}</a> '
            f'has registered to the system'
        )

        # Send notification to admin if credentials are available
        if BOT_TOKEN and ADMIN_CHAT_ID:
            try:
                response = requests.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                    json={
                        "chat_id": ADMIN_CHAT_ID,
                        "text": notification_text,
                        "parse_mode": "HTML"
                    }
                )
                if not response.ok:
                    print(f"Failed to send admin notification: {response.text}")
            except Exception as e:
                print(f"Error sending admin notification: {str(e)}")

        await message.reply_text(
            "<b>✅ Registration successful!\n"
            "Use /cmds to see available commands</b>",
            parse_mode=enums.ParseMode.HTML
        )

    except Exception as e:
        await message.reply_text(
            "<b>❌ An error occurred during registration.\n"
            "Please try again later or contact admin.</b>",
            parse_mode=enums.ParseMode.HTML
        )
        print(f"Registration error: {str(e)}")
