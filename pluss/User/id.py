from configs._def_main_ import *
from pyrogram import Client
from data import *
from pluss.Func import connect_to_db, connect_to_roles_db

async def is_banned(user_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT ban FROM Users WHERE id = ?", (user_id,))
    ban_status = cursor.fetchone()
    conn.close()
    return ban_status and ban_status[0] == 'True'

async def is_registered(user_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Users WHERE id=?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

@rex(['id'])
async def id(client, msg):
    if await is_banned(msg.from_user.id):
        await msg.reply_text(banned, disable_web_page_preview=True, reply_to_message_id=msg.id)
        return

    if not await is_registered(msg.from_user.id):
        await msg.reply_text(regist, disable_web_page_preview=True, reply_to_message_id=msg.id)
        return

    if msg.reply_to_message:
        user_id = msg.reply_to_message.from_user.id
    elif len(msg.command) > 1 and msg.command[1].startswith("@"):
        username = msg.command[1][1:]
        try:
            user = await client.get_users(username)
            user_id = user.id
        except:
            await msg.reply_text(error_username, disable_web_page_preview=True)
            return
    elif len(msg.command) > 1 and msg.command[1].isdigit():
        user_id = int(msg.command[1])
    else:
        user_id = msg.from_user.id

    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT ban, rango, fecha_registro FROM Users WHERE id=?", (user_id,))
    user_info = cursor.fetchone()
    conn.close()

    if not user_info:
        await msg.reply_text(user_not_registered, disable_web_page_preview=True, reply_to_message_id=msg.id)
        return

    ban_status, rango, fecha_registro = user_info

    roles_conn = connect_to_roles_db()
    roles_cursor = roles_conn.cursor()
    roles_cursor.execute("SELECT role FROM roles WHERE user_id=?", (user_id,))
    role_info = roles_cursor.fetchone()
    roles_conn.close()

    role = role_info[0] if role_info else "No disponible"
    user_name = (await client.get_users(user_id)).first_name
    username = (await client.get_users(user_id)).username or "No disponible"
    chat_id = msg.chat.id  

    response = textid.format(
        username=username,
        user_id=user_id,
        first_name=user_name,
        chat_id=chat_id,
        rango=rango,
        role=role,
        ban_status=ban_status,
        fecha_registro=fecha_registro
    )

    await msg.reply_text(
        response,
        disable_web_page_preview=True,
        reply_markup=link,
        reply_to_message_id=msg.id
    )
