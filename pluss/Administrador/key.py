from configs._def_main_ import *
from datetime import datetime, timedelta
import random
import string
import sqlite3
from pluss.Func import connect_to_roles_db

def generar_clave(longitud=7):
    base = "ZETA~PREMIUM~"
    caracteres = string.ascii_letters + string.digits
    clave_aleatoria = ''.join(random.choices(caracteres, k=longitud))
    return base + clave_aleatoria

@rex(['key'])
async def key(client, message):
    db = None  
    try:
        user_id = message.from_user.id
        db_roles = connect_to_roles_db()
        cursor_roles = db_roles.cursor()

        cursor_roles.execute('SELECT role FROM roles WHERE user_id = ?', (user_id,))
        user_role = cursor_roles.fetchone()

        if not user_role or user_role[0].lower() in ['mod']:  
            from configs._def_main_ import roles
            await message.reply_text(roles, reply_to_message_id=message.id)
            db_roles.close()
            return

        command = message.text.split()
        if len(command) != 2 or not command[1].isdigit():
            await message.reply_text("<b>[<a href=t.me/Zetachkbot>後</a>] AdminHub: $key | Key: dias/days</b>", reply_to_message_id=message.id)
            return

        dias = int(command[1])

        # Limitar a 6 dígitos
        if dias > 999999:
            dias = 999999

        db = connect_to_db()
        cursor = db.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS key (
            Key TEXT,
            Dias INTEGER,
            Status TEXT,
            Valid TEXT
        )''')

        generated_key = generar_clave()
        valid_until = (datetime.now() + timedelta(days=dias)).strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute('INSERT INTO key (Key, Dias, Status, Valid) VALUES (?, ?, ?, ?)', 
                       (generated_key, dias, 'Activo', valid_until))
        db.commit()

        response = key_template.format(
            key=generated_key,
            dias=dias,
            Username=message.from_user.username if message.from_user.username else "N/A",
            Valid=valid_until,
            Condition="[PREMIUM]"
        )

        await message.reply_text(response, disable_web_page_preview=True, reply_to_message_id=message.id)
    except Exception as e:
        await message.reply_text(f"Ocurrió un error: {str(e)}", reply_to_message_id=message.id)
    finally:
        if db: 
            db.close()
        if db_roles:
            db_roles.close()
