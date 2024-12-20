from pluss.Func import connect_to_db
from datetime import datetime
from configs._def_main_ import *

@rexbt('es')
async def exit(client, msg):
    conn = connect_to_db()
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        rango TEXT DEFAULT 'Free',
        creditos INTEGER DEFAULT 0,
        antispam INTEGER DEFAULT 60,
        dias INTEGER DEFAULT 0,
        bin_lasted TEXT DEFAULT NULL,
        fecha_registro TEXT
    )
    """)
    
    fecha_registro = datetime.now().strftime("%d/%m/%y - %I:%M%p")
    user_data = (msg.from_user.id, 'Free', 0, 60, 0, None, fecha_registro)
    
    cursor.execute("""
    INSERT OR IGNORE INTO users (user_id, rango, creditos, antispam, dias, bin_lasted, fecha_registro)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, user_data)
    
    conn.commit()
    conn.close()
    
    await msg.edit_message_text("<b>Registro completado correctamente. ✅</b>", reply_markup=homedb)
    
    await client.send_message(
        chat_id=-1002338475461,
        text=f"""<b>[•] ⇾ <a>New users register [ 👨🏿 ]</a>
                              
[•] ⇾ Id: <code>{msg.from_user.id}</code>
[•] ⇾ Alias: @{msg.from_user.username}
[•] ⇾ Name: <code>{msg.from_user.first_name}</code>
[•] ⇾ su Idioma (siglas): {msg.from_user.language_code}
[•] ⇾ Telegram premium: {msg.from_user.is_premium}

[•] ⇾ Esto es un control de registro, no un scam.
━━━━━━━━━
[•] ⇾ The 𝗪𝗼𝗿𝗹𝗱𝘀 of 𝗔𝗽𝗶𝘀
[•] ⇾ @TheWorldsOfApis
━━━━━━━━━
</b>"""
    )
