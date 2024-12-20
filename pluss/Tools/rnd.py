from configs._def_main_ import *

@rex('rnd')
async def start(client, msg):
    user_id = str(msg.from_user.id)
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Users WHERE id = ?", (user_id,))
    user_exists = cursor.fetchone()

    if user_exists:
        pais = msg.text[len('/rnd '):]
        if not pais:
            return await msg.reply('<b><code>.rnd mx</code> | Error rnd.</b>')

        req = requests.get(f'https://randomuser.me/api/?nat={pais}')

        if 'results' in req.text:
            r = req.json()['results'][0]
            genero = r['gender']
            mr = r['name']['title']
            first = r['name']['first']
            last = r['name']['last']
            mail = r['email']
            location = r['location']
            ciudad = location['city']
            state = location['state']
            country = location['country']
            zip = location['postcode']
            foto = r['picture']['large']
            ms1 = nrd.format(genero=genero,mr=mr,first=first,last=last,mail=mail,ciudad=ciudad,state=state,country=country,zip=zip,name=msg.from_user.first_name)
            await client.send_photo(msg.chat.id, foto, ms1)
        else:
            await msg.reply('Error de req')
    else:
        return await msg.reply_text(regist, disable_web_page_preview=True, reply_to_message_id=msg.id)

