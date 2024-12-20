from configs._def_main_ import *
from pluss.Func import connect_to_db

@rex(['start', 'ini', 'main', 'iniciar', 'star'])
async def start(client, msg):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (msg.from_user.id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        ms = startx.format(
            name=msg.from_user.first_name,
            username=msg.from_user.username if msg.from_user.username else "No username",
            user_id=user[0],
            rank=user[1]
        )
        await msg.reply_text(ms, reply_markup=atras, disable_web_page_preview=True, reply_to_message_id=msg.id)
    else:
        await msg.reply_text(controndb, reply_markup=dbre, disable_web_page_preview=True)
