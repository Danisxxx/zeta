from configs._def_main_ import *
from pluss.Func import connect_to_db

def get_user_data(user_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT rango, creditos, dias, ban, expiracion, antispam 
        FROM Users WHERE id = ?""", (user_id,))
    data = cursor.fetchone()
    conn.close()
    return data

async def is_banned(user_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT ban FROM Users WHERE id = ?", (user_id,))
    ban_status = cursor.fetchone()
    conn.close()
    return ban_status and ban_status[0] == 'True'

@rex(['me'])
async def send_message(client, msg):
    user_id = msg.from_user.id

    if await is_banned(user_id):
        await msg.reply_text(banned, disable_web_page_preview=True, reply_to_message_id=msg.id)
        return

    target_id = user_id
    if len(msg.command) == 2:
        arg = msg.command[1]
        if arg.isdigit():
            target_id = int(arg)
        elif arg.startswith("@"):
            try:
                user_info = await client.get_users(arg[1:])
                target_id = user_info.id
            except Exception:
                await msg.reply_text(
                    "<b>[Security System ⚠️] => Este Usuario No está registrado En Mi Base de Datos.</b>",
                    disable_web_page_preview=True,
                    reply_markup=link,
                    reply_to_message_id=msg.id
                )
                return
    elif msg.reply_to_message:
        target_id = msg.reply_to_message.from_user.id

    data = get_user_data(target_id)
    if data is None:
        await msg.reply_text(regist, disable_web_page_preview=True, reply_to_message_id=msg.id)
        return

    rank, credits, days, ban_status, expiration, antispam = data
    user_info = await client.get_users(target_id)
    first_name = user_info.first_name or "N/A"
    username = user_info.username or "None"
    user_link = f"tg://user?id={target_id}"
    ban_text = "True" if ban_status == "True" else "False"
    expiration_text = expiration or "0"
    time_text = days or "0"

    response = info.format(
        username=username,
        target_id=target_id,
        first_name=first_name,
        user_link=user_link,
        ban_text=ban_text,
        rank=rank,
        credits=credits,
        antispam=antispam,
        expiration_text=expiration_text
    )

    await msg.reply_text(
        response,
        disable_web_page_preview=True,
        reply_markup=atras,
        reply_to_message_id=msg.id
    )
