from pyrogram import Client
from data import *
from pluss.Func import connect_to_db
from configs._def_main_ import *

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
    cursor.execute("SELECT id FROM Users WHERE id = ?", (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    return user_data is not None

@rex(['groupme'])
async def chk(client, msg):
    user_id = msg.from_user.id
    group_id = str(msg.chat.id)
    group_name = msg.chat.title or "Desconocido"

    if await is_banned(user_id):
        await msg.reply_text(banned, disable_web_page_preview=True, reply_to_message_id=msg.id)
        return

    if not await is_registered(user_id):
        await msg.reply_text(regist, disable_web_page_preview=True, reply_to_message_id=msg.id)
        return

    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT Dias, Expiracion, Rango FROM Users WHERE ID = ?", (group_id,))
    group_info = cursor.fetchone()
    conn.close()

    dias, expiration, rango = group_info if group_info else (None, None, None)
    status_text = "No Authorized"
    plan = "No Authorized"

    if dias and int(dias) > 0 and rango.strip():
        status_text = "Authorized"
        plan = "Authorized"

    response = groupinfo.format(
        group_id=group_id,
        group_name=group_name,
        plan=plan,
        expiration=expiration or "No plan contrated"
    )

    await msg.reply_text(response.strip(), reply_markup=link, reply_to_message_id=msg.id)
