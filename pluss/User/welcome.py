from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.new_chat_members)
async def welcome_message(client, message: Message):
    for new_member in message.new_chat_members:
        welcome_text = f"<b>Hey there {new_member.first_name} and welcome to {message.chat.title}! How are you?</b>"
        await message.reply_text(welcome_text)
