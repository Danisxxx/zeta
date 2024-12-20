from pyrogram import Client, filters
from data import *
import sqlite3

db_path = "Vortex.db"
permission_path = "roles.db"

@rex(['rol'])
async def rol_handler(client, msg):
    args = msg.text.split()

    with sqlite3.connect(permission_path) as perm_conn:
        perm_cursor = perm_conn.cursor()
        perm_cursor.execute("SELECT role FROM roles WHERE user_id = ?", (msg.from_user.id,))
        result = perm_cursor.fetchone()
        
        if result is None:
            return
        user_role = result[0].lower()

    if len(args) < 3:
        await msg.reply_text("<b>[<a href=https://t.me/kanekichek_bot><b>後</b></a>] AdminHub: $rol | User: id/@username | Rol</b>", disable_web_page_preview=True, reply_to_message_id=msg.id)
        return

    # Verificar si el comando usa un ID o un username
    if args[1].startswith('@'):
        username = args[1][1:]  # Eliminar '@' del username
        user = await client.get_users(username)
        user_id = user.id
    else:
        user_id = args[1]

    new_role = " ".join(args[2:])
    
    with sqlite3.connect(permission_path) as perm_conn:
        perm_cursor = perm_conn.cursor()
        perm_cursor.execute("SELECT role FROM roles WHERE user_id = ?", (user_id,))
        target_role = perm_cursor.fetchone()

        if target_role is None:
            await msg.reply_text("<b>[<a href=https://t.me/kanekichek_bot><b>後</b></a>] Error: No se encontró el ID especificado.</b>", disable_web_page_preview=True, reply_to_message_id=msg.id)
            return

        target_role = target_role[0].lower()

        if user_role == "seller":
            if target_role in ["owner", "coder", "dev", "admin"]:
                await msg.reply_text("<b>[<a href=https://t.me/kanekichek_bot><b>後</b></a>] Error: No Puedes Modificarle El Rol A Este Usuario</b>", disable_web_page_preview=True, reply_to_message_id=msg.id)
                return
        elif user_role == "admin":
            if target_role in ["coder", "dev", "owner"]:
                await msg.reply_text("<b>[<a href=https://t.me/kanekichek_bot><b>後</b></a>] Error: No Puedes Modificarle El Rol A Este Usuario</b>", disable_web_page_preview=True, reply_to_message_id=msg.id)
                return
        elif user_role in ["dev", "owner", "coder"]:
            # Dev, Owner, and Coder can modify roles of anyone, including themselves
            pass

    if new_role.lower() == "none":
        new_role = "Free User"

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE Users SET rango = ? WHERE id = ?", (new_role, user_id))
        if cursor.rowcount > 0:
            await msg.reply_text(f"<b>[<a href=https://t.me/kanekichek_bot><b>後</b></a>] El rol de ID {user_id} ha sido actualizado a <code>{new_role}</code>.</b>", disable_web_page_preview=True, reply_to_message_id=msg.id)
        else:
            await msg.reply_text("<b>[<a href=https://t.me/kanekichek_bot><b>後</b></a>] Error: No se encontró el ID especificado</b>.", disable_web_page_preview=True, reply_to_message_id=msg.id)
