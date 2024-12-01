from pyrogram import Client, filters, enums
from plugins.utils_att import get_data
import requests
from plugins.db_connection import is_student_registered
from os import getenv

BOT_TOKEN = getenv('BOT_TOKEN')
private_access: list = ['5850533417', ]
admin_id: str = '5850533417'

groups: list = ['-1002435023187',
                '-1001939419392', '-4585529485', '-882696523']
rush_mode: bool = False


@Client.on_message(filters.command('rush'))
async def rush(Client: Client, message: str) -> None:
    global rush_mode
    try:
        if str(message.from_user.id) == admin_id:
            rush_mode = not rush_mode
            status = "🚀 ENABLED" if rush_mode else "🔄 DISABLED"
            await message.reply_text(
                f"⚡ <b>Rush Mode:</b> {status}\n"
                f"ℹ️ {
                    'Real-time updates disabled' if rush_mode else 'Real-time updates enabled'}",
                parse_mode=enums.ParseMode.HTML
            )
    except:
        await message.reply_text("❌ <b>ERROR:</b> Failed to toggle rush mode!", parse_mode=enums.ParseMode.HTML)
        return


@Client.on_message(filters.command('att'))
async def attendece_cmd(client: Client, message: str) -> None:
    # print(message)
    if str(message.chat.id) in groups or str(message.from_user.id) in private_access:
        if message.sender_chat or is_student_registered(message.from_user.id):
            try:
                checking_msg = await message.reply_text("⏳ Checking attendance, please wait...", quote=True)
                user_id: str = message.text.split(" ")[1].upper()
            except:
                await checking_msg.edit_text("<b>FORMAT :</b>  <code>/att 23KB1A0XXX</code>")
                return
            if '1':
                try:
                    if rush_mode:
                        realtime: bool = False
                        if 'realtime' in str(message.text):
                            realtime = True
                        data: dict = get_data(user_id, realtime)
                    else:
                        data: dict = get_data(user_id, True)
                    # data: dict = get_data(user_id)
                    # print(data)
                    if 'error' in data:
                        await checking_msg.edit_text(
                            "<b>Invalid format or roll number. Please use the correct format:</b>\n\n"
                            "<b>For Section C:</b> <code>/att 23KB1A0XXX</code>\n\n"
                            "<b>For other sections:</b> <code>/att 23KB1A0XXX {SECTION}</code>\n"
                            "Example: <code>/att 23KB1A0XXX A</code>\n\n"
                            "<b>Note: This bot is currently limited to 2nd year students only.</b>"
                        )
                        return

                    last_up: list = data.pop('date_up')
                    from_u: list = data.pop('from')
                    # print(dta)

                    dates: dict = {}

                    pq: list = [key for key in data.keys()][3:-1]

                    for key in pq:
                        dates[key] = last_up[pq.index(key)]

                    max_key_length: int = max(len(key) for key in pq)
                    max_value_length: int = max(len(str(value))
                                                for value in list(data.values())[3:-1])
                    max_date_length: int = max(len(date)
                                               for date in dates.values())

                    if from_u[0] == "CSE_DS":
                        pq.pop(6)
                    message1: str = ""
                    labs_count: str = f"({data[list(data.keys())[10]]})" if from_u[0] != "CSE_DS" else f"({
                        data[list(data.keys())[10+1]]})"
                    # print(pq)
                    for key in pq:
                        # Format each row with dynamic padding
                        key_str: str = key.ljust(max_key_length)
                        value_str: str = str(data[key]).ljust(max_value_length)
                        date_str: str = dates[key].ljust(max_date_length)

                        message1 += f"{key_str} : ({value_str}) - ({date_str})\n"

                    tex: str = f"🔢 <b>Roll No:</b> <code>{user_id}</code>\n"\
                        f"📚 <b>From:</b> <code>{from_u[0]} - {from_u[1]}</code>\n"\
                        f"📊 <b>Attendance:</b> <code>{data['attendance_percentage']}%</code>\n"\
                        f"🏫 <b>Total classes:</b> <code>{data['total_classes']}</code>\n\n"\
                        f"<pre language='Classes attended'>\n" + message1 +\
                        f"LABS".ljust(max_key_length) + " : " + labs_count.ljust(max_value_length) + \
                        f"</pre>"

                    await checking_msg.edit_text(tex)
                except Exception as e:
                    error_message = (
                        f"<pre language='error'>{e}</pre>\n"
                        "<b>Error occurred while fetching attendance.</b>\n\n"
                        "<b>Note: This bot is currently limited to 2nd year students only.</b>"
                    )
                    await checking_msg.edit_text(error_message)
        else:
            await message.reply_text(
                "<b>🚫 Access Denied: You are not registered!</b>\n\n"
                "👉 Use /register to gain access to attendance tracking features.",
                reply_to_message_id=message.id,
                parse_mode=enums.ParseMode.HTML
            )
    else:
        await message.reply_text(
            "<b>🚫 Access Restricted</b>\n\n"
            "This bot can only be used in the official group:\n"
            "👉 @nbkrist_attendence",
            reply_to_message_id=message.id,
            parse_mode=enums.ParseMode.HTML
        )


@ Client.on_message(filters.command('pvt'))
async def add_pvt(Client: Client, message: str) -> None:
    try:
        if str(message.from_user.id) == admin_id:
            if message.reply_to_message:
                # print(message)
                uid: str = message.reply_to_message.from_user.id

                private_access.append(str(uid))
                user_info = f'@{message.reply_to_message.from_user.username}' if message.reply_to_message.from_user.username else message.reply_to_message.from_user.first_name
                await message.reply_text(f'<b>Added</b> {user_info}', parse_mode=enums.ParseMode.HTML)
            else:
                msg: str = message.text[len('/pvt '):]
                private_access.append(str(msg))
                # Send the response with markdown parse mode
                await message.reply_text(
                    f"✅ <b>Added User:</b> <code>{msg}</code>\n"
                    f"🔐 Private access granted successfully.",
                    parse_mode=enums.ParseMode.HTML
                )
                requests.get(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id=5850533417&text={str(private_access)}")

    except:
        await message.reply_text("ERROR !")
        return
