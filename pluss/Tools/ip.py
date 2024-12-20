from configs._def_main_ import *
from pluss.Func import connect_to_db

def get_user_data(user_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT rango, creditos, dias, ban, expiracion, antispam 
        FROM Users WHERE id = ?""", (user_id,))
    data = cursor.fetchone()
    conn.close()
    return data

async def is_banned(user_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT ban FROM Users WHERE id = ?", (user_id,))
    ban_status = cursor.fetchone()
    conn.close()
    return ban_status and ban_status[0] == 'True'

@rex('ip')
async def start(client, msg):
    user_id = msg.from_user.id

    if await is_banned(user_id):
        await msg.reply_text(banned, disable_web_page_preview=True, reply_to_message_id=msg.id)
        return

    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Users WHERE id = ?", (user_id,))
    user_exists = cursor.fetchone()

    if user_exists:
        ips = msg.text[len('/ip '):]
        if not ips:
            return await msg.reply('<b><code>.ip 1.1.1.1</code> | Error ip.</b>')

        req = requests.get(f'https://ipwho.is/{ips}')
        if '"success":false' in req.text:
            return await msg.reply('<b>Invalid IP address ❌</b>')
        else:
            rr = req.json()
            ms = ip.format(ips=ips, fraud_score=rr.get('fraud_score', '0'), city=rr.get('city', 'N/A'), country=rr.get('country', 'N/A'), country_code=rr.get('country_code', 'N/A'), emoji=rr['flag']['emoji'], region=rr.get('region', 'N/A'), zip_code=rr.get('postal', 'N/A'))
            await msg.reply(ms)
    else:
        data = get_user_data(user_id)
        if data is None:
            await msg.reply_text(regist, disable_web_page_preview=True, reply_to_message_id=msg.id)
            return
        return await msg.reply(controndb, reply_markup=dbre)

    conn.close()
