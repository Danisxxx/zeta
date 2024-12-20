from configs._def_main_ import *

def get_user_data(user_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT rango, creditos, dias, ban, expiracion, antispam 
        FROM Users WHERE id = ?""", (user_id,))
    data = cursor.fetchone()
    conn.close()
    return data

@rexbt('perfil')
async def exit(client, msg):
    target_id = msg.from_user.id
    
    data = get_user_data(target_id)
    if data is None:
        await msg.edit_message_text("No se encontraron datos del usuario.", reply_markup=atras)
        return

    rank, credits, days, ban_status, expiration, antispam = data
    user_info = await client.get_users(target_id)
    first_name = user_info.first_name or "N/A"
    username = user_info.username or "None"
    user_link = f"tg://user?id={target_id}"
    ban_text = "True" if ban_status == "True" else "False"
    expiration_text = expiration or "0"
    time_text = days or "0"

    response = perfil.format(
        username=username,
        target_id=target_id,
        first_name=first_name,
        user_link=user_link,
        ban_text=ban_text,
        rank=rank,
        credits=credits,
        antispam=antispam,
        expiration_text=expiration_text
    )

    await msg.edit_message_text(response, reply_markup=atras)
