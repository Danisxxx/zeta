from pyrogram import Client, filters
import sqlite3
from data import *

ROLES_DB_PATH = "roles.db"

def is_allowed(user_id):
    conn = sqlite3.connect(ROLES_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM roles WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0].lower() in ['admin', 'seller', 'owner', 'dev'] if result else False

@rex(['panel'])
async def panel(client, message):
    user_id = message.from_user.id

    if is_allowed(user_id):
        panel_message = f"""
<b>[⌁](tg://user?id={user_id}) Admin Panel</b>
━━━━━━━━━━━━━━
<b>[⌁](tg://user?id={user_id}) $ban:</b> <code>Banea A User Del Bot</code>
<b>[⌁](tg://user?id={user_id}) $unban:</b> <code>Desbanea Use Del Botr</code>
<b>[⌁](tg://user?id={user_id}) $deltp:</b> <code>Resetea User De La DB</code>
<b>[⌁](tg://user?id={user_id}) $tp:</b> <code>Añade Membresia Al User</code>
<b>[⌁](tg://user?id={user_id}) $send:</b> <code>Enviar Mensaje Del Bot</code>
<b>[⌁](tg://user?id={user_id}) $addcr:</b> <code>Añade Creditos Al User</code>
<b>[⌁](tg://user?id={user_id}) $addg:</b> <code>Da Membresia A Grupos</code>
<b>[⌁](tg://user?id={user_id}) $key: $key:</b> <code>Genera Key Secretas</code>
<b>[⌁](tg://user?id={user_id}) $keyr: $keyr:</b> <code>Elimina La Key Canjeada</code>
<b>[⌁](tg://user?id={user_id}) $rol:</b> <code>Dar Rol Al User</code>
━━━━━━━━━━━━━━
<b>Nota: Se solicita a los sellers admins usar los comandos de forma responsable. Un mal uso puede resultar en la pérdida de privilegios. Contacten con los owners para dudas o inquietudes.</b>
"""
        await message.reply_text(panel_message, reply_to_message_id=message.id)