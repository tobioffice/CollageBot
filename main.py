import asyncio
from pyrogram import Client, compose, filters, enums
import google.generativeai as genai
import requests
from pyrogram.types import ChatMember
from dotenv import load_dotenv
from plugins.db_connection import is_student_registered
import os
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Get environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
ADMIN_ID = int(os.getenv('ADMIN_ID'))
GEMINI_API = os.getenv('GEMINI_API')


private_access = [ADMIN_ID]
print(f"Private access: {private_access}")


async def main() -> None:
    bot: Client = Client("my_bot",
                         api_id=API_ID,
                         api_hash=API_HASH,
                         bot_token=BOT_TOKEN,
                         plugins=dict(root="plugins"))
    clients = [bot]
    bot.set_parse_mode(enums.ParseMode.HTML)

    @bot.on_message(filters.command('adm_test') & filters.user(ADMIN_ID))
    async def cmd_admin_test(client: Client, message: str) -> None:
        try:
            await message.reply_text("Admin test successful. Bot is working correctly.", quote=True)
        except Exception as e:
            await message.reply_text(f"An error occurred: {str(e)}", quote=True)

    @bot.on_message(filters.command('start'))
    async def start_cmd(client: Client, message: str) -> None:
        welcome_message = (
            "<b>🤖 Welcome to the Attendance Tracking Bot!</b>\n\n"
            "<pre>📚 This bot provides real-time tracking of student attendance for 2ND Year students.</pre>\n\n"
            "<b>📌 How to use:</b>\n"
            "   • Type <code>/att</code> followed by your roll number\n"
            "   • Example: <code>/att 23KB1A0XXX</code>\n\n"
            "<i>💡 Tip: Use /cmds to see all available commands.</i>"
        )
        await message.reply_text(welcome_message, quote=True)

    chat_history = {}
    time_limit = 60 * 60 * 3  # 3 hours

    @bot.on_message(filters.command('ai'))
    async def gen_ai(client: Client, message: str) -> None:
        if is_student_registered(message.from_user.id) or message.sender_chat:
            try:
                # Ensure prompt is concise
                msg: str = message.text[len('/ai '):].strip()
                genai.configure(api_key=GEMINI_API)

                model: genai.GenerativeModel = genai.GenerativeModel(
                    'gemini-pro')
                chat = model.start_chat(history=chat_history.get(
                    message.from_user.id, {}).get('history', []))

                # Send message and stream response
                response_stream = chat.send_message(msg, stream=True)

                if message.from_user.id not in chat_history:
                    chat_history[message.from_user.id] = {
                        'time': datetime.now(),
                        'history': []
                    }
                chat_history[message.from_user.id]['history'].append(
                    {"role": "user", "parts": [msg]})

                # Simulate streaming using message edits
                sent_message = await message.reply_text("Generating response...", message.id, parse_mode=enums.ParseMode.MARKDOWN)
                response_text = ""
                for chunk in response_stream:
                    response_text += chunk.text
                    await sent_message.edit_text(response_text, parse_mode=enums.ParseMode.MARKDOWN)

                chat_history[message.from_user.id]['history'].append(
                    {"role": "model", "parts": [response_text]})

                # Limit history length
                if len(chat_history[message.from_user.id]['history']) > 10:
                    chat_history[message.from_user.id]['history'] = chat_history[message.from_user.id]['history'][-10:]

                # Clean up old history
                for user_id, chat_data in list(chat_history.items()):
                    if (datetime.now() - chat_data['time']).total_seconds() > time_limit:
                        del chat_history[user_id]

            except Exception as e:
                print(f"Error: {str(e)}")  # Log error
                await message.reply_text(f"<b>An error occurred:</b> {str(e)}\n<b>FORMAT:</b> <code>/ai write a c program</code>", parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)
        else:
            await message.reply_text(
                "<b>🚫 Access Denied: You are not registered!</b>\n\n"
                "👉 Use /register to gain access to AI features.",
                quote=True,
                parse_mode=enums.ParseMode.HTML
            )
    print("Done Bot Active ")

    await compose(clients)


asyncio.run(main())
