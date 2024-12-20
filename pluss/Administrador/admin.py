from datetime import datetime
from pyrogram import Client, filters
from data import rex
import sqlite3

OWNER_IDS = [7202754124, 6912324978]

db = sqlite3.connect("roles.db")
cursor = db.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS roles (
    user_id INTEGER PRIMARY KEY,
    role TEXT,
    assigned_by TEXT,
    assigned_date TEXT
)
''')
db.commit()

@rex(['admin'])
async def chk(client, msg):
    if msg.from_user.id not in OWNER_IDS:
        response = "<b>[<a href=tg://user?id=>⽷</a>] No cuentas con los privilegios suficientes para realizar esta acción</b>"
        await msg.reply_text(response, reply_to_message_id=msg.id)
        return

    command_parts = msg.text.split()
    if len(command_parts) < 2:
        response = "<b>[↯](tg://user?id=) » User <code>$admin id|rol|(12345687|Seller)</code></b>"
        await msg.reply_text(response, reply_to_message_id=msg.id)
        return

    if command_parts[0] in ["/admin", ".admin"]:
        user_id = int(command_parts[1])
        role = command_parts[2] if len(command_parts) > 2 else "Seller"
        assigner_username = msg.from_user.username if msg.from_user.username else "Unknown"
        assigned_date = datetime.now().strftime("%d|%m|%y")

        cursor.execute('SELECT role FROM roles WHERE user_id = ?', (user_id,))
        existing_role = cursor.fetchone()

        if existing_role:
            response = f"<b>[↯](tg://user?id=) » El usuario (<code>{user_id}</code>) ya tiene el rol de <code>{existing_role[0]}</code> asignado</b>"
            await msg.reply_text(response, reply_to_message_id=msg.id)
            return

        cursor.execute('''
        INSERT OR REPLACE INTO roles (user_id, role, assigned_by, assigned_date)
        VALUES (?, ?, ?, ?)
        ''', (user_id, role, assigner_username, assigned_date))
        db.commit()

        response = f"<b>[↯](tg://user?id=) » Ahora el usuario (<code>{user_id}</code>), cumple el rol de <code>{role}</code></b>"
        await msg.reply_text(response, reply_to_message_id=msg.id)

@rex(['unadmin'])
async def unadmin(client, msg):
    if msg.from_user.id not in OWNER_IDS:
        response = "<b>[あ](tg://user?id=) No cuentas con los privilegios suficientes para realizar esta accion</b>"
        await msg.reply_text(response, reply_to_message_id=msg.id)
        return

    command_parts = msg.text.split()
    if len(command_parts) < 2:
        response = "<b>[↯](tg://user?id=) » User <code>$unadmin id (12345687)</code></b>"
        await msg.reply_text(response, reply_to_message_id=msg.id)
        return

    user_id = int(command_parts[1])

    cursor.execute('SELECT role FROM roles WHERE user_id = ?', (user_id,))
    existing_role = cursor.fetchone()

    if existing_role:
        role = existing_role[0]
        cursor.execute('DELETE FROM roles WHERE user_id = ?', (user_id,))
        db.commit()

        response = f"<b>[↯](tg://user?id=) » El usuario (<code>{user_id}</code>) ha sido removido del rol <code>{role}</code></b>"
    else:
        response = f"<b>[↯](tg://user?id=) » El usuario (<code>{user_id}</code>) no tiene un rol asignado</b>"

    await msg.reply_text(response, reply_to_message_id=msg.id)
