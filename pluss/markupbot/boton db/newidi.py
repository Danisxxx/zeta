from configs._def_main_ import *

@rexbt('idioman')
async def exit(client, msg):
    await msg.edit_message_text(controndb,reply_markup=dbre)

