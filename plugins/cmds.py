from pyrogram import Client, filters, enums


@Client.on_message(filters.command('cmds'))
async def add_pvt(Client: Client, message: str) -> None:
    try:
        msg: str = "🤖 <b>Available Commands:</b>\n\n"\
            "1️⃣ <code>/att [ROLL NO]</code>\n"\
            "    📚 Get student's attendance\n"\
            "    💡 Example: <code>/att 23KB1A0XXX</code>\n\n"\
            "2️⃣ <code>/ai [ARGUMENT]</code>\n"\
            "    🤔 Get response from AI\n"\
            "    💡 Example: <code>/ai write a c program</code>\n\n"\
            "3️⃣ <code>/id</code>\n"\
            "    🆔 Get user and chat information\n"\
            "    💡 Reply to a message to get that user's info"
        await message.reply_text(msg, parse_mode=enums.ParseMode.HTML)
    except:
        await message.reply_text("❌ <b>ERROR!</b>", parse_mode=enums.ParseMode.HTML)
        return
