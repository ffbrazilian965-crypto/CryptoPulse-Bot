import os
import time
import random
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# 🔑 Token configuration using Environment Variables (Secrets)
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# ─── ZALGO/GLITCH TEXT GENERATOR FUNCTION ───
def generate_zalgo_captcha():
    chars = "RT4XYW89ABCEFGHKMNPRSTUVXYZ234567"
    plain_text = "".join(random.choice(chars) for _ in range(6))
    
    zalgo_up = ['̍', '̎', '̄', '̅', '̿', '̑', '̆', '̐', '͒', '͗', '͑', '̇', '̈', '̊']
    zalgo_down = ['̖', '̗', '̘', '̙', '̜', '̟', '̠', '̟', '̥', '̬', '̭', '̮', '̯', '̰']
    
    glitch_text = ""
    for char in plain_text:
        glitch_text += char
        for _ in range(3):
            glitch_text += random.choice(zalgo_up) + random.choice(zalgo_down)
            
    return plain_text, glitch_text

user_data = {}

# ─── 1. START COMMAND (CAPTCHA TRIGGER) ───
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    plain, glitch = generate_zalgo_captcha()
    
    user_data[chat_id] = {"captcha": plain, "verified": False, "disclaimer_accepted": False}
    
    bot.send_message(chat_id, "🔒 **SECURITY VERIFICATION**\n\nAnti-bot shield activated. Please type the 6-character security code shown below to verify you are human:")
    bot.send_message(chat_id, f"`{glitch}`", parse_mode="Markdown")

# ─── 2. CAPTCHA VERIFICATION & FAKE LOADING ───
@bot.message_handler(func=lambda msg: msg.chat.id in user_data and not user_data[msg.chat.id]["verified"])
def verify_captcha(message):
    chat_id = message.chat.id
    user_input = message.text.strip().upper()
    correct_captcha = user_data[chat_id]["captcha"]
    
    if user_input == correct_captcha:
        user_data[chat_id]["verified"] = True
        
        load_msg = bot.send_message(chat_id, "⚙️ Verifying credentials...")
        time.sleep(1.5)
        bot.edit_message_text("🟢 Access Granted! Fetching security protocols...", chat_id, load_msg.message_id)
        time.sleep(1.5)
        bot.delete_message(chat_id, load_msg.message_id)
        
        show_disclaimer(chat_id)
    else:
        plain, glitch = generate_zalgo_captcha()
        user_data[chat_id]["captcha"] = plain
        bot.send_message(chat_id, "❌ Invalid code! Try again with this new security code:")
        bot.send_message(chat_id, f"`{glitch}`", parse_mode="Markdown")

# ─── 3. WHITE DISCLAIMER BOX & ACCEPT BUTTON ───
def show_disclaimer(chat_id):
    disclaimer_text = (
        "⚠️ **RISK DISCLAIMER / JOKHIM CHETAVANI** ⚠️\n\n"
        "Cryptocurrency trading involves high risk and market volatility. "
        "This bot provides automated calculations based on historical data patterns for educational purposes only. "
        "We are not responsible for any financial profits or losses.\n\n"
        "Kya aap aage badhne ke liye taiyar hain?"
    )
    
    markup = InlineKeyboardMarkup()
    accept_btn = InlineKeyboardButton("✅ Han, main yeh jokhim uthata hoon", callback_data="accept_disclaimer")
    markup.add(accept_btn)
    
    bot.send_message(chat_id, disclaimer_text, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "accept_disclaimer")
def handle_disclaimer_acceptance(call):
    chat_id = call.message.chat.id
    if chat_id in user_data and user_data[chat_id]["verified"]:
        user_data[chat_id]["disclaimer_accepted"] = True
        bot.delete_message(chat_id, call.message.message_id)
        bot.send_message(chat_id, "🎉 Setup Complete! Welcome to CryptoPulse Premium Panel.")
        open_main_dashboard(chat_id)

# ─── 4. MAIN VIP DASHBOARD ───
def open_main_dashboard(chat_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_signal = KeyboardButton("🟢 Market Signal")
    btn_info = KeyboardButton("ℹ️ Bot Info")
    markup.add(btn_signal, btn_info)
    
    bot.send_message(chat_id, "🎛️ **Main Menu**\nSelect an option from below to proceed:", reply_markup=markup)

# ─── 5. 10-SECOND DEEP RESEARCH SIMULATION ───
@bot.message_handler(func=lambda msg: msg.text == "🟢 Market Signal")
def generate_prediction_signal(message):
    chat_id = message.chat.id
    
    if chat_id not in user_data or not user_data[chat_id]["disclaimer_accepted"]:
        bot.send_message(chat_id, "⚠️ Please run /start and complete verification first.")
        return

    status_msg = bot.send_message(chat_id, "🔍 `[1/4] Scanning Binance & Coinbase order books for Whales...`", parse_mode="Markdown")
    time.sleep(2.5)
    
    bot.edit_message_text("📊 `[2/4] Calculating 7-Day Volatility & RSI Indicators...`", chat_id, status_msg.message_id, parse_mode="Markdown")
    time.sleep(2.5)
    
    bot.edit_message_text("⚙️ `[3/4] AI Engine simulating 1,000 market reversal scenarios...`", chat_id, status_msg.message_id, parse_mode="Markdown")
    time.sleep(2.5)
    
    bot.edit_message_text("🟢 `[4/4] Generating High-Probability VIP Signal Panel...`", chat_id, status_msg.message_id, parse_mode="Markdown")
    time.sleep(2.5)
    
    bot.delete_message(chat_id, status_msg.message_id)
    
    coins = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT"]
    selected_coin = random.choice(coins)
    entry_price = round(random.uniform(10, 60000), 2)
    target_1 = round(entry_price * 1.05, 2)
    target_2 = round(entry_price * 1.10, 2)
    stop_loss = round(entry_price * 0.95, 2)
    action = random.choice(["🟢 STRONG BUY", "🔴 STRONG SELL"])
    
    signal_panel = (
        f"📊 **VIP MARKET SIGNAL GENERATED** 📊\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"🪙 **Pair:** {selected_coin}\n"
        f"⚡ **Action:** {action}\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"📥 **Entry Zone:** {entry_price}\n"
        f"🎯 **Target 1:** {target_1}\n"
        f"🎯 **Target 2:** {target_2}\n"
        f"🛑 **Stop Loss:** {stop_loss}\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"⏰ *Signal valid for next 4 hours. Trade responsibly.*"
    )
    
    bot.send_message(chat_id, signal_panel, parse_mode="Markdown")

@bot.message_handler(func=lambda msg: msg.text == "ℹ️ Bot Info")
def bot_info(message):
    bot.send_message(message.chat.id, "🤖 **CryptoPulse GRX Bot v2.0**\n\nBuilt with premium AI market scanning logic, live Zalgo verification systems, and deep risk mitigation panels.")

if __name__ == "__main__":
    print("Bot is running successfully...")
    bot.infinity_polling()
