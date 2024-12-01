from pyrogram import Client, filters, enums


@Client.on_message(filters.command('id'))
async def id(Client, message):
    # print(message)
    text = ''
    if message.reply_to_message:
        text = f"👤 <b>Name:</b> <code>{message.reply_to_message.from_user.first_name} {message.reply_to_message.from_user.last_name if message.reply_to_message.from_user.last_name else ''}</code>"\
            f"\n🆔 <b>User ID:</b> <code>{message.reply_to_message.from_user.id}</code>"\
            f"\n💬 <b>Chat ID:</b> <code>{message.chat.id}</code>"
        await message.reply_text(text, parse_mode=enums.ParseMode.HTML, reply_to_message_id=message.id)
        return

    text = f"👤 <b>Name:</b> <code>{message.from_user.first_name} {message.from_user.last_name if message.from_user.last_name else ''}</code>"\
        f"\n🆔 <b>User ID:</b> <code>{message.from_user.id}</code>"\
        f"\n💬 <b>Chat ID:</b> <code>{message.chat.id}</code>"
    await message.reply_text(text, parse_mode=enums.ParseMode.HTML, reply_to_message_id=message.id)
