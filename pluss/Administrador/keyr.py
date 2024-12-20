from data import *
from pyrogram import Client, filters
import sqlite3
from datetime import datetime, timedelta
import re

db_path = "Vortex.db"
roles_path = "roles.db"

def check_user_role(user_id):
    conn = sqlite3.connect(roles_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT role FROM roles WHERE user_id = ?", (user_id,))
    role_data = cursor.fetchone()
    
    conn.close()
    
    if role_data:
        role = role_data[0].lower()
        allowed_roles = ['admin', 'seller', 'dev', 'owner']
        if role in allowed_roles:
            return True
    return False

def parse_expiration(expiration):
    try:
        days, time_part = expiration.split('d-')
        hours, minutes, seconds = map(int, time_part.replace('h-', ':').replace('m-', ':').replace('s', '').split(':'))
        return timedelta(days=int(days), hours=hours, minutes=minutes, seconds=seconds)
    except ValueError:
        print(f"Error: formato de expiración incorrecto '{expiration}'")
        return timedelta(0)

def format_time_delta(delta):
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days}d-{hours}h-{minutes}m-{seconds}s"

def update_user_expiration(user_id, additional_days, is_revert=False):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT dias FROM Users WHERE id = ?", (user_id,))
    user_data = cursor.fetchone()

    if user_data:
        current_days = user_data[0]

        cursor.execute("SELECT expiracion FROM Vip WHERE id = ?", (user_id,))
        vip_data = cursor.fetchone()

        if vip_data:
            current_expiration = vip_data[0]

            if current_expiration:
                expiration_time = parse_expiration(current_expiration)
                if is_revert:
                    expiration_time -= timedelta(days=additional_days)
                else:
                    expiration_time += timedelta(days=additional_days)
                new_expiration = format_time_delta(expiration_time)
            else:
                new_expiration = format_time_delta(timedelta(days=current_days + additional_days))

            cursor.execute("UPDATE Vip SET expiracion = ? WHERE id = ?", (new_expiration, user_id))
        else:
            new_expiration = format_time_delta(timedelta(days=current_days + additional_days))

        new_days = current_days + additional_days if not is_revert else current_days - additional_days
        cursor.execute("UPDATE Users SET dias = ? WHERE id = ?", (new_days, user_id))
        conn.commit()

    conn.close()

@rex(['keyr'])
async def keyr(client, msg):
    user_id = msg.from_user.id

    if not check_user_role(user_id):
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    args = msg.text.split(maxsplit=1)
    if len(args) < 2:
        await msg.reply_text("<b>[<a href=https://t.me/kanekichek_bot><b>⽷</b></a>] Ingresa Una Key Valida</b>", reply_to_message_id=msg.id, disable_web_page_preview=True)
        conn.close()
        return

    key_to_revert = args[1]

    cursor.execute("SELECT Dias FROM key WHERE Key = ?", (key_to_revert,))
    key_data = cursor.fetchone()

    if key_data:
        dias_key = key_data[0]

        cursor.execute("SELECT dias FROM Users WHERE id = ?", (user_id,))
        user_data = cursor.fetchone()

        if user_data:
            user_days = user_data[0]

            if user_days >= dias_key:
                new_user_days = user_days - dias_key
                update_user_expiration(user_id, dias_key, is_revert=True)
                response = f"<b>[<a href=https://t.me/kanekichek_bot><b>⽷</b></a>] Has Eliminado La Key => <code>{key_to_revert}</code> Ha Sido Eliminada</b>"
            else:
                response = f"<b>[<a href=https://t.me/kanekichek_bot><b>⽷</b></a>] Esta Key => <code>{key_to_revert}</code> Ya a sido Eliminada</b>"
        else:
            response = f"<b>[<a href=https://t.me/kanekichek_bot><b>⽷</b></a>] Este Usuario No existe En mi Base de Datos</b>"

        cursor.execute("UPDATE key SET Status = 'OFF ❌' WHERE Key = ?", (key_to_revert,))
        conn.commit()

    else:
        response = f"<b>[<a href=https://t.me/kanekichek_bot><b>⽷</b></a>] La key => <code>{key_to_revert}</code> No Existe o Ningun Usuario la Ha Canjeado</b>"

    await msg.reply_text(response, reply_to_message_id=msg.id, disable_web_page_preview=True)
    
    conn.close()
