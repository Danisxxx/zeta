from configs._def_main_ import *
import re
import requests

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

@rex(['btc'])
async def send_message(client, msg):
    if await is_banned(msg.from_user.id):
        await msg.reply_text(banned, disable_web_page_preview=True, reply_to_message_id=msg.id)
        return

    if not await is_registered(msg.from_user.id):
        await msg.reply_text(regist, disable_web_page_preview=True, reply_to_message_id=msg.id)
        return

    text = msg.text.split(" ", 2)
    if len(text) < 3 or not re.match(r"^\d+(\.\d+)?\$$", text[1]):
        await msg.reply("""
<b>BTC Currency [⛈]
Format: <code>$btc {moneda}</code></b>""")
        return

    amount = float(text[1][:-1])
    command = text[2].lower()

    response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
    if response.status_code != 200:
        await msg.reply("No se pudo obtener la tasa de cambio. Intenta más tarde.")
        return

    data = response.json()

    monedas = {
        "dolar": "MXN", "arg": "ARS", "bol": "VES", "eur": "EUR", "col": "COP", 
        "per": "PEN", "bra": "BRL", "chi": "CLP", "ecu": "USD", "uru": "UYU", 
        "gtq": "GTQ", "pyg": "PYG", "dom": "DOP", "nio": "NIO", "pab": "PAB"
    }

    if command not in monedas:
        await msg.reply("Comando no válido. Usa: dolar, arg, bol, eur, col, per, bra, chi, ecu, uru, gtq, pyg, dom, nio, pab.", reply_to_message_id=msg.id)
        return

    tasa = data["rates"].get(monedas[command], 0)
    if tasa == 0:
        await msg.reply(f"No se encontró información para la conversión a {command.upper()}.", reply_to_message_id=msg.id)
        return

    converted_amount = round(amount * tasa, 2)

    amount_str = f"{int(amount) if amount.is_integer() else amount:.2f}".rstrip(".0")
    converted_amount_str = f"{int(converted_amount) if converted_amount.is_integer() else converted_amount:.2f}".rstrip(".0")

    if command == "dolar": msg1 = dolar.format(dolar=amount_str, pesos_mexicanos=converted_amount_str)
    elif command == "arg": msg1 = arg.format(dolar=amount_str, pesos_argentinos=converted_amount_str)
    elif command == "bol": msg1 = bol.format(dolar=amount_str, bolivares_venezolanos=converted_amount_str)
    elif command == "eur": msg1 = eur.format(dolar=amount_str, euros=converted_amount_str)
    elif command == "col": msg1 = col.format(dolar=amount_str, pesos_colombianos=converted_amount_str)
    elif command == "per": msg1 = per.format(dolar=amount_str, sol_peruano=converted_amount_str)
    elif command == "bra": msg1 = bra.format(dolar=amount_str, reales_brasilenos=converted_amount_str)
    elif command == "chi": msg1 = chi.format(dolar=amount_str, pesos_chilenos=converted_amount_str)
    elif command == "ecu": msg1 = ecu.format(dolar=amount_str, dolares_ecuadorianos=converted_amount_str)
    elif command == "uru": msg1 = uru.format(dolar=amount_str, pesos_uruguayos=converted_amount_str)
    elif command == "gtq": msg1 = gtq.format(dolar=amount_str, quetzales_guatemaltecos=converted_amount_str)
    elif command == "pyg": msg1 = pyg.format(dolar=amount_str, guaranies_paraguayos=converted_amount_str)
    elif command == "dom": msg1 = dom.format(dolar=amount_str, pesos_dominicanos=converted_amount_str)
    elif command == "nio": msg1 = nio.format(dolar=amount_str, cordobas_nicaraguenses=converted_amount_str)
    elif command == "pab": msg1 = pab.format(dolar=amount_str, balboas_panamenas=converted_amount_str)

    await msg.reply(msg1, reply_markup=link, reply_to_message_id=msg.id)
