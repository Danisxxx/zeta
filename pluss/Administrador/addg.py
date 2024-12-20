from pyrogram import Client
import sqlite3
from data import rex
import datetime

DB_PATH = "Vortex.db"
PERMISOS_PATH = "roles.db"

@rex(['addg'])
async def chk(client, msg):
    try:
        args = msg.text.split()
        if len(args) < 3:
            user_id = msg.from_user.id
            conn_permisos = sqlite3.connect(PERMISOS_PATH)
            cursor_permisos = conn_permisos.cursor()
            cursor_permisos.execute("SELECT role FROM roles WHERE user_id = ?", (user_id,))
            role = cursor_permisos.fetchone()
            conn_permisos.close()

            if role and role[0].lower() in ["admin", "seller", "dev", "owner", "hunter", "coder"]:
                captions = """
<b>[<a href=https://t.me/kanekichek_bot><b>後</b></a>] Admin $addg -id|dias</b>
"""
                await msg.reply_text(captions, disable_web_page_preview=True, reply_to_message_id=msg.id)
            return

        command, group_id, days = args
        group_id = group_id.strip()
        days = int(days)

        user_id = msg.from_user.id
        conn_permisos = sqlite3.connect(PERMISOS_PATH)
        cursor_permisos = conn_permisos.cursor()
        cursor_permisos.execute("SELECT role FROM roles WHERE user_id = ?", (user_id,))
        role = cursor_permisos.fetchone()
        conn_permisos.close()

        if not role or role[0].lower() not in ["admin", "seller", "dev", "owner", "hunter", "coder"]:
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT dias FROM Users WHERE id = ?", (group_id,))
        result = cursor.fetchone()

        if result:
            cursor.execute("UPDATE Users SET dias = ? WHERE id = ?", (days, group_id))
        else:
            cursor.execute("INSERT INTO Users (id, dias) VALUES (?, ?)", (group_id, days))

        conn.commit()

        expiration_date = datetime.datetime.now() + datetime.timedelta(days=days)
        expiration_str = expiration_date.strftime("%Y-%m-%d %H:%M:%S")

        # Obtener nombre de usuario del admin
        admin_user = msg.from_user.username
        admin_id = msg.from_user.id

        captions = f"""
<b>[<a href='t.me/VortexChekerBot'>ϟ</a>] Added Group: >_$-Security System ⚠️
━━━━━━━━━━━
[<a href='t.me/VortexChekerBot'>ϟ</a>] Id: <code>{group_id}</code>
[<a href='t.me/VortexChekerBot'>ϟ</a>] Days: <code>{days}</code>
[<a href='t.me/VortexChekerBot'>ϟ</a>] Plan: Supergroup
[<a href='t.me/VortexChekerBot'>ϟ</a>] Admin: @{admin_user} [<code>{admin_id}</code>]
[<a href='t.me/VortexChekerBot'>ϟ</a>] Expiración: <code>{expiration_str}</code></b>
"""

        await msg.reply_text(captions, disable_web_page_preview=True, reply_to_message_id=msg.id)

        conn.close()

    except Exception as e:
        print(f"Error: {e}")
