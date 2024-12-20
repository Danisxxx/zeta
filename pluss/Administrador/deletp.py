from pyrogram import Client, filters
import sqlite3
from data import *

db_path = "Vortex.db"
roles_db_path = 'roles.db'

def user_has_permission(user_id):
    conn = sqlite3.connect(roles_db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT role FROM roles WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    
    conn.close()
    
    if result:
        return result[0].lower() in ['owner', 'admin', 'seller', 'dev']
    return False

def reset_user(user_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT rango FROM Users WHERE id = ?", (user_id,))
    result = cursor.fetchone()

    if result:
        rango = result[0].lower() if result[0] else ""
        if rango == "premium":
            cursor.execute("""
                UPDATE Users
                SET dias = 0, creditos = 0, rango = 'Free User', expiracion = 0
                WHERE id = ?
            """, (user_id,))
        else:
            cursor.execute("""
                UPDATE Users
                SET dias = 0, creditos = 0, expiracion = 0
                WHERE id = ?
            """, (user_id,))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

@rex(['deletp'])
async def deltp_command(client, message):
    user_id = str(message.from_user.id)
    
    if not user_has_permission(user_id):
        return

    target_id = None

    if message.reply_to_message:
        target_id = message.reply_to_message.from_user.id
    else:
        args = message.text.split()[1:]
        if len(args) == 0:
            await message.reply(
                "<b>[<a href=https://t.me/kanekichek_bot><b>後</b></a>] Uso incorrecto:</b> <code>$deletp id|@username</code></b>", 
                reply_to_message_id=message.id,
                disable_web_page_preview=True
            )
            return
        if args[0].startswith('@'):
            username = args[0][1:]
            user = await client.get_users(username)
            target_id = user.id
        else:
            try:
                target_id = int(args[0])
            except ValueError:
                await message.reply(
                    "<b>[<a href=https://t.me/kanekichek_bot><b>後</b></a>] Uso incorrecto:</b> <code>$deletp id|@username</code></b>", 
                    reply_to_message_id=message.id,
                    disable_web_page_preview=True
                )
                return

    if reset_user(target_id):
        await message.reply(
            f"<b>[<a href=https://t.me/kanekichek_bot><b>後</b></a>] El ID <code>{target_id}</code> ha sido reseteado exitosamente.</b>",
            reply_to_message_id=message.id,
            disable_web_page_preview=True
        )
