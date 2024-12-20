from pluss.Func import connect_to_db
from configs._def_main_ import *

async def is_banned(user_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT ban FROM Users WHERE id = ?", (user_id,))
    ban_status = cursor.fetchone()
    conn.close()
    return ban_status and ban_status[0] == 'True'

async def is_registered(user_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Users WHERE id=?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

@rex('bin')
async def start(client, msg):
    if await is_banned(msg.from_user.id):
        await msg.reply_text(banned, disable_web_page_preview=True, reply_to_message_id=msg.id)
        return

    if not await is_registered(msg.from_user.id):
        await msg.reply_text(regist, disable_web_page_preview=True, reply_to_message_id=msg.id)
        return

    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("SELECT rango FROM users WHERE id = ?", (msg.from_user.id,))
    user_exists = cursor.fetchone()
    if user_exists:
        ccbin = msg.text[len('/bin '):]
        if not ccbin:
            msg1 = "<b><code>.bin 123456</code> | ingrese un bin.</b>"
            return await msg.reply_text(msg1, disable_web_page_preview=True, reply_to_message_id=msg.id)
        if len(str(ccbin)) < 6:
            msg1 = "<b>el bin es menos de 6 digitos | ingrese un bin.</b>"
            return await msg.reply_text(msg1, disable_web_page_preview=True, reply_to_message_id=msg.id)
        
        ccbin = ccbin[:6]
        
        binreq = requests.get(f'https://bins.antipublic.cc/bins/{ccbin}')
        if 'Invalid BIN' in binreq.text or 'not found' in binreq.text:
            msg1 = "<b>Status Dead ❌ | Invalid BIN.</b>"
            return await msg.reply_text(msg1, disable_web_page_preview=True, reply_to_message_id=msg.id)
        
        rango = user_exists[0]
        msg1 = bin.format(
            binif=ccbin,
            brand=binreq.json()['brand'],
            country=binreq.json()['country'],
            country_name=binreq.json()['country_name'],
            country_flag=binreq.json()['country_flag'],
            bank=binreq.json()['bank'],
            level=binreq.json()['level'],
            type=binreq.json()['type'],
            name=msg.from_user.username if msg.from_user.username else msg.from_user.first_name,
            rango=rango
        )
        
        await msg.reply_text(
            msg1,
            disable_web_page_preview=True,
            reply_markup=link,
            reply_to_message_id=msg.id
        )
    else:
        data = get_user_data(msg.from_user.id)
        if data is None:
            await msg.reply_text(regist, disable_web_page_preview=True, reply_to_message_id=msg.id)
            return
