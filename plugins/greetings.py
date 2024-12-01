from datetime import datetime
from pyrogram import Client, enums, filters


@Client.on_message(filters.new_chat_members)
async def welcome(client: Client, message: str) -> None:
    """
    Welcomes new members when they join the chat.
    Sends a formatted message with user details and registration instructions.
    """
    for new_member in message.new_chat_members:
        member_name: str = new_member.first_name if new_member.first_name else "there"
        user_name: str = f"\n<b>𝚈𝚘𝚞𝚛 𝚄𝚜𝚎𝚛𝚗𝚊𝚖𝚎: </b> @{new_member.username}" if new_member.username else ""
        user_id: str = new_member.id
        now: datetime = datetime.now()
        join_date: str = now.strftime("%Y-%m-%d")
        chat_members_count: int = await client.get_chat_members_count(message.chat.id)
        
        msg: str = f"<b>𝙷𝚕𝚠</b> {member_name} {user_name}\n"
        msg += f"<b>𝚈𝚘𝚞𝚛 𝙸𝙳: </b> <code>{user_id}</code>\n"
        msg += f"<b>𝙹𝚘𝚒𝚗 𝚍𝚊𝚝𝚎: </b> <code>{join_date}</code>\n"
        msg += f"<b>𝙼𝚎𝚖𝚋𝚎𝚛 𝚗𝚞𝚖𝚋𝚎𝚛: </b> <code>{chat_members_count}</code>\n"
        msg += f"/register <b>𝚝𝚘 𝚛𝚎𝚐𝚒𝚜𝚝𝚎𝚛</b>"
        await message.reply_text(msg)


@Client.on_message(filters.left_chat_member)
async def farewell_user(client: Client, message: str):
    """
    Sends farewell messages when users leave the chat.
    Attempts to send a DM to the leaving user with an invitation to return.
    """
    left_member = message.left_chat_member
    await message.reply_text(
        f"𝙽𝚒𝚌𝚎 𝚔𝚗𝚘𝚠𝚒𝚗𝚐 𝚢𝚘𝚞 {left_member.first_name}", 
        parse_mode=enums.ParseMode.HTML
    )
    try:
        await client.send_message(
            left_member.id, 
            "You left the <a href='https://t.me/nbkrist_attendence'>NBKRIST ATTENDENCE</a>. We hope to see you back someday!"
        )
    except Exception as e:
        print(f"Couldn't send a DM to {left_member.id}: {e}")
