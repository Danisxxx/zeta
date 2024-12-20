from configs._def_main_ import *

@rexbt('tools')
async def exit(client, msg):
    await msg.edit_message_text(tools,reply_markup=atras)
   
    