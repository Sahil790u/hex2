import telebot
import random
import os
from datetime import datetime, timedelta

# 🔐 Bot Token aur Owner/Admin ID (Owner: @offx_sahil)
BOT_TOKEN = '7226582576:AAG1tAiH-OaqQmedlsb4ZPtgJ1653qWkHCk'
OWNER_ID = 6512242172  # Owner hamesha approved rahega

# ✅ Approved Users Dictionary (User ID: Expiry Time)
approved_users = {OWNER_ID: None}

# 🚀 Bot Object Create Karna
sahil_bot = telebot.TeleBot(BOT_TOKEN)

# 📂 Custom Payload Generate Function
def generate_and_save_payload(payload_type, count, payload_value):
    if payload_type == "hex":
        # Generate payload like: "\x91", "\x91", "\x91", ...
        random_payload = ','.join([f'"{payload_value}"' for _ in range(count)])
    elif payload_type == "multi":
        # Generate multi payload in a fixed format; here we use the provided payload_value.
        random_payload = f'"{payload_value}"'
    else:
        return None

    file_path = "sahil.txt"
    with open(file_path, "w") as file:
        file.write(random_payload)
    return file_path

# ✅ `/start` Command (Automatically sends help message)
@sahil_bot.message_handler(commands=['start'])
def start_message(message):
    if message.chat.id in approved_users:
        # Send Admin approval message and then help text
        start_text = ("✅ <b>Admin Approve</b> 🔥\n\n"
                      "ℹ️ <b>SahilBot Commands:</b>\n"
                      "/generate - Select payload type (Hex or Multi) and generate file.\n"
                      "/add <id> <hour/day/week/month> - Approve a user (Owner only).\n"
                      "/remove <id> - Remove a user's access (Owner only).\n"
                      "/clearlogs - Clear logs (Owner only).\n"
                      "/time - Show current time.\n"
                      "/help - Show this command list.\n")
        sahil_bot.send_message(message.chat.id, start_text, parse_mode="HTML")
    else:
        sahil_bot.send_message(message.chat.id, "⛔ <b>Aap is bot ko use nahi kar sakte. Admin approval required.</b> 🚫", parse_mode="HTML")

# 🛡️ `/add <id> <hour/day/week/month>` Command
@sahil_bot.message_handler(commands=['add'])
def add_user(message):
    if message.chat.id != OWNER_ID:
        sahil_bot.send_message(message.chat.id, "❌ <b>Sirf Owner is command ka use kar sakta hai!</b> 🔒", parse_mode="HTML")
        return
    try:
        parts = message.text.split()
        user_id = int(parts[1])
        duration = parts[2].lower()
        if "hour" in duration:
            expiry_time = datetime.now() + timedelta(hours=int(duration.replace("hour", "")))
        elif "day" in duration:
            expiry_time = datetime.now() + timedelta(days=int(duration.replace("day", "")))
        elif "week" in duration:
            expiry_time = datetime.now() + timedelta(weeks=int(duration.replace("week", "")))
        elif "month" in duration:
            expiry_time = datetime.now() + timedelta(days=int(duration.replace("month", "")) * 30)
        else:
            sahil_bot.send_message(message.chat.id, "❌ <b>Invalid duration!</b> Use: hour/day/week/month.", parse_mode="HTML")
            return
        approved_users[user_id] = expiry_time
        sahil_bot.send_message(message.chat.id, f"✅ <b>User {user_id} approved till {expiry_time}.</b> 🎉", parse_mode="HTML")
    except Exception:
        sahil_bot.send_message(message.chat.id, "❌ <b>Invalid format!</b> Use: /add <id> <hour/day/week/month>", parse_mode="HTML")

# 🚀 `/remove <id>` Command
@sahil_bot.message_handler(commands=['remove'])
def remove_user(message):
    if message.chat.id != OWNER_ID:
        sahil_bot.send_message(message.chat.id, "❌ <b>Sirf Owner is command ka use kar sakta hai!</b> 🔒", parse_mode="HTML")
        return
    try:
        user_id = int(message.text.split()[1])
        if user_id in approved_users:
            del approved_users[user_id]
            sahil_bot.send_message(message.chat.id, f"✅ <b>User {user_id} ka access remove kar diya gaya hai.</b>", parse_mode="HTML")
        else:
            sahil_bot.send_message(message.chat.id, "❌ <b>User already removed ya exist nahi karta!</b>", parse_mode="HTML")
    except Exception:
        sahil_bot.send_message(message.chat.id, "❌ <b>Invalid format!</b> Use: /remove <id>", parse_mode="HTML")

# 🚀 `/generate` Command (Select payload type and generate file)
@sahil_bot.message_handler(commands=['generate'])
def generate_file(message):
    if message.chat.id not in approved_users:
        sahil_bot.send_message(message.chat.id, "⛔ <b>Aap is bot ko use nahi kar sakte. Admin approval required.</b> 🚫", parse_mode="HTML")
        return
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row('Hex', 'Multi')
    prompt = ("🔄 <b>Select Payload Type:</b>\n"
              "1. <b>Hex</b>: \"\\x91\",\"\\x91\",\"\\x91\"\n"
              "2. <b>Multi</b>: \"xb0\\x45\\x5c\\x74\\x9d\\xb4\\xc8\\xd9\"")
    sahil_bot.send_message(message.chat.id, prompt, reply_markup=markup, parse_mode="HTML")

    @sahil_bot.message_handler(func=lambda m: m.text in ['Hex', 'Multi'])
    def handle_payload_choice(message):
        payload_type = message.text.lower()
        sahil_bot.send_message(message.chat.id, f"⏳ <b>Generating {payload_type} Payload...</b> 💥", parse_mode="HTML")
        sahil_bot.send_message(message.chat.id, "📏 <b>Enter the number of payloads (e.g., 5, 10, 20):</b>", parse_mode="HTML")
        
        @sahil_bot.message_handler(func=lambda m: m.text.isdigit())
        def handle_number_input(message):
            count = int(message.text)
            if count <= 0:
                sahil_bot.send_message(message.chat.id, "❌ <b>Number must be greater than 0!</b> ⚠️", parse_mode="HTML")
                return
            sahil_bot.send_message(message.chat.id, "📏 <b>Enter the payload value (e.g., \\x91, \\x51):</b>", parse_mode="HTML")
            
            @sahil_bot.message_handler(func=lambda m: m.text.startswith("\\x") and len(m.text.strip()) == 4)
            def handle_payload_value(message):
                payload_value = message.text.strip()
                file_path = generate_and_save_payload(payload_type, count, payload_value)
                if file_path:
                    with open(file_path, "rb") as file:
                        sahil_bot.send_document(message.chat.id, file)
                    sahil_bot.send_message(message.chat.id, f"✅ <b>sahil.txt</b> file with {payload_type} payload generated successfully! 🎉📂", parse_mode="HTML")
                else:
                    sahil_bot.send_message(message.chat.id, "❌ <b>Error: Invalid payload type.</b> ⚠️", parse_mode="HTML")
    
# ℹ️ `/help` Command
@sahil_bot.message_handler(commands=['help'])
def help_message(message):
    if message.chat.id in approved_users:
        help_text = (
            "🤖 <b>SahilBot Commands:</b>\n\n"
            "<b>/start</b> - ✅ Admin Approve Message + Help text.\n"
            "<b>/generate</b> - 📂 Select payload type (Hex or Multi) and generate file.\n"
            "<b>/add &lt;id&gt; &lt;hour/day/week/month&gt;</b> - ✅ Approve a user (Owner only).\n"
            "<b>/remove &lt;id&gt;</b> - ❌ Remove a user's access (Owner only).\n"
            "<b>/clearlogs</b> - 🗑️ Clear logs (Owner only).\n"
            "<b>/time</b> - 🕒 Show current time.\n"
            "<b>/help</b> - ℹ️ Show this command list.\n"
        )
        sahil_bot.send_message(message.chat.id, help_text, parse_mode="HTML")
    else:
        sahil_bot.send_message(message.chat.id, "⛔ <b>Aap is bot ko use nahi kar sakte. Admin approval required.</b> 🚫", parse_mode="HTML")

# 🔥 Bot Polling Start Karna
if __name__ == "__main__":
    sahil_bot.polling()
    