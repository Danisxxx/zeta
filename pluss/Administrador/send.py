from pyrogram import Client, filters
import sqlite3
from data import *

@rex(['send'])
async def send_message(client, msg):
    user_id = msg.from_user.id

    try:
        db = sqlite3.connect("Vortex.db")
        cursor = db.cursor()
        cursor.execute("SELECT id FROM Users WHERE id = ?", (user_id,))
        result = cursor.fetchone()
    except sqlite3.OperationalError as e:
        await msg.reply(f"Error al conectar con la base de datos: {str(e)}", reply_to_message_id=msg.id)
        return
    finally:
        db.close()

    if result is None:
        await msg.reply(f"**__[あ](tg://user?id={user_id}) » No estás registrado en el bot, por favor regístrate con /register__**", reply_to_message_id=msg.id)
        return

    try:
        db = sqlite3.connect('roles.db')
        cursor = db.cursor()
        cursor.execute("SELECT role FROM roles WHERE user_id = ?", (user_id,))
        role_result = cursor.fetchone()
    except sqlite3.OperationalError as e:
        await msg.reply(f"Error al conectar con la base de datos de roles: {str(e)}", reply_to_message_id=msg.id)
        return
    finally:
        db.close()

    if role_result is None or role_result[0].lower() not in ['owner', 'admin', 'dev']:
        await msg.reply(f"<b>[<a href=tg://user?id={user_id}>⽷</a>] No cuentas con los privilegios suficientes para realizar esta acción</b>", reply_to_message_id=msg.id)
        return

    command_args = msg.command[1:]

    # Caso 1: ".send -ID Mensaje" o ".send ID Mensaje"
    if command_args and command_args[0].lstrip("-").isdigit():
        target_id = int(command_args[0])  # Obtener el ID del usuario o grupo
        if len(command_args) > 1:
            message_to_send = " ".join(command_args[1:])  # Mensaje a enviar
            try:
                await client.send_message(chat_id=target_id, text=message_to_send)
            except Exception as e:
                await msg.reply(f"Error al enviar el mensaje a {target_id}: {e}")
        elif msg.reply_to_message:
            try:
                # Reenviar el mensaje respondido al ID
                await client.forward_messages(chat_id=target_id, from_chat_id=msg.chat.id, message_ids=msg.reply_to_message.id)
            except Exception as e:
                await msg.reply(f"Error al reenviar el mensaje a {target_id}: {e}")
        else:
            await msg.reply("Debes responder a un mensaje o escribir un texto para enviarlo.")
        return

    # Obtener todos los usuarios y grupos registrados
    try:
        db = sqlite3.connect('Vortex.db')
        cursor = db.cursor()
        cursor.execute("SELECT id FROM Users")
        users_and_groups = [row[0] for row in cursor.fetchall()]
    except sqlite3.OperationalError as e:
        await msg.reply(f"Error al conectar con la base de datos: {str(e)}", reply_to_message_id=msg.id)
        return
    finally:
        db.close()

    # Caso 2: ".send mensaje" o ".send" respondiendo a un mensaje
    if command_args and len(command_args) > 0:
        message_to_send = " ".join(command_args)
        for target_id in users_and_groups:
            try:
                await client.send_message(chat_id=target_id, text=message_to_send, disable_notification=True)
            except Exception as e:
                print(f"Error al enviar mensaje a {target_id}: {e}")
        return

    if msg.reply_to_message:
        # Caso 3: ".send" respondiendo a un mensaje
        for target_id in users_and_groups:
            try:
                await client.forward_messages(chat_id=target_id, from_chat_id=msg.chat.id, message_ids=msg.reply_to_message.id)
            except Exception as e:
                print(f"Error al reenviar mensaje a {target_id}: {e}")
        return

    # Si no se especificó texto ni se respondió a un mensaje
    await msg.reply("Debes responder a un mensaje o escribir un texto para enviarlo.")
