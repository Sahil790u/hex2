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

# 📂 HEX File Generate Karne Ka Function (Random Payload Har Baar)
def generate_and_save_hex_file(total_size_kb):
    total_size_bytes = total_size_kb * 1024  
    random_sequence = bytes([random.randint(0, 255) for _ in range(total_size_bytes)])
    result_str = ''.join([f"\\x{byte:02x}" for byte in random_sequence])
    file_path = "sahil.txt"
    with open(file_path, "w") as file:
        file.write(result_str)
    return file_path, total_size_kb

# ✅ `/start` Command
@sahil_bot.message_handler(commands=['start'])
def start_message(message):
    if message.chat.id in approved_users:
        sahil_bot.send_message(message.chat.id, "✅ **Admin Approve** 🔥\n\nType /help for available commands.")
    else:
        sahil_bot.send_message(message.chat.id, "⛔ **Aap is bot ko use nahi kar sakte. Admin approval required.**")

# 🛡️ `/add <id> <hour/day/week/month>` - User Approve Karne Ka Command
@sahil_bot.message_handler(commands=['add'])
def add_user(message):
    if message.chat.id != OWNER_ID:
        sahil_bot.send_message(message.chat.id, "❌ **Sirf Owner is command ka use kar sakta hai!**")
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
            sahil_bot.send_message(message.chat.id, "❌ **Invalid duration! Use: hour/day/week/month.**")
            return
        approved_users[user_id] = expiry_time
        sahil_bot.send_message(message.chat.id, f"✅ **User `{user_id}` approved till `{expiry_time}`.** 🔥")
    except Exception:
        sahil_bot.send_message(message.chat.id, "❌ **Invalid format! Use: `/add <id> <hour/day/week/month>`**")

# 🚀 `/remove <id>` - Kisi User Ka Access Remove Karne Ka Command
@sahil_bot.message_handler(commands=['remove'])
def remove_user(message):
    if message.chat.id != OWNER_ID:
        sahil_bot.send_message(message.chat.id, "❌ **Sirf Owner is command ka use kar sakta hai!**")
        return
    try:
        user_id = int(message.text.split()[1])
        if user_id in approved_users:
            del approved_users[user_id]
            sahil_bot.send_message(message.chat.id, f"✅ **User `{user_id}` ka access remove kar diya gaya hai.**")
        else:
            sahil_bot.send_message(message.chat.id, "❌ **User already removed ya exist nahi karta!**")
    except Exception:
        sahil_bot.send_message(message.chat.id, "❌ **Invalid format! Use: `/remove <id>`**")

# 📂 `/generate <size>` - Specific Size Ka File Generate Karega
@sahil_bot.message_handler(commands=['generate'])
def generate_file(message):
    if message.chat.id not in approved_users:
        sahil_bot.send_message(message.chat.id, "⛔ **Aap is bot ko use nahi kar sakte. Admin approval required.**")
        return
    try:
        parts = message.text.split()
        if len(parts) == 1:
            file_size_kb = random.randint(1, 10240)  
        else:
            size_text = parts[1].lower()
            if "kb" in size_text:
                file_size_kb = int(size_text.replace("kb", ""))
            elif "mb" in size_text:
                file_size_kb = int(size_text.replace("mb", "")) * 1024
            else:
                sahil_bot.send_message(message.chat.id, "❌ **Invalid size format! Use: `/generate 10kb` or `/generate 2mb`**")
                return
        sahil_bot.send_message(message.chat.id, f"⏳ **{file_size_kb} KB ka HEX payload generate ho raha hai...** 🔥")
        file_path, file_size = generate_and_save_hex_file(file_size_kb)
        with open(file_path, "rb") as file:
            sahil_bot.send_document(message.chat.id, file)
        sahil_bot.send_message(message.chat.id, f"✅ **`sahil.txt` file {file_size} KB size ke sath generate ho gayi!** 📂")
    except Exception:
        sahil_bot.send_message(message.chat.id, "❌ **Error: Invalid input! Use: `/generate 10kb` or `/generate 2mb`**")

# 🗑️ `/clearlogs` - `sahil.txt` File Delete Karne Ka Command
@sahil_bot.message_handler(commands=['clearlogs'])
def clear_logs(message):
    if message.chat.id != OWNER_ID:
        sahil_bot.send_message(message.chat.id, "❌ **Sirf Owner is command ka use kar sakta hai!**")
        return
    try:
        if os.path.exists("sahil.txt"):
            os.remove("sahil.txt")
            sahil_bot.send_message(message.chat.id, "✅ **Logs (sahil.txt) clear kar diye gaye hain!** 🗑️")
        else:
            sahil_bot.send_message(message.chat.id, "❌ **Logs file exist nahi karti!**")
    except Exception:
        sahil_bot.send_message(message.chat.id, "❌ **Error: Logs delete nahi ho sake!**")

# 🕒 `/time` Command
@sahil_bot.message_handler(commands=['time'])
def time_message(message):
    if message.chat.id in approved_users:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sahil_bot.send_message(message.chat.id, f"🕒 **Current Time: `{current_time}`**")
    else:
        sahil_bot.send_message(message.chat.id, "⛔ **Aap is bot ko use nahi kar sakte. Admin approval required.**")

# ℹ️ `/help` Command
@sahil_bot.message_handler(commands=['help'])
def help_message(message):
    if message.chat.id in approved_users:
        help_text = (
            "🤖 **SahilBot Commands:**\n\n"
            "/start - ✅ Admin Approve Message.\n"
            "/generate - 📂 Random HEX file generate karega (1 KB - 10 MB).\n"
            "/generate 10kb - 📂 10 KB ka HEX file banayega.\n"
            "/generate 5mb - 📂 5 MB ka HEX file banayega.\n"
            "/clearlogs - 🗑️ `sahil.txt` logs clear karega. (Owner Only)\n"
            "/time - 🕒 Current time dikhaye.\n"
            "/help - ℹ️ Commands ki list dikhaye.\n\n"
            "👑 **Owner Commands:**\n"
            "/add <id> <hour/day/week/month> - ✅ User approve kare.\n"
            "/remove <id> - ❌ User ka access remove kare.\n"
        )
        sahil_bot.send_message(message.chat.id, help_text, parse_mode="Markdown")

# 🔥 Bot Polling Start Karna
if __name__ == "__main__":
    sahil_bot.polling()
    