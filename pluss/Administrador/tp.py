from pyrogram import Client, filters
import sqlite3
from data import *
import time
import uuid
from datetime import datetime, timedelta

db_path = "Vortex.db"
roles_path = "roles.db"

@rex(['tp'])
async def chk(client, msg):
    user_id = msg.from_user.id

    roles_conn = sqlite3.connect(roles_path)
    roles_cursor = roles_conn.cursor()

    roles_cursor.execute("SELECT role FROM roles WHERE user_id = ?", (user_id,))
    role_data = roles_cursor.fetchone()

    if not role_data or role_data[0].lower() not in ['owner', 'dev', 'hunter', 'admin', 'seller']:
        roles_conn.close()
        return

    roles_conn.close()

    command_args = msg.text.split()

    if len(command_args) != 3:
        await msg.reply_text("<b>[<a href=https://t.me/kanekichek_bot><b>後</b></a>] AdminHub: $tp | User: id/@username</b>", disable_web_page_preview=True, reply_to_message_id=msg.id)
        return

    target_id = command_args[1]
    try:
        days_to_add = int(command_args[2])
    except ValueError:
        await msg.reply_text("<b>[<a href=https://t.me/kanekichek_bot><b>後</b></a>] Error: El número de días debe ser un valor entero.</b>", disable_web_page_preview=True, reply_to_message_id=msg.id)
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT ID, dias, ban FROM Users WHERE ID = ?", (target_id,))
    user_data = cursor.fetchone()

    if not user_data:
        await msg.reply_text(f"<b>[<a href=https://t.me/kanekichek_bot><b>後</b></a>] Error: Usuario no registrado en la base de datos (ID: <code>{target_id}</code>)</b>", disable_web_page_preview=True, reply_to_message_id=msg.id)
        conn.close()
        return

    if len(user_data) < 3:
        await msg.reply_text("<b>[<a href=https://t.me/kanekichek_bot><b>後</b></a>] Error: los datos del usuario no están completos en la base de datos.</b>", disable_web_page_preview=True, reply_to_message_id=msg.id)
        conn.close()
        return

    if user_data[2] == 'True':
        response = f"<b><i>[↯](tg://user?id={target_id}) » Usuario Baneado❗</i></b>"
        await msg.reply_text(response, disable_web_page_preview=True, reply_to_message_id=msg.id)
        conn.close()
        return

    expiration_date = datetime.now() + timedelta(days=days_to_add)
    expiration_date_str = expiration_date.strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute("UPDATE Users SET dias = ? WHERE ID = ?", (days_to_add, target_id))
    conn.commit()

    cursor.execute("SELECT ID, dias FROM Users WHERE ID = ?", (target_id,))
    updated_user_data = cursor.fetchone()

    conn.close()

    admin_response = f"""
<b>Admin Panel / User Activate</b>
━━━━━━━━━━━
<b>ID: <code>{target_id}</code></b>
<b>Rol: Premium</b>
<b>Dias: {int(updated_user_data[1])}</b>
<b>Activos Hasta: <code>{expiration_date_str}</code></b>
<b>Actualizado Por: @{msg.from_user.username}</b> [<code>{msg.from_user.id}</code>]
"""

    await msg.reply_text(admin_response, disable_web_page_preview=True, reply_to_message_id=msg.id)
