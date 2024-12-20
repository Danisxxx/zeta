from configs._def_main_ import *
from pluss.Func import connect_to_db
from datetime import datetime
import pytz

@rex(['cm','cmd','cmds','comandos','command','help','ayuda'])
async def start(client, msg):
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("SELECT id FROM Users WHERE id=?", (msg.from_user.id,))
    result = cursor.fetchone()
    
    monterrey_tz = pytz.timezone('America/Monterrey')
    fecha_mx = datetime.now(monterrey_tz).strftime("%Y-%m-%d")
    hora_mx = datetime.now(monterrey_tz).strftime("%H:%M")
    
    username = msg.from_user.username if msg.from_user.username else "Unknown"
    
    if result:
        ms = cmds.format(
            fecha_mx=fecha_mx,
            hora_mx=hora_mx,
            username=username
        )
        await msg.reply_text(ms, reply_markup=mainstart, reply_to_message_id=msg.id, disable_web_page_preview=True)
    else:
        await msg.reply_text(controndb, reply_markup=dbre, reply_to_message_id=msg.id, disable_web_page_preview=True)
