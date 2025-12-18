import os
from pyrogram import Client, filters
from pyromod import listen
from pyrogram.errors import (
    ApiIdInvalid, 
    PasswordHashInvalid, 
    PhoneCodeExpired, 
    PhoneCodeInvalid, 
    PhoneNumberInvalid, 
    SessionPasswordNeeded
)

# Environment Variables (Hosting ki settings mein ye naam dalne honge)
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client(
    "session_generator",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start") & filters.private)
async def start(bot, message):
    text = (
        "👋 Welcome! Main String Session nikalne wala bot hoon.\n\n"
        "Shuru karne ke liye niche diye gaye button ya command ka use karein:\n"
        "👉 /generate"
    )
    await message.reply_text(text)

@app.on_message(filters.command("generate") & filters.private)
async def generate_session(bot, message):
    user_id = message.chat.id
    
    # Step 1: Phone Number Lena
    phone_ask = await bot.ask(user_id, "📱 Apna **Phone Number** international format mein bhejein.\nExample: `+919876543210`", filters=filters.text)
    phone_number = phone_ask.text

    # Temporary Client Setup
    client = Client(":memory:", api_id=API_ID, api_hash=API_HASH)
    await client.connect()

    try:
        code_data = await client.send_code(phone_number)
    except Exception as e:
        await message.reply(f"❌ Error: {str(e)}")
        return

    # Step 2: OTP Lena
    otp_ask = await bot.ask(user_id, "📩 Aapke Telegram par ek code aaya hai.\nUise is tarah bhejein: `1 2 3 4 5` (Numbers ke beech space dein)", filters=filters.text)
    otp = otp_ask.text.replace(" ", "")

    try:
        await client.sign_in(phone_number, code_data.phone_code_hash, otp)
    except SessionPasswordNeeded:
        # Step 3: Agar 2FA On hai
        pwd_ask = await bot.ask(user_id, "🔐 Aapka **Two-Step Verification** on hai. Apna Password bhejein:", filters=filters.text)
        try:
            await client.check_password(pwd_ask.text)
        except Exception as e:
            await message.reply(f"❌ Password Galat Hai: {str(e)}")
            return
    except (PhoneCodeInvalid, PhoneCodeExpired):
        await message.reply("❌ OTP galat hai ya expire ho gaya hai.")
        return
    except Exception as e:
        await message.reply(f"❌ Kuch galat hua: {str(e)}")
        return

    # Final Step: Session Export Karna
    session_string = await client.export_session_string()
    
    final_text = (
        "✅ **String Session Successfully Ban Gaya Hai!**\n\n"
        f"`{session_string}`\n\n"
        "⚠️ **Warning:** Ise kabhi kisi ke saath share na karein. Isse aapka account hack ho sakta hai."
    )
    
    await bot.send_message(user_id, final_text)
    await client.disconnect()

print("Bot is running...")
app.run()
