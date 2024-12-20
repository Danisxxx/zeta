from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data import rex

Client.parse_mode = 'html'

@rex(['myspam'])
async def myspam(client, msg):
    text = """<b><i>[後](t.me/Exzzex) 𝘼𝙇𝙋𝙃𝘼 𝘾𝙃𝙀𝙆𝙀𝙍 𝘽𝙊𝙏</i></b>

<b><i>[後](t.me/Exzzex) Planes Disponibles:</i></b>
• <b><i>$5.00 USD - 15 Días + 300 Créditos</i></b>  
• <b><i>$9.00 USD - 30 Días + 750 Créditos</i></b>  
• <b><i>$15.00 USD - 40 Días + 1150 Créditos</i></b>  
• <b><i>$20.00 USD - 45 Días + Créditos ILIMITADOS</i></b>  
• <b><i>$300.00 USD - ILIMITADO + CRÉDITOS ILIMITADOS</i></b>

<b><i>[後](t.me/Exzzex) Plan de por vida (por tiempo ilimitado Días y Créditos):</i></b>  
• <b><i>Acceso ilimitado a días y créditos.</i></b>  
• <b><i>Posibilidad de pedir 15 Keys de 7 días por mes.</i></b>

<b><i>[後](t.me/Exzzex) Beneficios incluidos en todos los planes:</i></b>  
• <b><i>Premium Scrapper</i></b>  
• <b><i>Grupo privado</i></b>  
• <b><i>Asistencia 24/7</i></b>  
• <b><i>Te Puedo Ayudar A Calar o A Sacar Live</i></b>  
• <b><i>Lista De Pasarelas ⚠️</i></b>

<b><i>[後](t.me/Exzzex) Vendedor [✅]</i></b>  
<b><i>[後](t.me/Exzzex) @Exzzex » [7202754124]</i></b>

<b><i>[後](t.me/Exzzex) Aprovecha la oportunidad de obtener los beneficios que yo ofrezco y los beneficios que ofrece el bot.</i></b>
"""

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Referencias", url="https://t.me/xFouns"),
                InlineKeyboardButton("Métodos de Pago", url="https://t.me/AlphaChks/12"),
            ]
        ]
    )

    await msg.reply(
        f"<a href='https://imgur.com/B1ds3U1.jpg'>&#8203;</a> {text}",
        reply_markup=buttons,
        reply_to_message_id=msg.id
    )
