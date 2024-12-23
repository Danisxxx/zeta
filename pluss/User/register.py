from datetime import datetime
from pyrogram import Client, filters
import mysql.connector
from data import *
from configs._def_main_ import *

def connect_to_db():
    mysql_url = "mysql://root:AALCqBDaYexmmkDBZzqGgdMXpBpcwDIj@mysql.railway.internal:3306/railway"
    
    import urllib.parse
    result = urllib.parse.urlparse(mysql_url)
    db_config = {
        'user': result.username,
        'password': result.password,
        'host': result.hostname,
        'port': result.port,
        'database': result.path[1:],  # Elimina el primer carácter '/' del path
    }

    conn = mysql.connector.connect(**db_config)
    return conn

@rex(['register'])
async def chk(client, msg):
    user_id = msg.from_user.id
    user_username = msg.from_user.username or "Sin nombre de usuario"

    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        # Verificar si el usuario ya está registrado
        cursor.execute("SELECT * FROM Users WHERE id=%s", (user_id,))
        if cursor.fetchone():
            await msg.reply(
                textea.format(user_id=user_id, user_username=user_username),
                disable_web_page_preview=True,
                reply_to_message_id=msg.id
            )
        else:
            # Si no está registrado, insertarlo en la base de datos
            fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute('''
                INSERT INTO Users (id, rango, dias, expiracion, creditos, antispam, bin_lasted, ban, fecha_registro) 
                VALUES (%s, %s, %s, %s, %s, %s, NULL, %s, %s)
            ''', (user_id, 'Free User', 0, '', 0, 0, 'False', fecha_registro))
            conn.commit()
            await msg.reply(
                texteb.format(user_username=user_username),
                disable_web_page_preview=True,
                reply_to_message_id=msg.id
            )
    except mysql.connector.Error as err:
        await msg.reply(
            f"Se produjo un error al intentar acceder a la base de datos: {err}",
            disable_web_page_preview=True,
            reply_to_message_id=msg.id
        )
    finally:
        conn.close()
