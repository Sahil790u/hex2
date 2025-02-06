import telebot
import os
from datetime import datetime, timedelta

# 🔐 Bot Token and Owner/Admin ID (Owner: @offx_sahil)
BOT_TOKEN = '7226582576:AAG1tAiH-OaqQmedlsb4ZPtgJ1653qWkHCk'
OWNER_ID = 6512242172  # Owner always approved

# ✅ Approved Users Dictionary (user id: expiry time)
approved_users = {OWNER_ID: None}

# 🚀 Create the bot instance
sahil_bot = telebot.TeleBot(BOT_TOKEN)

# ------------------------------------------------------------------------------
# Function to generate payload and save to file "sahil.txt"
def generate_and_save_payload(payload_type, count, payload_value=None):
    """
    For 'hex': generates a string like:
       "<payload_value>", "<payload_value>", "<payload_value>"
    For 'multi': uses a fixed pattern.
    """
    if payload_type == "hex":
        if not payload_value:
            return None
        # Create a comma-separated list of quoted payload values
        generated = ', '.join([f'"{payload_value}"' for _ in range(count)])
    elif payload_type == "multi":
        fixed_pattern = "xb0\\x45\\x5c\\x74\\x9d\\xb4\\xc8\\xd9"
        # Repeat the fixed pattern 'count' times, separated by a space
        generated = ' '.join([fixed_pattern for _ in range(count)])
    else:
        return None

    file_path = "sahil.txt"
    with open(file_path, "w") as f:
        f.write(generated)
    return file_path

# ------------------------------------------------------------------------------
# /start Command – Sends admin approval message plus help text automatically.
@sahil_bot.message_handler(commands=['start'])
def start_message(message):
    if message.chat.id in approved_users:
        start_text = (
            "✅ <b>Admin Approve</b> 🔥<br><br>"
            "ℹ️ <b>SahilBot Commands:</b><br>"
            "<b>/generate</b> - Select payload type (Multi or Hex) and generate file.<br>"
            "<b>/add &lt;id&gt; &lt;hour/day/week/month&gt;</b> - Approve a user (Owner only).<br>"
            "<b>/remove &lt;id&gt;</b> - Remove a user's access (Owner only).<br>"
            "<b>/clearlogs</b> - Clear logs (Owner only).<br>"
            "<b>/time</b> - Show current time.<br>"
            "<b>/help</b> - Show this command list.<br>"
        )
        sahil_bot.send_message(message.chat.id, start_text, parse_mode="HTML")
    else:
        sahil_bot.send_message(
            message.chat.id,
            "⛔ <b>Aap is bot ko use nahi kar sakte. Admin approval required.</b> 🚫",
            parse_mode="HTML"
        )

# ------------------------------------------------------------------------------
# /help Command – Displays the list of available commands.
@sahil_bot.message_handler(commands=['help'])
def help_message(message):
    if message.chat.id in approved_users:
        help_text = (
            "🤖 <b>SahilBot Commands:</b><br><br>"
            "<b>/start</b> - Admin Approve Message + Help text.<br>"
            "<b>/generate</b> - Select payload type (Multi or Hex) and generate file.<br>"
            "<b>/add &lt;id&gt; &lt;hour/day/week/month&gt;</b> - Approve a user (Owner only).<br>"
            "<b>/remove &lt;id&gt;</b> - Remove a user's access (Owner only).<br>"
            "<b>/clearlogs</b> - Clear logs (Owner only).<br>"
            "<b>/time</b> - Show current time.<br>"
            "<b>/help</b> - Show this command list.<br>"
        )
        sahil_bot.send_message(message.chat.id, help_text, parse_mode="HTML")
    else:
        sahil_bot.send_message(
            message.chat.id,
            "⛔ <b>Aap is bot ko use nahi kar sakte. Admin approval required.</b> 🚫",
            parse_mode="HTML"
        )

# ------------------------------------------------------------------------------
# /add Command – Approve a user (Owner only).
@sahil_bot.message_handler(commands=['add'])
def add_user(message):
    if message.chat.id != OWNER_ID:
        sahil_bot.send_message(
            message.chat.id,
            "❌ <b>Sirf Owner is command ka use kar sakta hai!</b> 🔒",
            parse_mode="HTML"
        )
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
            sahil_bot.send_message(
                message.chat.id,
                "❌ <b>Invalid duration!</b> Use: hour/day/week/month.",
                parse_mode="HTML"
            )
            return
        approved_users[user_id] = expiry_time
        sahil_bot.send_message(
            message.chat.id,
            f"✅ <b>User {user_id} approved till {expiry_time}.</b> 🎉",
            parse_mode="HTML"
        )
    except Exception:
        sahil_bot.send_message(
            message.chat.id,
            "❌ <b>Invalid format!</b> Use: /add &lt;id&gt; &lt;hour/day/week/month&gt;",
            parse_mode="HTML"
        )

# ------------------------------------------------------------------------------
# /remove Command – Remove a user's access (Owner only).
@sahil_bot.message_handler(commands=['remove'])
def remove_user(message):
    if message.chat.id != OWNER_ID:
        sahil_bot.send_message(
            message.chat.id,
            "❌ <b>Sirf Owner is command ka use kar sakta hai!</b> 🔒",
            parse_mode="HTML"
        )
        return
    try:
        user_id = int(message.text.split()[1])
        if user_id in approved_users:
            del approved_users[user_id]
            sahil_bot.send_message(
                message.chat.id,
                f"✅ <b>User {user_id} ka access remove kar diya gaya hai.</b>",
                parse_mode="HTML"
            )
        else:
            sahil_bot.send_message(
                message.chat.id,
                "❌ <b>User already removed ya exist nahi karta!</b>",
                parse_mode="HTML"
            )
    except Exception:
        sahil_bot.send_message(
            message.chat.id,
            "❌ <b>Invalid format!</b> Use: /remove &lt;id&gt;",
            parse_mode="HTML"
        )

# ------------------------------------------------------------------------------
# /clearlogs Command – Delete the file "sahil.txt" (Owner only).
@sahil_bot.message_handler(commands=['clearlogs'])
def clear_logs(message):
    if message.chat.id != OWNER_ID:
        sahil_bot.send_message(
            message.chat.id,
            "❌ <b>Sirf Owner is command ka use kar sakta hai!</b> 🔒",
            parse_mode="HTML"
        )
        return
    try:
        if os.path.exists("sahil.txt"):
            os.remove("sahil.txt")
            sahil_bot.send_message(
                message.chat.id,
                "✅ <b>Logs (sahil.txt) clear kar diye gaye hain!</b> 🗑️",
                parse_mode="HTML"
            )
        else:
            sahil_bot.send_message(
                message.chat.id,
                "❌ <b>Logs file exist nahi karti!</b>",
                parse_mode="HTML"
            )
    except Exception:
        sahil_bot.send_message(
            message.chat.id,
            "❌ <b>Error: Logs delete nahi ho sake!</b>",
            parse_mode="HTML"
        )

# ------------------------------------------------------------------------------
# /time Command – Show current time.
@sahil_bot.message_handler(commands=['time'])
def time_message(message):
    if message.chat.id in approved_users:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sahil_bot.send_message(
            message.chat.id,
            f"🕒 <b>Current Time:</b> {current_time}",
            parse_mode="HTML"
        )
    else:
        sahil_bot.send_message(
            message.chat.id,
            "⛔ <b>Aap is bot ko use nahi kar sakte. Admin approval required.</b> 🚫",
            parse_mode="HTML"
        )

# ------------------------------------------------------------------------------
# /generate Command – Ask user to choose payload type, then number, then (if Hex) payload value.
@sahil_bot.message_handler(commands=['generate'])
def generate_command(message):
    if message.chat.id not in approved_users:
        sahil_bot.send_message(
            message.chat.id,
            "⛔ <b>Aap is bot ko use nahi kar sakte. Admin approval required.</b> 🚫",
            parse_mode="HTML"
        )
        return
    # Use a reply keyboard for payload type selection.
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.row('Multi', 'Hex')
    prompt = (
        "🔄 <b>Select Payload Type:</b><br>"
        "• <b>Multi</b>: Generates payload like: xb0\\x45\\x5c\\x74\\x9d\\xb4\\xc8\\xd9<br>"
        "• <b>Hex</b>: Generates payload like: \"\\x91\", \"\\x91\", \"\\x91\"<br>"
        "For Hex, you can input any custom hex value (e.g., \\x91 or \\x51)."
    )
    sahil_bot.send_message(message.chat.id, prompt, reply_markup=markup, parse_mode="HTML")
    sahil_bot.register_next_step_handler(message, process_payload_choice)

def process_payload_choice(message):
    chosen_type = message.text.strip().lower()  # Should be 'multi' or 'hex'
    sahil_bot.send_message(
        message.chat.id,
        f"⏳ <b>Generating {chosen_type.capitalize()} Payload...</b> 💥",
        parse_mode="HTML"
    )
    sahil_bot.send_message(
        message.chat.id,
        "📏 <b>Enter the number of payload units (e.g., 5, 10, 20):</b>",
        parse_mode="HTML"
    )
    sahil_bot.register_next_step_handler(message, lambda msg: process_payload_count(msg, chosen_type))

def process_payload_count(message, chosen_type):
    if not message.text.isdigit():
        sahil_bot.send_message(
            message.chat.id,
            "❌ <b>Please enter a valid number!</b> ⚠️",
            parse_mode="HTML"
        )
        return
    count = int(message.text)
    if count <= 0:
        sahil_bot.send_message(
            message.chat.id,
            "❌ <b>Number must be greater than 0!</b> ⚠️",
            parse_mode="HTML"
        )
        return
    if chosen_type == "hex":
        sahil_bot.send_message(
            message.chat.id,
            "📏 <b>Enter the payload value (e.g., \\x91 or \\x51):</b>",
            parse_mode="HTML"
        )
        sahil_bot.register_next_step_handler(message, lambda msg: process_payload_value(msg, chosen_type, count))
    else:  # For multi option, use fixed value.
        file_path = generate_and_save_payload("multi", count, payload_value="xb0\\x45\\x5c\\x74\\x9d\\xb4\\xc8\\xd9")
        if file_path:
            with open(file_path, "rb") as f:
                sahil_bot.send_document(message.chat.id, f)
            sahil_bot.send_message(
                message.chat.id,
                f"✅ <b>sahil.txt</b> file with Multi payload generated successfully! 🎉📂",
                parse_mode="HTML"
            )
        else:
            sahil_bot.send_message(
                message.chat.id,
                "❌ <b>Error: Could not generate payload.</b> ⚠️",
                parse_mode="HTML"
            )

def process_payload_value(message, chosen_type, count):
    payload_value = message.text.strip()
    if not (payload_value.startswith("\\x") and len(payload_value) == 4):
        sahil_bot.send_message(
            message.chat.id,
            "❌ <b>Invalid payload value!</b> Please enter a value like \\x91 or \\x51.",
            parse_mode="HTML"
        )
        return
    file_path = generate_and_save_payload("hex", count, payload_value)
    if file_path:
        with open(file_path, "rb") as f:
            sahil_bot.send_document(message.chat.id, f)
        sahil_bot.send_message(
            message.chat.id,
            f"✅ <b>sahil.txt</b> file with Hex payload generated successfully! 🎉📂",
            parse_mode="HTML"
        )
    else:
        sahil_bot.send_message(
            message.chat.id,
            "❌ <b>Error: Could not generate payload.</b> ⚠️",
            parse_mode="HTML"
        )

# ------------------------------------------------------------------------------
# Start bot polling
if __name__ == "__main__":
    sahil_bot.polling()
    