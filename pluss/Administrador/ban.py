import sqlite3
from pyrogram import Client, filters
from data import *
from datetime import datetime

DB_PATH = "Vortex.db"
ROLES_DB_PATH = "roles.db"
NOTIFY_USERS = [6912324978, 7202754124]

def is_allowed(user_id):
    conn = sqlite3.connect(ROLES_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM roles WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0].lower() in ['admin', 'seller', 'owner', 'dev'] if result else False

def get_role(user_id):
    conn = sqlite3.connect(ROLES_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM roles WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0].lower() if result else None

def is_user_in_db(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM Users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return bool(result)

def get_ban_status(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT ban FROM Users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def ban_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE Users SET ban = 'True' WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

def unban_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE Users SET ban = 'False' WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

async def reply_message(client, message, text):
    await message.reply(
        text,
        reply_to_message_id=message.id,
        disable_web_page_preview=True
    )

async def notify_users(client, text):
    for user_id in NOTIFY_USERS:
        try:
            await client.send_message(user_id, text, disable_web_page_preview=True)
        except Exception:
            pass

@rex(['ban'])
async def ban_command(client, message):
    user_id = message.from_user.id

    if not is_allowed(user_id):
        await reply_message(client, message, "<b>No cuentas con los privilegios suficientes para realizar esta acción</b>")
        return

    args = message.command[1:]
    if len(args) < 1:
        await reply_message(client, message, "<b><i>User $ban id|@username</i></b>")
        return

    target_user_id = int(args[0])

    if user_id == target_user_id:
        await reply_message(client, message, "<b>No puedes banearte a ti mismo</b>")
        return

    if not is_user_in_db(target_user_id):
        await reply_message(client, message, "<b>Este Usuario No se ha Encontrado en La DB ❗️</b>")
        return

    target_role = get_role(target_user_id)
    if target_role == 'owner':
        await reply_message(client, message, "<b>No puedes banear a un usuario con el rol de Owner</b>")
        return

    ban_status = get_ban_status(target_user_id)
    if ban_status == 'True':
        await reply_message(client, message, "<b>Usuario Ya Baneado</b>")
        return

    ban_user(target_user_id)

    try:
        target_user = await client.get_users(target_user_id)
        username = target_user.username if target_user.username else "Sin username"
    except Exception:
        username = "Sin username"

    admin_id = message.from_user.id
    admin_username = message.from_user.username or "Sin username"

    confirmation_message = f"""
<b>Usuario Baneado</b>

<b>Usuario: @{username} [<code>{target_user_id}</code>]</b>
<b>Admin: @{admin_username} [<code>{admin_id}</code>]</b>
"""

    await reply_message(client, message, confirmation_message)
    await notify_users(client, confirmation_message)

@rex(['unban'])
async def unban_command(client, message):
    user_id = message.from_user.id

    if not is_allowed(user_id):
        await reply_message(client, message, "<b>No cuentas con los privilegios suficientes para realizar esta acción</b>")
        return

    args = message.command[1:]
    if len(args) < 1:
        await reply_message(client, message, "<b><i>User $unban id|@username</i></b>")
        return

    target_user_id = int(args[0])

    if not is_user_in_db(target_user_id):
        await reply_message(client, message, "<b>Este Usuario No se ha Encontrado en La DB ❗️</b>")
        return

    ban_status = get_ban_status(target_user_id)
    if ban_status == 'False':
        await reply_message(client, message, "<b>Usuario No Está Baneado</b>")
        return

    unban_user(target_user_id)

    try:
        target_user = await client.get_users(target_user_id)
        username = target_user.username if target_user.username else "Sin username"
    except Exception:
        username = "Sin username"

    admin_id = message.from_user.id
    admin_username = message.from_user.username or "Sin username"

    confirmation_message = f"""
<b>Usuario Desbaneado</b>

<b>Usuario: @{username} [<code>{target_user_id}</code>]</b>
<b>Admin: @{admin_username} [<code>{admin_id}</code>]</b>
"""

    await reply_message(client, message, confirmation_message)
    await notify_users(client, confirmation_message)
