import os
from threading import Thread
from flask import Flask
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- Render Web Service Keep Alive Server ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is running online 24/7!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# --- বটের মূল তথ্য ---
BOT_TOKEN = "8606618808:AAG_cdOuE92VsGCOj-hkHGZE15bHPy2Gi9M"
CHANNEL_1 = "@A_Z_U_RA"

bot = telebot.TeleBot(BOT_TOKEN)

def is_user_joined(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_1, user_id)
        if member.status in ['creator', 'administrator', 'member']:
            return True
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def get_join_keyboard():
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("🐉 Join AZURA Channel", url=f"https://t.me/{CHANNEL_1.replace('@', '')}")
    btn2 = InlineKeyboardButton("✅ Joined / Check Now", callback_data="check_membership")
    markup.add(btn1)
    markup.add(btn2)
    return markup

SUCCESS_MESSAGE = (
    "🎉 স্বাগতম! আপনি আমাদের AZURA shop-এর একজন সদস্য 🎉\n\n"
    "🔴 নির্দেশনা :\n\n"
    "আপনার কাঙ্ক্ষিত কোর্সটি পেতে একটি মেসেজেই বিস্তারিত লিখে পাঠান। "
    "ছোট ছোট অনেকগুলো মেসেজ না পাঠিয়ে, একটি মেসেজেই সবকিছু গুছিয়ে বলার অনুরোধ রইল। "
    "এতে আমরা দ্রুত আপনার অর্ডারটি প্রসেস করতে পারব।\n\n"
    "👉🏻 কিভাবে লিখবেন? (Demo): \"আমি HSC/ssc 27/28 ব্যাচ। আমার ACS HSC 27 Biology Cycle 1 কোর্সটি প্রয়োজন।\""
)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if is_user_joined(user_id):
        bot.send_message(message.chat.id, SUCCESS_MESSAGE)
    else:
        bot.send_message(
            message.chat.id,
            "🌟 বটটি ব্যবহার করতে আপনাকে নিচের চ্যানেলে অবশ্যই জয়েন করতে হবে :\n\n"
            "👉🏻 জয়েন করা শেষ হলে নিচের Joined / Check Now বাটনে চাপ দিন :",
            reply_markup=get_join_keyboard()
        )

@bot.callback_query_handler(func=lambda call: call.data == "check_membership")
def verify_button(call):
    user_id = call.from_user.id
    bot.answer_callback_query(call.id)
    
    if is_user_joined(user_id):
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=SUCCESS_MESSAGE
        )
    else:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="❌ আপনি এখনো AZURA চ্যানেলে জয়েন করেননি! ❌\n\n"
                 "দয়া করে নিচের লিংকে গিয়ে চ্যানেলে জয়েন করুন, তারপর আবার 'Joined / Check Now' বাটনে ক্লিক করুন।",
            reply_markup=get_join_keyboard()
        )

if __name__ == '__main__':
    keep_alive()  # ২৪ ঘণ্টা ফ্রিতে চালু রাখার জন্য
    print("🤖 @AZU_RA_bot is running...")
    bot.infinity_polling()
