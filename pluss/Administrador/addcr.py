import sqlite3
from data import *
from pyrogram import Client, filters

db_path = "Vortex.db"
permisos_path = "roles.db"

@rex(["addcr"])
async def add_credits(client, msg):
    con_permisos = sqlite3.connect(permisos_path)
    cursor_permisos = con_permisos.cursor()

    cursor_permisos.execute("SELECT role FROM roles WHERE user_id=?", (str(msg.from_user.id),))
    user_role = cursor_permisos.fetchone()

    if user_role is None or user_role[0].lower() == "mod":
        con_permisos.close()
        return

    if len(msg.text.split()) != 3:
        await msg.reply_text("<b>[⌁](t.me/VortexChekBot) AdminHub: $addcr | User: id/@username</b>", disable_web_page_preview=True, reply_to_message_id=msg.id)
        con_permisos.close()
        return

    user_id = msg.text.split()[1]
    try:
        credits = int(msg.text.split()[2])
    except ValueError:
        await msg.reply_text("<b>[⌁](t.me/VortexChekBot) Por favor, ingresa una cantidad válida de créditos.</b>", disable_web_page_preview=True, reply_to_message_id=msg.id)
        con_permisos.close()
        return

    con = sqlite3.connect(db_path)
    cursor = con.cursor()

    cursor.execute("SELECT * FROM Users WHERE id=?", (user_id,))
    user = cursor.fetchone()

    if user is None:
        await msg.reply_text(f"<b>[<a href=https://t.me/kanekichek_bot><b>後</b></a>] Error: Usuario no registrado en la base de datos (ID: <code>{user_id}</code>)</b>", disable_web_page_preview=True, reply_to_message_id=msg.id)
        con.close()
        con_permisos.close()
        return

    if user[6] == 'True' or user[6] == 'true':  
        response = f"<b><i>[↯](tg://user?id={user_id}) » Usuario Baneado❗</i></b>"
        await msg.reply_text(response, disable_web_page_preview=True, reply_to_message_id=msg.id)
        con.close()
        con_permisos.close()
        return

    cursor.execute("UPDATE Users SET creditos=? WHERE id=?", (credits, user_id))
    con.commit()

    response_text = f"<b>[⌁](t.me/VortexChekBot) Al ID <code>{user_id}</code> se le han asignado {credits} créditos.</b>"
    con.close()
    con_permisos.close()

    await msg.reply_text(response_text, disable_web_page_preview=True, reply_to_message_id=msg.id)
