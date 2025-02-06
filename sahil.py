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
def generate_and_save_payload(payload_type, count, payload_value):
    if payload_type == "hex":
        # Hex Payload (\x091, \x092, etc. based on count)
        random_payload = ','.join([f'"\\x{payload_value}"' for i in range(count)])
    elif payload_type == "multi":
        # Multi Payload (xb0\x45\x5c\x74\x9d\xb4\xc8\xd9) format
        random_payload = f'"{payload_value}"'
    else:
        return None

    file_path = "sahil.txt"
    with open(file_path, "w") as file:
        file.write(random_payload)
    return file_path

# ✅ `/start` Command
@sahil_bot.message_handler(commands=['start'])
def start_message(message):
    if message.chat.id in approved_users:
        sahil_bot.send_message(message.chat.id, "✅ **Admin Approve** 🔥\nUse /help to view commands. 🌟")
    else:
        sahil_bot.send_message(message.chat.id, "⛔ **Aap is bot ko use nahi kar sakte. Admin approval required.** 🚫")

# 🛡️ `/add <id> <hour/day/week/month>` - User Approve Karne Ka Command
@sahil_bot.message_handler(commands=['add'])
def add_user(message):
    if message.chat.id != OWNER_ID:
        sahil_bot.send_message(message.chat.id, "❌ **Sirf Owner is command ka use kar sakta hai!** 🔒")
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
            sahil_bot.send_message(message.chat.id, "❌ **Invalid duration! Use: hour/day/week/month.** 🕒")
            return
        approved_users[user_id] = expiry_time
        sahil_bot.send_message(message.chat.id, f"✅ **User `{user_id}` approved till `{expiry_time}`.** 🎉")
    except Exception:
        sahil_bot.send_message(message.chat.id, "❌ **Invalid format! Use: `/add <id> <hour/day/week/month>`** ⚠️")

# 🚀 `/generate` - Payload Type Select Karne Ka Command
@sahil_bot.message_handler(commands=['generate'])
def generate_file(message):
    if message.chat.id not in approved_users:
        sahil_bot.send_message(message.chat.id, "⛔ **Aap is bot ko use nahi kar sakte. Admin approval required.** 🚫")
        return
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row('Hex', 'Multi')
    sahil_bot.send_message(message.chat.id, "🔄 **Select Payload Type:**\n1. **Hex**: \\"\\x091\\",\\"\\x091\\",\\"\\x091\\\"\n2. **Multi**: \"xb0\\x45\\x5c\\x74\\x9d\\xb4\\xc8\\xd9\"", reply_markup=markup)

    # Wait for user to choose Hex or Multi
    @sahil_bot.message_handler(func=lambda m: m.text in ['Hex', 'Multi'])
    def handle_payload_choice(message):
        payload_type = message.text.lower()
        sahil_bot.send_message(message.chat.id, f"⏳ **Generating {payload_type} Payload...** 💥")

        # Ask for number of payloads
        sahil_bot.send_message(message.chat.id, "📏 **Enter the number of payloads (e.g., 5, 10, 20, etc.):**")
        
        # Handle Number Input
        @sahil_bot.message_handler(func=lambda m: m.text.isdigit())
        def handle_number_input(message):
            count = int(message.text)
            if count <= 0:
                sahil_bot.send_message(message.chat.id, "❌ **Number must be greater than 0!** ⚠️")
                return

            # Ask for the payload value (e.g., "\x91", "\x51")
            sahil_bot.send_message(message.chat.id, "📏 **Enter the payload value (e.g., \\x91, \\x51):**")

            # Handle Payload Value Input
            @sahil_bot.message_handler(func=lambda m: m.text.startswith("\\x") and len(m.text) == 4)
            def handle_payload_value(message):
                payload_value = message.text.strip()

                # Generate Payload and save to file
                file_path = generate_and_save_payload(payload_type, count, payload_value)
                if file_path:
                    with open(file_path, "rb") as file:
                        sahil_bot.send_document(message.chat.id, file)
                    sahil_bot.send_message(message.chat.id, f"✅ **`sahil.txt` file with {payload_type} payload generated successfully!** 🎉📂")
                else:
                    sahil_bot.send_message(message.chat.id, "❌ **Error: Invalid payload type.** ⚠️")

# ℹ️ `/help` Command
@sahil_bot.message_handler(commands=['help'])
def help_message(message):
    if message.chat.id in approved_users:
        help_text = (
            "🤖 **SahilBot Commands:**\n\n"
            "/start - ✅ Admin Approve Message.\n"
            "/generate - 📂 Select payload type (Hex or Multi) and generate file.\n"
            "/help - ℹ️ Commands ki list dikhaye.\n"
            "/add <id> <hour/day/week/month> - ✅ User approve kare.\n"
            "/remove <id> - ❌ User ka access remove kare.\n"
        )
        sahil_bot.send_message(message.chat.id, help_text, parse_mode="Markdown")
    else:
        sahil_bot.send_message(message.chat.id, "⛔ **Aap is bot ko use nahi kar sakte. Admin approval required.** 🚫")

# 🔥 Bot Polling Start Karna
if __name__ == "__main__":
    sahil_bot.polling()
    