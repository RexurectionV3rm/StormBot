"""
Hello Developer!

This is an OpenSource project made by @scultura & @reversedns on Telegram!
Check out the channel on Telegram!
https://t.me/OpenSourceFFA

THE BOT IS NOT FINALIZED TO MALICIOUS USE.
WE DO NOT PARTAKE ANY ACTIONS THAT COULD BE DONE USING THIS BOT.

Thanks!
"""
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from pyrogram.errors import PhoneNumberInvalid, PhoneNumberFlood, PhoneNumberBanned, PhoneCodeInvalid, UserDeactivatedBan, SessionPasswordNeeded
from pyromod import *
import db

API_HASH = "0" # YOUR API_HASH
API_ID = 0 # YOUR API_ID
TOKEN = "0" # YOUR BOT_TOKEN

add = [] # DON'T CHANGE IF YOU DO NOT KNOW WHAT YOU'RE DOING!
code = [] # DON'T CHANGE IF YOU DO NOT KNOW WHAT YOU'RE DOING!
clns = [] # DON'T CHANGE IF YOU DO NOT KNOW WHAT YOU'RE DOING!
number = None # DON'T CHANGE IF YOU DO NOT KNOW WHAT YOU'RE DOING!
sent = None # DON'T CHANGE IF YOU DO NOT KNOW WHAT YOU'RE DOING!
chat = None # DON'T CHANGE IF YOU DO NOT KNOW WHAT YOU'RE DOING!

bot = Client("bot",api_id=API_ID,api_hash=API_HASH,bot_token=TOKEN, in_memory=True)
tempcln = Client("session",api_id=API_ID,api_hash=API_HASH, in_memory=True)
db.initialize_db() # DON'T CHANGE IF YOU DO NOT KNOW WHAT YOU'RE DOING!
 
def remove(id):
    for i in [add, code]:
        try:
            i.remove(id)
        except: pass

#### reply markup buttons
storm_bot_start = InlineKeyboardMarkup([[InlineKeyboardButton("✅ STORM", "storm")], [InlineKeyboardButton("➕ ADD", "add"), InlineKeyboardButton("➖ REMOVE","remove")],[InlineKeyboardButton("OPEN SOURCE", url="https://github.com/")]])
back = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 BACK", "back")]])

@bot.on_message(filters.private & filters.command("start"))
async def start(cl, msg):
    await msg.reply(f"**Hello {msg.from_user.mention}!** Welcome to the StormBot!__\nThe bot is not finalized in malicious ways!", reply_markup=storm_bot_start)
    remove(msg.from_user.id)

@bot.on_message(filters.private)
async def msg(client, msg):
    user_id = msg.from_user.id
    if user_id in add:
        if db.uniform_number(msg.text) in db.get_number():
            await msg.reply("❌ VoIP già aggiunto")
            remove(user_id)
        else:
            global number
            await tempcln.connect()
            number = msg.text
            try:
                global sent
                sent = await tempcln.send_code(number)
                await msg.reply("**✅ If the username is valid, you received a code, send it here.**")
                add.remove(user_id)
                code.append(user_id)
            except PhoneNumberInvalid:
                await msg.reply("🔢Invalid number!\n**💡Remember: Numbers must already have a Telegram account created!**", reply_markup = back)
                try: await tempcln.disconnect() 
                except Exception as e: print(e)
            except PhoneNumberFlood:
                await msg.reply("⌛**!Number in flood!**\n➰Try again soon!",  reply_markup = back)
                try: await tempcln.disconnect() 
                except Exception as e: print(e)
            except PhoneNumberBanned:
                await msg.reply("⛔Number banned by Telegram!",  reply_markup = back)
                try: await tempcln.disconnect() 
                except Exception as e: print(e)
            
            except Exception as e: 
                await msg.reply("⛔Error!")
                try: await tempcln.disconnect() 
                except Exception as e: print(e)
                print(e)
    elif user_id in code:
        try:
            await tempcln.sign_in(number, sent.phone_code_hash, msg.text)
            ss = await tempcln.export_session_string()
            db.add(number, ss)
            await msg.reply(f"**✅Account successfully logged in!**")
            remove(user_id)
            try: await tempcln.disconnect() 
            except Exception as e: print(e)
        except SessionPasswordNeeded:
            await tempcln.check_password((await client.ask(msg.from_user.id, "🔑Send 2-steps password")).text)
            ss = await tempcln.export_session_string()
            db.add(number, ss)
            await msg.reply(f"**✅Account successfully logged in!**")
            remove(user_id)
            try: await tempcln.disconnect() 
            except Exception as e: print(e)
        except PhoneCodeInvalid:
            await msg.reply("⛔Incorrect code, try again!",  reply_markup = back)
        except Exception as e: 
            await msg.reply("⛔Error!")
            print(e)

# CREATE INLINE KEYBOARD FOR PHONE NUMBERS
def crea_kb_inline(sessioni):
    keyboard = []
    for num in sessioni:
        btn = InlineKeyboardButton(text=num, callback_data=num)
        keyboard.append([btn])
    keyboard.append([InlineKeyboardButton("🔙 BACK", "back")])
    inline_kb = InlineKeyboardMarkup(keyboard)
    return inline_kb


#CALL BACK HANDLER
@bot.on_callback_query()
async def callb(cl, cb):
    chat_id = cb.message.chat.id
    await cb.answer("✅")
    if cb.data == "add":
        await cb.message.edit("📞 Please provide the phone number of the user you want to log in: ", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 BACK", "back")]]))
        add.append(chat_id)  
    if cb.data == "remove":
        list_accounts = crea_kb_inline(sessioni=db.get_number())
        if not list_accounts.inline_keyboard:
            await cb.message.edit(f"❌ You have no VoIPs connected!", reply_markup=back)
        else:
            await cb.message.edit(f"📱 Please, select one of the phone numbers in the inline keyboard list.\n\n Total VoIPs: <code>{len(db.get_number())}</code>", reply_markup = list_accounts)    
    elif cb.data == "back":
        await cb.message.edit(f"**Hello {cb.from_user.mention}!** Welcome to the StormBot!__\nThe bot is not finalized in malicious ways!", reply_markup=storm_bot_start)
        remove(cb.from_user.id)
    elif cb.data == "storm":
        grupporaw = await cl.ask(cb.from_user.id, "❓ Which group do you want to storm?")
        gruppo = grupporaw.text
        msg_stormraw = await cl.ask(cb.from_user.id, "❓ What message do you want to use for the storm?")
        amount_raw = await cl.ask(cb.from_user.id, "❓ How many messages for each VoIP?")
        amount = int(amount_raw.text)
        msg_storm = msg_stormraw.text
        await cb.message.reply(f"<code>⛈...</code>")
        for i in db.get_session():
            try:
                cln = Client("temp", session_string=i)
                await cln.start()
                clns.append(cln)
            except UserDeactivatedBan:
                db.banned_user(i)
        for x in clns:
            try:
                await x.join_chat(gruppo)
            except Exception as e: print(e)
        try:
            global chat
            chat = await clns[0].get_chat(gruppo)
        except Exception as e: print(e)
        for y in range(amount):
            for i in clns:
                try:
                    await i.send_message(chat.id, msg_storm)
                except Exception as e: print(e)
        for i in clns:
            try:
                await i.stop()
            except Exception as e: print(e)
        clns.clear()
    if cb.data in db.get_number():
        num = cb.data
        db.remove(num)
        await cb.message.reply(f"✅ VoIP <code>{num}</code> removed!", )
    
        
bot.run()