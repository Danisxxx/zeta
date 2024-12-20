from configs._def_main_ import *
from datetime import datetime
import pytz

@rexbt('home')
async def exit(client, msg):
    monterrey_tz = pytz.timezone('America/Monterrey')
    fecha_mx = datetime.now(monterrey_tz).strftime("%Y-%m-%d")
    hora_mx = datetime.now(monterrey_tz).strftime("%H:%M")
    
    username = msg.from_user.username if msg.from_user.username else "Unknown"
    
    ms = cmds.format(
        fecha_mx=fecha_mx,
        hora_mx=hora_mx,
        username=username
    )
    
    await msg.edit_message_text(ms, reply_markup=mainstart)
