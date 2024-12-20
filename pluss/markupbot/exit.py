from configs._def_main_ import *

@rexbt('exit')
async def exit(client, msg):
    await msg.edit_message_text("""
<b>Good bye! 🌩
━━━━━━━━━━━━━━━━━
Enjoy my use.</b>""")