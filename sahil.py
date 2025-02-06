import telebot
import random
import os
from datetime import datetime, timedelta

# 🔐 Bot Token aur Owner/Admin ID (Owner: @offx_sahil)
BOT_TOKEN = '7446224442:AAFsFF_8Ojr_DsXKQa7JGJflvboWihgllK8'
OWNER_ID = 6512242172  # Owner hamesha approved rahega

# ✅ Approved Users Dictionary (User ID: Expiry Time)
approved_users = {OWNER_ID: None}

# 🚀 Bot Object Create Karna
sahil_bot = telebot.TeleBot(BOT_TOKEN)

# 📂 HEX File Generate Karne Ka Function
def generate_and_save_hex_file(total_size_kb, payload_type="hex"):
    total_size_bytes = total_size_kb * 1024
    file_path = "sahil.txt"

    if payload_type == "hex":
        random_sequence = bytes([random.randint(0, 255) for _ in range(total_size_bytes)])
        result_str = ''.join([f"{byte:02x}\\x" for byte in random_sequence])[:-2]  # Format: 7b\x26\x94\xda\x56\x6c

    elif payload_type == "decimal":
        result_str = ' '.join([str(random.randint(0, 255)) for _ in range(total_size_bytes)])

    elif payload_type.startswith("custom_hex"):
        prefix = payload_type.split("_")[-1]
        result_str = ' '.join([f"{prefix}" for _ in range(total_size_bytes // 2)])  # Format: /x91 /x91 /x91

    with open(file_path, "w") as file:
        file.write(result_str)

    return file_path, total_size_kb

# ✅ `/start` Command
@sahil_bot.message_handler(commands=['start'])
def start_message(message):
    if message.chat.id in approved_users:
        help_text = (
            "✅ **Admin Approve** 🔥\n\n"
            "ℹ️ **Commands List:**\n"
            "/generate - 📂 Random HEX file generate karega (1 KB - 10 MB).\n"
            "/generate 10kb hex - 📂 10 KB ka HEX file banayega.\n"
            "/generate 5mb decimal - 📂 5 MB ka Decimal file banayega.\n"
            "/generate 1mb /x91 - 📂 1MB file Custom HEX Prefix `/x91 /x91` ke sath banayega.\n"
            "/help - ℹ️ Commands ki list dikhaye.\n\n"
            "👑 **Owner:** @offx_sahil"
        )
        sahil_bot.send_message(message.chat.id, help_text, parse_mode="Markdown")
    else:
        sahil_bot.send_message(message.chat.id, "⛔ **Aap is bot ko use nahi kar sakte. Admin approval required.**")

# 📂 `/generate <size> <payload_type>` - File Generate Karega
@sahil_bot.message_handler(commands=['generate'])
def generate_file(message):
    if message.chat.id not in approved_users:
        sahil_bot.send_message(message.chat.id, "⛔ **Aap is bot ko use nahi kar sakte. Admin approval required.**")
        return
    try:
        parts = message.text.split()
        file_size_kb = 1024  # Default 1MB
        payload_type = "hex"

        if len(parts) >= 2:
            size_text = parts[1].lower()
            if "kb" in size_text:
                file_size_kb = int(size_text.replace("kb", ""))
            elif "mb" in size_text:
                file_size_kb = int(size_text.replace("mb", "")) * 1024
            else:
                sahil_bot.send_message(message.chat.id, "❌ **Invalid size format! Use: `/generate 10kb` or `/generate 2mb`**")
                return

        if len(parts) == 3:
            user_type = parts[2].lower()
            if user_type in ["hex", "decimal"]:
                payload_type = user_type
            elif user_type.startswith("/x") and len(user_type) == 4:
                payload_type = f"custom_hex_{user_type}"

        sahil_bot.send_message(message.chat.id, f"⏳ **{file_size_kb} KB ka `{payload_type}` payload generate ho raha hai...** 🔥")
        file_path, file_size = generate_and_save_hex_file(file_size_kb, payload_type)
        with open(file_path, "rb") as file:
            sahil_bot.send_document(message.chat.id, file)
        sahil_bot.send_message(message.chat.id, f"✅ **`sahil.txt` file `{payload_type}` format ke sath generate ho gayi!** 📂")
    except Exception:
        sahil_bot.send_message(message.chat.id, "❌ **Error: Invalid input! Use: `/generate 10kb hex` or `/generate 5mb /x91`**")

# ℹ️ `/help` Command
@sahil_bot.message_handler(commands=['help'])
def help_message(message):
    if message.chat.id in approved_users:
        help_text = (
            "🤖 **SahilBot Commands:**\n\n"
            "/generate - 📂 Random HEX file generate karega (1 KB - 10 MB).\n"
            "/generate 10kb hex - 📂 10 KB ka HEX file banayega.\n"
            "/generate 5mb decimal - 📂 5 MB ka Decimal file banayega.\n"
            "/generate 1mb /x91 - 📂 1MB file Custom HEX Prefix `/x91 /x91` ke sath banayega.\n"
            "/help - ℹ️ Commands ki list dikhaye.\n\n"
            "👑 **Owner:** @offx_sahil"
        )
        sahil_bot.send_message(message.chat.id, help_text, parse_mode="Markdown")

# 🔥 Bot Polling Start Karna
if __name__ == "__main__":
    sahil_bot.polling()
    