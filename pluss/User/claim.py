from pluss.Func import connect_to_db
from data import *
from datetime import datetime, timedelta
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

@rex(['claim'])
async def chk(client, msg):
    user_id = msg.from_user.id

    if await is_banned(user_id):
        await msg.reply_text(banned, disable_web_page_preview=True, reply_to_message_id=msg.id)
        return

    if not await is_registered(user_id):
        await msg.reply_text(regist, disable_web_page_preview=True, reply_to_message_id=msg.id)
        return

    key = msg.text.split(maxsplit=1)[1] if len(msg.text.split()) > 1 else None
    if not key:
        await msg.reply_text(provide_key, disable_web_page_preview=True, reply_to_message_id=msg.id)
        return

    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("SELECT Dias, Status FROM key WHERE Key = ?", (key,))
    result = cursor.fetchone()

    if not result:
        await msg.reply_text(invalid, disable_web_page_preview=True, reply_to_message_id=msg.id)
        conn.close()
        return

    dias, status = result

    if status == "OFF ❌":
        await msg.reply_text(invalid, disable_web_page_preview=True, reply_to_message_id=msg.id)
    elif status == "Live ✅":
        cursor.execute("UPDATE Users SET dias = ? WHERE ID = ?", (dias, msg.from_user.id))
        cursor.execute("UPDATE key SET Status = 'OFF ❌' WHERE Key = ?", (key,))
        conn.commit()

        expiration_date = (datetime.now().replace(hour=23, minute=59, second=59) + timedelta(days=dias)).strftime("%d-%m-%Y %I:%M:%S %p")
        response = claim.format(
            key=key,
            msg=msg,
            expiration_date=expiration_date
        )
        await msg.reply_text(
            response,
            disable_web_page_preview=True,
            reply_markup=link,
            reply_to_message_id=msg.id
        )

    conn.close()
