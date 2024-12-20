from pyrogram import Client,filters
from gotas.chattext import *
from gotas.botones import *
from gotas.claim.errorclaim import *
from gotas.id.textid import *
from pyrogram import *
from datetime import datetime
import os, requests,re,time
from configs.configsBot import *
from configs.defccs import *
from _mainConten_ import *
from pluss.Func import connect_to_db, connect_to_roles_db

def rex(bit):
    nix = Client.on_message(filters.command(bit, ["/", ".", ",","-","$","%"]))
    return nix

def rexbt(bor):
    nox = Client.on_callback_query(filters.regex(bor))
    return nox

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Main : The Worlds Of Apis ( max )')

def dia():
    if datetime.now().hour < 12:return "Buenos dias ⛅️"
    elif datetime.now().hour >= 11 and datetime.now().hour < 16:return "Buenas Tades ☀️"
    elif datetime.now().hour >= 17 and datetime.now().hour < 19:return "Buenas Nochesitas 🌅"
    elif datetime.now().hour >= 19 and datetime.now().hour < 24:return "Buenas Noche 🌃 "
    else:return "Unos Buenos dias ⛅️"

def conta(call):
    if call == 'apid':
        return apid
    elif call == 'hasd':
        return apihasd
    else:
        return token 


usertime = {}
timetake = 30
def atspam(func):
    async def wrapper(client, message):
        user_id = message.from_user.id
        if 5416957433 in usertime and time.time() - usertime[user_id] < timetake:
            await func(client, message)
            usertime[user_id] = time.time()
            return
        elif user_id in usertime and time.time() - usertime[user_id] < timetake:
            wait_time = int(timetake - (time.time() - usertime[user_id]))
            await message.reply(f"<b>[•] Contro de spam await <code>{wait_time} sg.</code> </b>")
            return
        else:
            await func(client, message)
            usertime[user_id] = time.time()

    return wrapper