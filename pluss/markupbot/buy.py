from configs._def_main_ import *

@rexbt('buy')
async def exit(client, msg):
    await msg.edit_message_text(buy,reply_markup=atras)