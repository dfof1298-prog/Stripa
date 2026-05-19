# ==================== main.py (لـ Stripe Charge 5$ - Axel-Wehning) ====================

import socket

orig_getaddrinfo = socket.getaddrinfo
def getaddrinfo_ipv4(*args, **kwargs):
    return [ai for ai in orig_getaddrinfo(*args, **kwargs) if ai[0] == socket.AF_INET]
socket.getaddrinfo = getaddrinfo_ipv4
import telebot,os
import re,json
import requests
import telebot,time,random
import random
import string
from telebot import types
from gatet import ch
from reg import reg
from datetime import datetime, timedelta
from faker import Faker
import telebot
from telebot.types import LabeledPrice, InlineKeyboardMarkup, InlineKeyboardButton, PreCheckoutQuery
from datetime import datetime, timedelta
import json
from multiprocessing import Process
import threading

# قاموس لتتبع الفحوصات النشطة لكل مستخدم
active_scans = {}

stopuser = {}
token = '8993584606:AAFkRzB2flAx2iQEwYpsgDKrmwYIoM41M64'
bot = telebot.TeleBot(token, parse_mode="HTML")
admin = 1093032296
f = Faker()
name = f.name()
street = f.address()
city = f.city()
state = f.state()
postal = f.zipcode()
phone = f.phone_number()
coun = f.country()
mail = f.email()
command_usage = {}
user_check_counts = {}
MAX_CHECKS_FREE = 1000

def reset_command_usage():
    for user_id in command_usage:
        command_usage[user_id] = {'count': 0, 'last_time': None}

def update_user_check_count(user_id):
    user_id_str = str(user_id)
    if user_id_str not in user_check_counts:
        user_check_counts[user_id_str] = 0
    user_check_counts[user_id_str] += 1
    return user_check_counts[user_id_str]

def get_remaining_checks(user_id):
    if user_id == admin:
        return "غير محدود"
    user_id_str = str(user_id)
    current = user_check_counts.get(user_id_str, 0)
    remaining = MAX_CHECKS_FREE - current
    return remaining if remaining > 0 else 0

def reset_user_checks(user_id):
    user_id_str = str(user_id)
    if user_id_str in user_check_counts:
        user_check_counts[user_id_str] = 0
    return True

def add_user_checks(user_id, amount):
    user_id_str = str(user_id)
    if user_id_str not in user_check_counts:
        user_check_counts[user_id_str] = 0
    user_check_counts[user_id_str] += amount
    return user_check_counts[user_id_str]

def set_user_checks(user_id, amount):
    user_id_str = str(user_id)
    user_check_counts[user_id_str] = amount
    return True

def has_active_scan(user_id):
    return user_id in active_scans and active_scans[user_id].get("active", False)

def stop_user_scan(user_id):
    if user_id in active_scans:
        active_scans[user_id]["stop_requested"] = True
        return True
    return False

def remove_active_scan(user_id):
    if user_id in active_scans:
        active_scans[user_id]["active"] = False
        del active_scans[user_id]

BANNED_USERS_FILE = "banned_users.json"
USERS_LIST_FILE = "users_list.json"

def load_banned_users():
    try:
        with open(BANNED_USERS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_banned_users(banned):
    with open(BANNED_USERS_FILE, "w") as f:
        json.dump(banned, f, indent=4)

def is_user_banned(user_id):
    banned = load_banned_users()
    return str(user_id) in banned

def ban_user_id(user_id):
    banned = load_banned_users()
    banned[str(user_id)] = True
    save_banned_users(banned)

def unban_user_id(user_id):
    banned = load_banned_users()
    if str(user_id) in banned:
        del banned[str(user_id)]
        save_banned_users(banned)

def load_users_list():
    try:
        with open(USERS_LIST_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_users_list(users):
    with open(USERS_LIST_FILE, "w") as f:
        json.dump(users, f, indent=4)

def add_user_to_list(user_id, username, first_name):
    users = load_users_list()
    user_id_str = str(user_id)
    if user_id_str not in users:
        users[user_id_str] = {
            "username": username,
            "first_name": first_name,
            "joined_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "checks": user_check_counts.get(user_id_str, 0)
        }
        save_users_list(users)
        bot.send_message(admin, f"🆕 **مستخدم جديد!**\n👤 {first_name}\n🆔 `{user_id}`\n🔗 @{username if username else 'لا يوجد'}", parse_mode="Markdown")
    return users

def update_user_in_list(user_id, checks=None):
    users = load_users_list()
    user_id_str = str(user_id)
    if user_id_str in users:
        if checks is not None:
            users[user_id_str]["checks"] = checks
        save_users_list(users)

def get_all_users_list():
    return load_users_list()

def can_user_check(user_id, needed=1):
    if user_id == admin:
        return True
    if is_user_banned(user_id):
        return False
    user_id_str = str(user_id)
    current = user_check_counts.get(user_id_str, 0)
    return (current + needed) <= MAX_CHECKS_FREE

@bot.message_handler(commands=["start"])
def start(message):
    def my_function():
        user_id = message.from_user.id
        username = message.from_user.username or "𝐔𝐬𝐞𝐫"
        add_user_to_list(user_id, username, message.from_user.first_name)
        keyboard = types.InlineKeyboardMarkup()
        add_bot_button = types.InlineKeyboardButton(text="𝐀𝐝𝐝 𝐭𝐡𝐞 𝐛𝐨𝐭 𝐭𝐨 𝐲𝐨𝐮𝐫 𝐜𝐨𝐥𝐥𝐞𝐜𝐭𝐢𝐨𝐧", url="https://t.me/Joker73336?startgroup")
        cmds_button = types.InlineKeyboardButton(text="𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬", callback_data="menu")
        cmutton = types.InlineKeyboardButton(text="𝐁𝐔𝐘", callback_data="Buy")        
        keyboard.row(add_bot_button, cmutton)
        keyboard.row(cmds_button)
        video_url = 'https://t.me/Joker73336/6'
        bot.send_video(
            chat_id=message.chat.id,
            video=video_url,
            caption=f"""<b>𝐇𝐞𝐥𝐥𝐨 @{username}! [<code>{user_id}</code>]
𝐎𝐩𝐞𝐫𝐚𝐭𝐢𝐨𝐧𝐚𝐥 𝐁𝐨𝐭!
━━━━━━━━━━━━
𝐒𝐭𝐚𝐭𝐮𝐬: 𝐀𝐜𝐭𝐢𝐯𝐞 ✅
𝐑𝐞𝐦𝐚𝐢𝐧𝐢𝐧𝐠 𝐜𝐡𝐞𝐜𝐤𝐬: {get_remaining_checks(user_id)}
━━━━━━━━━━━━
𝐔𝐬𝐞 𝐭𝐡𝐞 𝐛𝐮𝐭𝐭𝐨𝐧 𝐛𝐞𝐥𝐨𝐰 𝐭𝐨 𝐯𝐢𝐞𝐰 𝐜𝐨𝐦𝐦𝐚𝐧𝐝𝐬 .

𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫:𝐉𝐨𝐤𝐞𝐫 🃏</b>""",
            reply_markup=keyboard,
            parse_mode="HTML"
        )
    threading.Thread(target=my_function).start()

@bot.message_handler(commands=["admin"])
def show_admin_commands(message):
    if message.from_user.id != admin:
        bot.reply_to(message, "❌ هذا الأمر للمالك فقط!")
        return
    commands_text = """
👑 **أوامر المالك - 𝐉𝐨𝐤𝐞𝐫 🃏**
━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 **إدارة المستخدمين:**
• `/users` - عرض جميع المستخدمين
• `/ban <ايدي>` - حظر مستخدم
• `/unban <ايدي>` - فك الحظر
• `/userinfo <ايدي>` - معلومات مستخدم

━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 **إدارة الفحوصات:**
• `/resetchecks <ايدي>` - إعادة تعيين فحوصات المستخدم
• `/addchecks <ايدي> <عدد>` - إضافة فحوصات
• `/setchecks <ايدي> <عدد>` - تعيين عدد فحوصات
• `/mychecks` - معرفة فحوصاتك أنت

━━━━━━━━━━━━━━━━━━━━━━━━━━
💎 **إدارة الاشتراكات:**
• `/code <ساعات>` - إنشاء كود اشتراك
• `/add <ايدي> <ساعات>` - إضافة اشتراك VIP مباشر
• `/dell <ايدي>` - حذف VIP من مستخدم

━━━━━━━━━━━━━━━━━━━━━━━━━━
📢 **الإذاعة:**
• `/broadcast <رسالة>` - إذاعة للجميع

━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 **إدارة الأسعار:**
• `/set 1 <سعر>` - تعديل سعر الساعة
• `/set 2 <سعر>` - تعديل سعر اليوم
• `/set 3 <سعر>` - تعديل سعر الأسبوع

━━━━━━━━━━━━━━━━━━━━━━━━━━
🛠️ **أوامر إضافية:**
• `/status` - حالة حسابك
• `/vip` - عرض قائمة VIP
• `/all <رسالة>` - إرسال رسالة للكل

━━━━━━━━━━━━━━━━━━━━━━━━━━
✨ **𝐁𝐲: 𝐉𝐨𝐤𝐞𝐫 🃏**
"""
    bot.reply_to(message, commands_text, parse_mode="Markdown")

@bot.message_handler(commands=["userinfo"])
def user_info(message):
    if message.from_user.id != admin:
        bot.reply_to(message, "❌ هذا الأمر للمالك فقط!")
        return
    try:
        user_id = int(message.text.split()[1])
    except:
        bot.reply_to(message, "❌ استخدم: `/userinfo <ايدي المستخدم>`", parse_mode="Markdown")
        return
    user_id_str = str(user_id)
    is_vip, vip_msg = is_vip_active(user_id)
    checks = user_check_counts.get(user_id_str, 0)
    remaining = get_remaining_checks(user_id)
    try:
        chat = bot.get_chat(user_id)
        username = chat.username or "لا يوجد"
        first_name = chat.first_name or "Unknown"
    except:
        username = "لا يمكن الجلب"
        first_name = "لا يمكن الجلب"
    info_text = f"""
📊 **معلومات المستخدم**
━━━━━━━━━━━━━━━━━━
🆔 **الايدي:** `{user_id}`
👤 **الاسم:** {first_name}
🔗 **اليوزر:** @{username}
━━━━━━━━━━━━━━━━━━
💎 **VIP:** {'✅ نشط' if is_vip else '❌ غير نشط'}
📅 **تفاصيل:** {vip_msg}
━━━━━━━━━━━━━━━━━━
📊 **الفحوصات:**
• استخدم: {checks}
• متبقي: {remaining if not is_vip else 'غير محدود'}
• الحد الأقصى: {MAX_CHECKS_FREE if not is_vip else 'VIP'}
━━━━━━━━━━━━━━━━━━
🚫 **محظور:** {'✅ نعم' if is_user_banned(user_id) else '❌ لا'}
━━━━━━━━━━━━━━━━━━
✨ **𝐉𝐨𝐤𝐞𝐫 🃏**
"""
    bot.reply_to(message, info_text, parse_mode="Markdown")

@bot.message_handler(commands=["users"])
def show_users(message):
    if message.from_user.id != admin:
        bot.reply_to(message, "❌ هذا الأمر للمالك فقط!")
        return
    users = get_all_users_list()
    if not users:
        bot.reply_to(message, "📭 لا يوجد مستخدمين حتى الآن")
        return
    msg = "👥 **قائمة المستخدمين**\n━━━━━━━━━━━━━━━━━━\n"
    for uid, data in users.items():
        msg += f"🆔 `{uid}`\n👤 {data.get('first_name', 'Unknown')}\n🔗 @{data.get('username', 'لا يوجد')}\n📊 فحص: {data.get('checks', 0)}/{MAX_CHECKS_FREE}\n━━━━━━━━━━━━━━━━━━\n"
    if len(msg) > 4000:
        for i in range(0, len(msg), 4000):
            bot.send_message(admin, msg[i:i+4000], parse_mode="Markdown")
    else:
        bot.send_message(admin, msg, parse_mode="Markdown")

@bot.message_handler(commands=["ban"])
def ban_user_command(message):
    if message.from_user.id != admin:
        bot.reply_to(message, "❌ هذا الأمر للمالك فقط!")
        return
    try:
        user_id = int(message.text.split()[1])
        ban_user_id(user_id)
        bot.reply_to(message, f"✅ تم حظر المستخدم `{user_id}`", parse_mode="Markdown")
        try:
            bot.send_message(user_id, "🚫 **لقد تم حظرك من استخدام هذا البوت.**\nللتواصل مع المالك: @Joker")
        except:
            pass
    except:
        bot.reply_to(message, "❌ استخدم: `/ban <ايدي المستخدم>`", parse_mode="Markdown")

@bot.message_handler(commands=["unban"])
def unban_user_command(message):
    if message.from_user.id != admin:
        bot.reply_to(message, "❌ هذا الأمر للمالك فقط!")
        return
    try:
        user_id = int(message.text.split()[1])
        unban_user_id(user_id)
        bot.reply_to(message, f"✅ تم فك الحظر عن المستخدم `{user_id}`", parse_mode="Markdown")
        try:
            bot.send_message(user_id, "✅ **تم فك الحظر عنك!** يمكنك استخدام البوت الآن.")
        except:
            pass
    except:
        bot.reply_to(message, "❌ استخدم: `/unban <ايدي المستخدم>`", parse_mode="Markdown")

@bot.message_handler(commands=["resetchecks"])
def reset_checks_command(message):
    if message.from_user.id != admin:
        bot.reply_to(message, "❌ هذا الأمر للمالك فقط!")
        return
    try:
        user_id = int(message.text.split()[1])
        reset_user_checks(user_id)
        update_user_in_list(user_id, 0)
        bot.reply_to(message, f"✅ تم إعادة تعيين فحوصات المستخدم `{user_id}`", parse_mode="Markdown")
    except:
        bot.reply_to(message, "❌ استخدم: `/resetchecks <ايدي المستخدم>`", parse_mode="Markdown")

@bot.message_handler(commands=["addchecks"])
def add_checks_command(message):
    if message.from_user.id != admin:
        bot.reply_to(message, "❌ هذا الأمر للمالك فقط!")
        return
    try:
        parts = message.text.split()
        user_id = int(parts[1])
        amount = int(parts[2])
        new_total = add_user_checks(user_id, amount)
        update_user_in_list(user_id, new_total)
        bot.reply_to(message, f"✅ تم إضافة {amount} فحص للمستخدم `{user_id}`\n📊 إجمالي الفحوصات الآن: {new_total}", parse_mode="Markdown")
    except:
        bot.reply_to(message, "❌ استخدم: `/addchecks <ايدي المستخدم> <العدد>`", parse_mode="Markdown")

@bot.message_handler(commands=["setchecks"])
def set_checks_command(message):
    if message.from_user.id != admin:
        bot.reply_to(message, "❌ هذا الأمر للمالك فقط!")
        return
    try:
        parts = message.text.split()
        user_id = int(parts[1])
        amount = int(parts[2])
        set_user_checks(user_id, amount)
        update_user_in_list(user_id, amount)
        bot.reply_to(message, f"✅ تم تعيين فحوصات المستخدم `{user_id}` إلى {amount}", parse_mode="Markdown")
    except:
        bot.reply_to(message, "❌ استخدم: `/setchecks <ايدي المستخدم> <العدد>`", parse_mode="Markdown")

@bot.message_handler(commands=["mychecks"])
def my_checks(message):
    user_id = message.from_user.id
    if user_id == admin:
        bot.reply_to(message, "👑 **أنت المالك، ليس لديك حدود للفحص!**")
    else:
        current = user_check_counts.get(str(user_id), 0)
        remaining = MAX_CHECKS_FREE - current
        bot.reply_to(message, f"📊 **عدد فحوصاتك**\n━━━━━━━━━━━━\n✅ استخدمت: {current}\n📋 متبقي: {remaining}\n🔒 الحد الأقصى: {MAX_CHECKS_FREE}")

@bot.message_handler(commands=["broadcast"])
def broadcast_message(message):
    if message.from_user.id != admin:
        bot.reply_to(message, "❌ هذا الأمر للمالك فقط!")
        return
    text = message.text.replace("/broadcast", "").strip()
    if not text:
        bot.reply_to(message, "❌ استخدم: `/broadcast <الرسالة>`", parse_mode="Markdown")
        return
    users = get_all_users_list()
    sent = 0
    failed = 0
    bot.reply_to(message, f"🔄 جاري الإذاعة لـ {len(users)} مستخدم...")
    for uid in users.keys():
        try:
            bot.send_message(int(uid), f"📢 **إذاعة من المالك**\n━━━━━━━━━━━━━━━━\n{text}")
            sent += 1
            time.sleep(0.2)
        except:
            failed += 1
    bot.send_message(admin, f"✅ **تم الإذاعة!**\n✅ نجح: {sent}\n❌ فشل: {failed}")

@bot.callback_query_handler(func=lambda call: call.data == 'menu')
def show_menu(call):
    keyboard = types.InlineKeyboardMarkup()
    plans = types.InlineKeyboardButton(text='𝐆𝐚𝐭𝐞𝐰𝐚𝐲𝐬', callback_data='plans')
    tools = types.InlineKeyboardButton(text='𝐓𝐨𝐨𝐥𝐬', callback_data='tool')
    keyboard.row(plans, tools)
    bot.edit_message_caption(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        caption=f"""<b>𝐀𝐯𝐚𝐢𝐥𝐚𝐛𝐥𝐞 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬:
━━━━━━━━━━━━
𝐓𝐨𝐭𝐚𝐥 𝐆𝐚𝐭𝐞𝐰𝐚𝐲𝐬: 1
𝐓𝐨𝐭𝐚𝐥 𝐓𝐨𝐨𝐥𝐬: 4
━━━━━━━━━━━━
𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫: 𝐉𝐨𝐤𝐞𝐫 🃏</b>""",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

@bot.callback_query_handler(func=lambda call: call.data == 'plans')
def show_gateways(call):
    keyboard = types.InlineKeyboardMarkup()
    back = types.InlineKeyboardButton(text='𝐁𝐚𝐜𝐤', callback_data='menu')
    keyboard.add(back)
    bot.edit_message_caption(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        caption=f"""<b>𝐆𝐚𝐭𝐞𝐰𝐚𝐲𝐬:
━━━━━━━━━━━━
𝐍𝐚𝐦𝐞: 𝐒𝐭𝐫𝐢𝐩𝐞 𝐂𝐡𝐚𝐫𝐠𝐞 𝟓$
𝐒𝐭𝐚𝐭𝐮𝐬: ✅
𝐂𝐨𝐦𝐦𝐚𝐧𝐝: /chk
━━━━━━━━━━━━</b>""",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

@bot.callback_query_handler(func=lambda call: call.data == 'tool')
def show_tools(call):
    keyboard = types.InlineKeyboardMarkup()
    back = types.InlineKeyboardButton(text='𝐁𝐚𝐜𝐤', callback_data='menu')
    keyboard.add(back)
    bot.edit_message_caption(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        caption=f"""<b>𝐀𝐯𝐚𝐢𝐥𝐚𝐛𝐥𝐞 𝐓𝐨𝐨𝐥𝐬:
━━━━━━━━━━━━
𝐍𝐚𝐦𝐞: 𝐂𝐂 𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐨𝐫 𝐀𝐩𝐢 - ✅
𝐂𝐨𝐦𝐦𝐚𝐧𝐝: <code>/gen 440393</code>
━━━━━━━━━━━━
𝐍𝐚𝐦𝐞: 𝐁𝐈𝐍 𝐥𝐨𝐨𝐤𝐮𝐩 𝐀𝐩𝐢 ✅
𝐂𝐨𝐦𝐦𝐚𝐧𝐝: <code>/bin 440393</code>
━━━━━━━━━━━━
𝐍𝐚𝐦𝐞: 𝐂𝐨𝐦𝐝𝐨 𝐁𝐢𝐧 ✅
𝐂𝐨𝐦𝐦𝐚𝐧𝐝: <code>/comdo</code>
━━━━━━━━━━━━
𝐍𝐚𝐦𝐞: 𝐅𝐚𝐤𝐞 𝐀𝐝𝐝𝐫𝐞𝐬𝐬 𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐨𝐫 ✅
𝐂𝐨𝐦𝐦𝐚𝐧𝐝: <code>/fake</code></b>""",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

DATA_FILE = "data.json"

def load_users():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_users(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

STAR_PRICES = {
    "1hour": 10,
    "3hours": 30,
    "1day": 100,
    "1week": 700
}

@bot.callback_query_handler(func=lambda call: call.data == 'Buy')
def show_subscription_plans(call):
    keyboard = InlineKeyboardMarkup(row_width=2)
    hour1 = InlineKeyboardButton(f"🕐 1 ساعة - {STAR_PRICES['1hour']} ⭐", callback_data='sub_1hour')
    hour3 = InlineKeyboardButton(f"🕒 3 ساعات - {STAR_PRICES['3hours']} ⭐", callback_data='sub_3hours')
    day1 = InlineKeyboardButton(f"📅 1 يوم - {STAR_PRICES['1day']} ⭐", callback_data='sub_1day')
    week1 = InlineKeyboardButton(f"📆 1 أسبوع - {STAR_PRICES['1week']} ⭐", callback_data='sub_1week')
    back = InlineKeyboardButton("🔙 رجوع", callback_data='menu')
    keyboard.add(hour1, hour3, day1, week1, back)
    bot.edit_message_caption(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        caption="⭐ **خطط الاشتراك** ⭐\n━━━━━━━━━━━━━━━━━━\nاختر الباقة المناسبة لك:\n• 1 ساعة → 10 نجوم\n• 3 ساعات → 30 نجمة\n• 1 يوم → 100 نجمة\n• 1 أسبوع → 700 نجمة\n━━━━━━━━━━━━━━━━━━\nالدفع عبر نجوم تليجرام 💫",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('sub_'))
def handle_subscription(call):
    plan = call.data.split('_')[1]
    user_id = call.from_user.id
    prices_map = {
        '1hour': {'stars': STAR_PRICES['1hour'], 'hours': 1, 'name': 'ساعة واحدة'},
        '3hours': {'stars': STAR_PRICES['3hours'], 'hours': 3, 'name': '3 ساعات'},
        '1day': {'stars': STAR_PRICES['1day'], 'hours': 24, 'name': 'يوم واحد'},
        '1week': {'stars': STAR_PRICES['1week'], 'hours': 168, 'name': 'أسبوع واحد'}
    }
    if plan not in prices_map:
        bot.answer_callback_query(call.id, "❌ حدث خطأ، حاول مرة أخرى")
        return
    plan_info = prices_map[plan]
    title = f"اشتراك VIP - {plan_info['name']}"
    description = f"اشتراك مميز في بوت Joker 🃏\nلمدة {plan_info['name']}\nفحص غير محدود خلال المدة"
    prices = [LabeledPrice(label="VIP Subscription", amount=plan_info['stars'])]
    try:
        bot.send_invoice(
            chat_id=user_id,
            title=title,
            description=description,
            invoice_payload=f"vip_{plan}_{user_id}_{plan_info['hours']}",
            provider_token="",
            currency="XTR",
            prices=prices,
            start_parameter="vip_subscription"
        )
    except Exception as e:
        bot.answer_callback_query(call.id, f"❌ حدث خطأ: {str(e)[:50]}")
        bot.send_message(admin, f"⚠️ خطأ في الدفع للمستخدم {user_id}: {e}")

@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout_handler(pre_checkout_query: PreCheckoutQuery):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def successful_payment_handler(message):
    payload = message.successful_payment.invoice_payload
    user_id = message.from_user.id
    amount = message.successful_payment.total_amount
    parts = payload.split('_')
    if len(parts) >= 4 and parts[0] == 'vip':
        plan_type = parts[1]
        hours = int(parts[3])
        end_time = datetime.now() + timedelta(hours=hours)
        with open('data.json', 'r') as f:
            subs = json.load(f)
        user_id_str = str(user_id)
        subs[user_id_str] = {
            "plan": "𝗩𝗜𝗣",
            "timer": end_time.strftime("%Y-%m-%d %H:%M")
        }
        with open('data.json', 'w') as f:
            json.dump(subs, f, indent=4)
        if user_id_str in user_check_counts:
            user_check_counts[user_id_str] = 0
        update_user_in_list(user_id, 0)
        bot.send_message(
            user_id,
            f"✅ **تم تفعيل اشتراك VIP بنجاح!**\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"⭐ المبلغ المدفوع: {amount} نجمة\n"
            f"📅 ينتهي في: {end_time.strftime('%Y-%m-%d %H:%M')}\n"
            f"🎉 أصبحت الآن مشترك VIP - فحص غير محدود!\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"𝐉𝐨𝐤𝐞𝐫 🃏"
        )
        user = message.from_user
        bot.send_message(
            admin,
            f"💎 **اشتراك VIP جديد!**\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"👤 المستخدم: {user.first_name}\n"
            f"🆔 المعرف: `{user_id}`\n"
            f"🔗 اليوزر: @{user.username if user.username else 'لا يوجد'}\n"
            f"⭐ المبلغ: {amount} نجمة\n"
            f"⏰ المدة: {hours} ساعة\n"
            f"📅 ينتهي: {end_time.strftime('%Y-%m-%d %H:%M')}\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"𝐉𝐨𝐤𝐞𝐫 🃏",
            parse_mode="Markdown"
        )
    else:
        bot.send_message(user_id, "❌ حدث خطأ في معالجة الدفع، يرجى التواصل مع المالك")

def is_vip_active(user_id):
    if user_id == admin:
        return True, "المالك"
    try:
        with open('data.json', 'r') as f:
            subs = json.load(f)
        user_id_str = str(user_id)
        if user_id_str not in subs:
            return False, "لا يوجد اشتراك"
        timer_str = subs[user_id_str].get("timer")
        if not timer_str:
            return False, "لا يوجد اشتراك"
        expiry = datetime.strptime(timer_str, "%Y-%m-%d %H:%M")
        if expiry > datetime.now():
            remaining = expiry - datetime.now()
            hours_left = remaining.total_seconds() // 3600
            return True, f"{int(hours_left)} ساعة متبقية"
        else:
            return False, "انتهى الاشتراك"
    except:
        return False, "خطأ في التحقق"

@bot.message_handler(commands=["status"])
def check_status(message):
    user_id = message.from_user.id
    is_vip, msg = is_vip_active(user_id)
    if is_vip:
        bot.reply_to(
            message,
            f"🌟 **حالة اشتراكك** 🌟\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"✅ الاشتراك: **نشط**\n"
            f"📋 التفاصيل: {msg}\n"
            f"🎯 فحص: غير محدود\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"𝐉𝐨𝐤𝐞𝐫 🃏"
        )
    else:
        remaining = get_remaining_checks(user_id)
        bot.reply_to(
            message,
            f"📊 **حالة حسابك**\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"❌ الاشتراك: {msg}\n"
            f"📋 الفحوصات المتبقية: {remaining}\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🛒 استخدم /buy للاشتراك VIP\n"
            f"𝐉𝐨𝐤𝐞𝐫 🃏"
        )

@bot.message_handler(content_types=["document"])
def handle_document(message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    if is_user_banned(user_id):
        bot.reply_to(message, "🚫 **لقد تم حظرك من استخدام هذا البوت.**\nللتواصل مع المالك: @Joker")
        return
    if has_active_scan(user_id):
        bot.reply_to(message, "⚠️ **يوجد فحص نشط بالفعل!**\n❌ لا يمكنك رفع ملف جديد حتى ينتهي الفحص الحالي.\n━━━━━━━━━━━━━━━━━━\n🛑 استخدم زر STOP لإيقاف الفحص الحالي")
        return
    with open('data.json', 'r') as file:
        json_data = json.load(file)
    is_vip, vip_msg = is_vip_active(user_id)
    try:
        BL = (json_data[str(user_id)]['plan']) if str(user_id) in json_data else '𝗙𝗥𝗘𝗘'
    except:
        BL = '𝗙𝗥𝗘𝗘'
    if BL == '𝗙𝗥𝗘𝗘' and not is_vip:
        with open('data.json', 'r') as json_file:
            existing_data = json.load(json_file)
        new_data = {
            user_id: {
                "plan": "𝗙𝗥𝗘𝗘",
                "timer": "none",
            }
        }
        existing_data.update(new_data)
        with open('data.json', 'w') as json_file:
            json.dump(existing_data, json_file, ensure_ascii=False, indent=4)
        keyboard = types.InlineKeyboardMarkup()
        contact_button = types.InlineKeyboardButton(text="𝐃𝐞𝐯", url="https://t.me/Joker")
        keyboard.add(contact_button)
        bot.send_message(chat_id=message.chat.id, text=f'''<b>𝐘𝐨𝐮 𝐜𝐚𝐧'𝐭 𝐮𝐬𝐞 𝐭𝐡𝐞 𝐛𝐨𝐭 𝐛𝐞𝐜𝐚𝐮𝐬𝐞 𝐲𝐨𝐮𝐫 𝐬𝐮𝐛𝐬𝐜𝐫𝐢𝐩𝐭𝐢𝐨𝐧 𝐡𝐚𝐬 𝐞𝐱𝐩𝐢𝐫𝐞𝐝 ❌
</b>\n🛒 استخدم /buy للاشتراك''', reply_markup=keyboard)
        return
    ee = bot.download_file(bot.get_file(message.document.file_id).file_path)
    with open("combo.txt", "wb") as w:
        w.write(ee)
    with open("combo.txt", "r") as file:
        lines_list = file.readlines()
        line_count = len(lines_list)
        if line_count > 2000000:
            bot.reply_to(message, "❌ 𝐌𝐚𝐱𝐢𝐦𝐮𝐦 2000000 𝐜𝐚𝐫𝐝𝐬 𝐚𝐥𝐥𝐨𝐰𝐞𝐝 𝐩𝐞𝐫 𝐟𝐢𝐥𝐞!")
            return
    if not is_vip and user_id != admin:
        current_checks = user_check_counts.get(str(user_id), 0)
        if current_checks + line_count > MAX_CHECKS_FREE:
            remaining = MAX_CHECKS_FREE - current_checks
            bot.reply_to(
                message,
                f"❌ **لا يمكنك فحص {line_count} بطاقة!**\n"
                f"📊 المتبقي لك: {remaining} فحص فقط\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"💎 اشترك VIP للفحص غير المحدود:\n"
                f"🛒 استخدم /buy"
            )
            return
    if not is_vip:
        try:
            date_str = json_data[str(user_id)]['timer'].split('.')[0]
            provided_time = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        except:
            keyboard = types.InlineKeyboardMarkup()
            ahmed = types.InlineKeyboardButton(text="𝐃𝐞𝐯", url="https://t.me/Joker")
            keyboard.add(ahmed)
            bot.send_message(chat_id=message.chat.id, text=f'''<b>𝐘𝐨𝐮 𝐜𝐚𝐧'𝐭 𝐮𝐬𝐞 𝐭𝐡𝐞 𝐛𝐨𝐭 𝐛𝐞𝐜𝐚𝐮𝐬𝐞 𝐲𝐨𝐮𝐫 𝐬𝐮𝐛𝐬𝐜𝐫𝐢𝐩𝐭𝐢𝐨𝐧 𝐡𝐚𝐬 𝐞𝐱𝐩𝐢𝐫𝐞𝐝 ❌</b>\n🛒 استخدم /buy للاشتراك''', reply_markup=keyboard)
            return
        current_time = datetime.now()
        if current_time > provided_time:
            keyboard = types.InlineKeyboardMarkup()
            ahmed = types.InlineKeyboardButton(text="𝐃𝐞𝐯", url="https://t.me/Joker")
            keyboard.add(ahmed)
            bot.send_message(chat_id=message.chat.id, text=f'''<b>𝐘𝐨𝐮 𝐜𝐚𝐧'𝐭 𝐮𝐬𝐞 𝐭𝐡𝐞 𝐛𝐨𝐭 𝐛𝐞𝐜𝐚𝐮𝐬𝐞 𝐲𝐨𝐮𝐫 𝐬𝐮𝐛𝐬𝐜𝐫𝐢𝐩𝐭𝐢𝐨𝐧 𝐡𝐚𝐬 𝐞𝐱𝐩𝐢𝐫𝐞𝐝 ❌</b>\n🛒 استخدم /buy للاشتراك''', reply_markup=keyboard)
            with open('data.json', 'w') as file:
                json_data[str(user_id)]['timer'] = 'none'
                json_data[str(user_id)]['plan'] = '𝗙𝗥𝗘𝗘'
                json.dump(json_data, file, indent=2)
            return
    if not is_vip and user_id != admin:
        update_user_check_count(user_id)
        update_user_in_list(user_id, user_check_counts.get(str(user_id), 0))
    keyboard = types.InlineKeyboardMarkup()
    stripe_btn = types.InlineKeyboardButton(text=f"𝐒𝐭𝐫𝐢𝐩𝐞 𝐂𝐡𝐚𝐫𝐠𝐞 𝟓$", callback_data='stripe_charge')
    keyboard.add(stripe_btn)
    bot.reply_to(message, text=f'𝐂𝐡𝐨𝐨𝐬𝐞 𝐓𝐡𝐞 𝐆𝐚𝐭𝐞𝐰𝐚𝐲 𝐘𝐨𝐮 𝐖𝐚𝐧𝐧𝐚 𝐔𝐬𝐞\n\n👤 {name}\n📊 فحوصات متبقية: {get_remaining_checks(user_id)}', reply_markup=keyboard)

# ==================== أوامر الفحص (Stripe Charge 5$) ====================

@bot.callback_query_handler(func=lambda call: call.data == 'stripe_charge')
def menu_callback(call):
    def my_function():
        user_id = call.from_user.id
        active_scans[user_id] = {"active": True, "stop_requested": False}
        if is_user_banned(user_id):
            bot.edit_message_text("🚫 **لقد تم حظرك!**", chat_id=call.message.chat.id, message_id=call.message.message_id)
            remove_active_scan(user_id)
            return
        user = call.from_user.username
        name = call.from_user.first_name
        gate = '𝐒𝐭𝐫𝐢𝐩𝐞 𝐂𝐡𝐚𝐫𝐠𝐞 𝟓$'
        dd = 0
        live = 0
        ch_count = 0
        ccnn = 0
        risk_count = 0
        op = 0 
        app = 0
        gate_number = 0
        
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="𝐂𝐡𝐞𝐜𝐤𝐢𝐧𝐠 𝐘𝐨𝐮𝐫 𝐂𝐚𝐫𝐝𝐬...⌛"
        )
        
        try:
            with open("combo.txt", 'r') as file:
                lino = file.readlines()
                total = len(lino)
                
                for index, cc in enumerate(lino):
                    if not active_scans.get(user_id, {}).get("active", False) or active_scans.get(user_id, {}).get("stop_requested", False):
                        bot.edit_message_text(
                            chat_id=call.message.chat.id,
                            message_id=call.message.message_id,
                            text="🛑 **تم إيقاف الفحص بناءً على طلبك** 🛑"
                        )
                        break
                    
                    cc = cc.strip()
                    data = {}
                    try:
                        data = requests.get('https://bins.antipublic.cc/bins/'+cc[:6]).json()
                    except:
                        pass
                    
                    try:
                        level = data['level']
                    except:
                        level = '𝐮𝐧𝐤𝐧𝐨𝐰𝐧'
                    try:
                        bank = data['bank']
                    except:
                        bank = '𝐮𝐧𝐤𝐧𝐨𝐰𝐧'
                    try:
                        country = data['country']
                        country_flag = data['country_flag']
                    except:
                        country = '𝐮𝐧𝐤𝐧𝐨𝐰𝐧'
                        country_flag = '𝐮𝐧𝐤𝐧𝐨𝐰𝐧'
                    try:
                        brand = data['brand']
                    except:
                        brand = '𝐮𝐧𝐤𝐧𝐨𝐰𝐧'
                    try:
                        card_type = data['type']
                    except:
                        card_type = '𝐮𝐧𝐤𝐧𝐨𝐰𝐧'
                    
                    start_time = time.time()
                    last = "ERROR"  
                    try:
                        result = ch(cc)
                        # تصنيف النتيجة حسب ردود gatet.py (Stripe)
                        if result == 'CHARGED':
                            last = 'Charged 💰'
                        elif result == 'INSUFFICIENT FUNDS':
                            last = 'Insufficient Funds 💸'
                        elif result == 'CVV MISMATCH':
                            last = 'CVV Mismatch 🔒'
                        elif result == 'EXPIRED CARD':
                            last = 'Expired Card 📅'
                        elif result == 'SUSPECTED FRAUD':
                            last = 'Suspected Fraud ⚠️'
                        elif result == 'DO NOT HONOR':
                            last = 'Do Not Honor 🚫'
                        elif result == 'CLOSED CARD':
                            last = 'Closed Card 🔒'
                        elif result == 'CALL ISSUER':
                            last = 'Call Issuer 📞'
                        elif result == 'PICK UP CARD':
                            last = 'Pick Up Card 🃏'
                        elif result == '3D SECURE REQUIRED':
                            last = '3D Secure Required 🔐'
                        elif result == 'LIMIT EXCEEDED':
                            last = 'Limit Exceeded 📊'
                        elif result == 'LOST/STOLEN CARD':
                            last = 'Lost/Stolen Card 🏴'
                        elif result == 'ADDRESS MISMATCH':
                            last = 'Address Mismatch 📍'
                        elif result == 'PROCESSOR DECLINED':
                            last = 'Processor Declined 🏦'
                        elif result == 'INVALID CARD NUMBER':
                            last = 'Invalid Card Number ❌'
                        elif result == 'TRANSACTION NOT ALLOWED':
                            last = 'Transaction Not Allowed 🚫'
                        elif result == 'INVALID CARD':
                            last = 'Invalid Card ❌'
                        else:
                            last = result if len(result) < 40 else 'Declined ❌'
                    except Exception as e:
                        print(f"Error processing card {cc}: {e}")
                        last = "ERROR"
                    
                    mes = types.InlineKeyboardMarkup(row_width=1)
                    mes.add(
                        types.InlineKeyboardButton(f"• {cc[:20]}... •", callback_data='u8'),
                        types.InlineKeyboardButton(f"• 𝐒𝐓𝐀𝐓𝐔𝐒 ➜ {last[:35]} •", callback_data='u8'),
                        types.InlineKeyboardButton(f"• 𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 𝐂𝐡𝐚𝐫𝐠𝐞 ✅ ➜ [ {ch_count} ] •", callback_data='x'),
                        types.InlineKeyboardButton(f"• 𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅ ➜ [ {app} ] •", callback_data='x'),
                        types.InlineKeyboardButton(f"• 𝐎𝐓𝐏 ☑️ ➜ [ {op} ] •", callback_data='x'),
                        types.InlineKeyboardButton(f"• 𝐂𝐜𝐧 ☑️ ➜ [ {ccnn} ] •", callback_data='x'),
                        types.InlineKeyboardButton(f"• 𝐢𝐧𝐬𝐮𝐟𝐟𝐢𝐜𝐢𝐞𝐧𝐭 𝐅𝐮𝐧𝐝𝐬 ☑️ ➜ [ {live} ] •", callback_data='x'),
                        types.InlineKeyboardButton(f"• 𝐃𝐄𝐂𝐋𝐈𝐍𝐄𝐃 ❌ ➜ [ {dd} ] •", callback_data='x'),
                        types.InlineKeyboardButton(f"• 𝐓𝐎𝐓𝐀𝐋 👻 ➜ [ {total} ] •", callback_data='x'),
                        types.InlineKeyboardButton(f"• {index+1}/{total} •", callback_data='x'),
                        types.InlineKeyboardButton(f"[ 𝐒𝐓𝐎𝐏 ]", callback_data=f'stop_scan_{user_id}')
                    )
                    
                    end_time = time.time()
                    execution_time = end_time - start_time
                    
                    bot.edit_message_text(
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        text=f'''𝐏𝐥𝐞𝐚𝐬𝐞 𝐖𝐚𝐢𝐭 𝐖𝐡𝐢𝐥𝐞 𝐘𝐨𝐮𝐫 𝐂𝐚𝐫𝐝𝐬 𝐀𝐫𝐞 𝐁𝐞𝐢𝐧𝐠 𝐂𝐡𝐞𝐜𝐤 𝐀𝐭 𝐓𝐡𝐞 𝐆𝐚𝐭𝐞𝐰𝐚𝐲 {gate}''',
                        reply_markup=mes
                    )
                    
                    base_msg = f'''
- - - - - - - - - - - - - - - - - - - - - - -
[ϟ] 𝐂𝐚𝐫𝐝:  <code>{cc}</code> 
[ϟ] 𝐒𝐭𝐚𝐭𝐮𝐬: <b>{last}</b>
- - - - - - - - - - - - - - - - - - - - - - - -
[ϟ] 𝐈𝐧𝐟𝐨: <code>{card_type} - {brand}</code>
[ϟ] 𝐁𝐚𝐧𝐤: <code>{bank}</code>
[ϟ] 𝐂𝐨𝐮𝐧𝐭𝐫𝐲: <code>{country} - [{country_flag}]</code>
- - - - - - - - - - - - - - - - - - - - - - - -
[⌥] 𝐓𝐢𝐦𝐞: <code>{"{:.1f}".format(execution_time)}</code> 𝐒𝐞𝐜. || 𝐏𝐫𝐨𝐱𝐲: <code>𝐋𝐢𝐯𝐞</code> ✅
[⎇] 𝐑𝐞𝐪 𝐁𝐲: <a href="tg://resolve?domain={user}">{name}</a> 

- - - - - - - - - - - - - - - - - - - - - - - -
[⌤] 𝐃𝐞𝐯 𝐛𝐲: 𝐉𝐨𝐤𝐞𝐫 🃏'''
                    
                    if 'Charged' in last or 'Charge' in last: 
                        ch_count += 1
                        msg = f"<b>𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 𝐂𝐡𝐚𝐫𝐠𝐞 ✅</b>\n{base_msg}"
                        bot.send_message(call.from_user.id, msg, parse_mode='HTML')
                    elif 'Insufficient' in last: 
                        live += 1
                        msg = f"<b>𝐢𝐧𝐬𝐮𝐟𝐟𝐢𝐜𝐢𝐞𝐧𝐭 𝐅𝐮𝐧𝐝𝐬 ☑️</b>\n{base_msg}"
                        bot.send_message(call.from_user.id, msg, parse_mode='HTML')
                    elif 'CVV' in last: 
                        ccnn += 1
                        msgc = f"<b>𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝(CCN) ☑️</b>\n{base_msg}"
                        bot.send_message(call.from_user.id, msgc, parse_mode='HTML')
                    else:
                        dd += 1
                    
                    sleep_time = random.uniform(16, 20)
                    time.sleep(sleep_time)
                    
        except Exception as e:
            print(f"Error in main loop: {e}")
        
        remove_active_scan(user_id)
        
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text='✅ 𝐒𝐂𝐀𝐍 𝐂𝐎𝐌𝐏𝐋𝐄𝐓𝐄𝐃 ✅')
    
    my_thread = threading.Thread(target=my_function)
    my_thread.start()

@bot.callback_query_handler(func=lambda call: call.data.startswith('stop_scan_'))
def stop_scan(call):
    user_id = call.from_user.id
    target_id = int(call.data.split('_')[2])
    if user_id != target_id:
        bot.answer_callback_query(call.id, "❌ هذا الزر ليس مخصص لك!")
        return
    if user_id in active_scans:
        active_scans[user_id]["stop_requested"] = True
        bot.answer_callback_query(call.id, "🛑 جاري إيقاف الفحص...")
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="🛑 **تم طلب إيقاف الفحص، جاري الإيقاف...** 🛑"
        )
    else:
        bot.answer_callback_query(call.id, "❌ لا يوجد فحص نشط للإيقاف")

# أمر الفحص الفردي Stripe
@bot.message_handler(func=lambda message: message.text.lower().startswith('.chk') or message.text.lower().startswith('/chk'))
def respond_to_stripe(message):
    if is_user_banned(message.from_user.id):
        bot.reply_to(message, "🚫 **لقد تم حظرك من استخدام هذا البوت.**\nللتواصل مع المالك: @Joker")
        return
    
    name = message.from_user.first_name
    user = message.from_user.username
    idt = message.from_user.id
    id = message.chat.id
    gate = '𝐒𝐭𝐫𝐢𝐩𝐞 𝐂𝐡𝐚𝐫𝐠𝐞 𝟓$'

    is_vip, _ = is_vip_active(idt)
    if not is_vip and idt != admin:
        if not can_user_check(idt, 1):
            bot.reply_to(message, f"❌ **لقد وصلت للحد الأقصى للفحوصات!**\n📊 الحد الأقصى: {MAX_CHECKS_FREE}\n💎 اشترك VIP للفحص غير المحدود:\n🛒 استخدم /buy")
            return

    current_time = datetime.now()
    try:
        command_usage[idt]['last_time']
    except:
        command_usage[idt] = {'last_time': datetime.now()}
    
    if command_usage[idt]['last_time'] is not None:
        time_diff = (current_time - command_usage[idt]['last_time']).seconds
        if time_diff < 30 and idt != admin:
            bot.reply_to(message, f"<b>Try again after {30-time_diff} seconds.</b>", parse_mode="HTML")
            return
    
    ko = (bot.reply_to(message, "𝐂𝐡𝐞𝐜𝐤𝐢𝐧𝐠 𝐘𝐨𝐮𝐫 𝐂𝐚𝐫𝐝𝐬...⌛").message_id)
    try:
        cc = message.reply_to_message.text
    except:
        cc = message.text
    
    cc = str(reg(cc))
    if cc == 'None':
        bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='''<b>🚫 Oops!
Please ensure you enter the card details in the correct format:
Card: XXXXXXXXXXXXXXXX|MM|YYYY|CVV</b>''', parse_mode="HTML")
        return
    
    if not is_vip and idt != admin:
        update_user_check_count(idt)
        update_user_in_list(idt, user_check_counts.get(str(idt), 0))
    
    start_time = time.time()
    try:
        result = ch(cc)
    except Exception as e:
        result = 'DECLINED'
    
    try:
        data = requests.get('https://bins.antipublic.cc/bins/'+cc[:6]).json()
    except:
        pass
    
    try:
        level = data['level']
    except:
        level = 'Unknown'
    try:
        brand = data['brand']
    except:
        brand = 'Unknown'
    try:
        card_type = data['type']
    except:
        card_type = 'Unknown'
    try:
        country = data['country']
        country_flag = data['country_flag']
    except:
        country = 'Unknown'
        country_flag = 'Unknown'
    try:
        bank = data['bank']
    except:
        bank = 'Unknown'
    
    end_time = time.time()
    execution_time = end_time - start_time
    command_usage[idt]['last_time'] = datetime.now()
    
    # تصنيف النتيجة حسب ردود gatet.py (Stripe)
    if result == 'CHARGED':
        status_text = "𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 𝐂𝐡𝐚𝐫𝐠𝐞 ✅"
    elif result == 'INSUFFICIENT FUNDS':
        status_text = "𝐢𝐧𝐬𝐮𝐟𝐟𝐢𝐜𝐢𝐞𝐧𝐭 𝐅𝐮𝐧𝐝𝐬 💸"
    elif result == 'CVV MISMATCH':
        status_text = "𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝(CCN) ☑️"
    elif result == 'EXPIRED CARD':
        status_text = "𝐄𝐱𝐩𝐢𝐫𝐞𝐝 𝐂𝐚𝐫𝐝 📅"
    elif result == 'SUSPECTED FRAUD':
        status_text = "𝐒𝐮𝐬𝐩𝐞𝐜𝐭𝐞𝐝 𝐅𝐫𝐚𝐮𝐝 ⚠️"
    elif result == 'DO NOT HONOR':
        status_text = "𝐃𝐨 𝐍𝐨𝐭 𝐇𝐨𝐧𝐨𝐫 🚫"
    elif result == 'CLOSED CARD':
        status_text = "𝐂𝐥𝐨𝐬𝐞𝐝 𝐂𝐚𝐫𝐝 🔒"
    elif result == 'CALL ISSUER':
        status_text = "𝐂𝐚𝐥𝐥 𝐈𝐬𝐬𝐮𝐞𝐫 📞"
    elif result == 'PICK UP CARD':
        status_text = "𝐏𝐢𝐜𝐤 𝐔𝐩 𝐂𝐚𝐫𝐝 🃏"
    elif result == '3D SECURE REQUIRED':
        status_text = "𝟑𝐃 𝐒𝐞𝐜𝐮𝐫𝐞 𝐑𝐞𝐪𝐮𝐢𝐫𝐞𝐝 🔐"
    elif result == 'LIMIT EXCEEDED':
        status_text = "𝐋𝐢𝐦𝐢𝐭 𝐄𝐱𝐜𝐞𝐞𝐝𝐞𝐝 📊"
    elif result == 'LOST/STOLEN CARD':
        status_text = "𝐋𝐨𝐬𝐭/𝐒𝐭𝐨𝐥𝐞𝐧 𝐂𝐚𝐫𝐝 🏴"
    elif result == 'ADDRESS MISMATCH':
        status_text = "𝐀𝐝𝐝𝐫𝐞𝐬𝐬 𝐌𝐢𝐬𝐦𝐚𝐭𝐜𝐡 📍"
    elif result == 'PROCESSOR DECLINED':
        status_text = "𝐏𝐫𝐨𝐜𝐞𝐬𝐬𝐨𝐫 𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 🏦"
    elif result == 'INVALID CARD NUMBER':
        status_text = "𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐂𝐚𝐫𝐝 𝐍𝐮𝐦𝐛𝐞𝐫 ❌"
    elif result == 'TRANSACTION NOT ALLOWED':
        status_text = "𝐓𝐫𝐚𝐧𝐬𝐚𝐜𝐭𝐢𝐨𝐧 𝐍𝐨𝐭 𝐀𝐥𝐥𝐨𝐰𝐞𝐝 🚫"
    elif result == 'INVALID CARD':
        status_text = "𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐂𝐚𝐫𝐝 ❌"
    elif result == 'DECLINED':
        status_text = "𝐃𝐄𝐂𝐋𝐈𝐍𝐄𝐃 ❌"
    else:
        status_text = f"𝐃𝐄𝐂𝐋𝐈𝐍𝐄𝐃 ❌ | {result[:40]}"
    
    base_msg = f'''
- - - - - - - - - - - - - - - - - - - - - - -
[ϟ] 𝐆𝐚𝐭𝐞:  {gate}
[ϟ] 𝐂𝐚𝐫𝐝:  <code>{cc}</code> 
[ϟ] 𝐒𝐭𝐚𝐭𝐮𝐬: <b>{status_text}</b>
- - - - - - - - - - - - - - - - - - - - - - - -
[ϟ] 𝐈𝐧𝐟𝐨: <code>{card_type} - {brand}</code>
[ϟ] 𝐁𝐚𝐧𝐤: <code>{bank}</code>
[ϟ] 𝐂𝐨𝐮𝐧𝐭𝐫𝐲: <code>{country} - [{country_flag}]</code>
- - - - - - - - - - - - - - - - - - - - - - - -
[⌥] 𝐓𝐢𝐦𝐞: <code>{"{:.1f}".format(execution_time)}</code> 𝐒𝐞𝐜. || 𝐏𝐫𝐨𝐱𝐲: <code>𝐋𝐢𝐯𝐞</code> ✅
[⎇] 𝐑𝐞𝐪 𝐁𝐲: <a href="tg://resolve?domain={user}">{name}</a> 

- - - - - - - - - - - - - - - - - - - - - - - -
[⌤] 𝐃𝐞𝐯 𝐛𝐲: 𝐉𝐨𝐤𝐞𝐫 🃏'''
    
    bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=f"<b>{status_text}</b>{base_msg}", parse_mode="HTML")

# ==================== أوامر الكود والاشتراك ====================

@bot.message_handler(commands=["code"])
def create_code(message):
    def my_function():
        id = message.from_user.id
        if id != admin:
            return
        try:
            h = float(message.text.split(' ')[1])
            characters = string.ascii_uppercase + string.digits
            pas = 'JOKER-'+''.join(random.choices(characters, k=4))+'-'+''.join(random.choices(characters, k=4))+'-'+''.join(random.choices(characters, k=4))
            current_time = datetime.now()
            ig = current_time + timedelta(hours=h)
            plan = '𝗩𝗜𝗣'
            parts = str(ig).split(':')
            ig = ':'.join(parts[:2])
            with open('data.json', 'r') as json_file:
                existing_data = json.load(json_file)
            new_data = {
                pas: {
                    "plan": plan,
                    "time": ig,
                }
            }
            existing_data.update(new_data)
            with open('data.json', 'w') as json_file:
                json.dump(existing_data, json_file, ensure_ascii=False, indent=4)
            msg = f'''<b>𝐍𝐄𝐖 𝐊𝐄𝐘 𝐂𝐑𝐄𝐀𝐓𝐄𝐃 🌩️
━━━━━━━━━━━━━━━━━━
𝐏𝐋𝐀𝐍 ➜ {plan}
𝐄𝐗𝐏𝐈𝐑𝐄𝐒 𝐈𝐍 ➜ {ig}
𝐊𝐄𝐘 ➜ <code>{pas}</code>
━━━━━━━━━━━━━━━━━━
𝐔𝐒𝐄 /cimo [𝐊𝐄𝐘]</b>'''
            bot.reply_to(message, msg, parse_mode="HTML")
        except Exception as e:
            print('𝐄𝐑𝐑𝐎𝐑 : ', e)
            bot.reply_to(message, f"❌ خطأ: {e}", parse_mode="HTML")
    my_thread = threading.Thread(target=my_function)
    my_thread.start()

@bot.message_handler(commands=["cimo"])
def redeem_code(message):
    def my_function():
        try:
            re = message.text.split(' ')[1]
            with open('data.json', 'r') as file:
                json_data = json.load(file)
            if re not in json_data:
                bot.reply_to(message, '<b>𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐨𝐫 𝐚𝐥𝐫𝐞𝐚𝐝𝐲 𝐮𝐬𝐞𝐝 𝐕𝐈𝐏 𝐜𝐨𝐝𝐞.</b>', parse_mode="HTML")
                return
            timer = json_data[re]['time']
            typ = json_data[re]['plan']
            user_id_str = str(message.from_user.id)
            if user_id_str not in json_data:
                json_data[user_id_str] = {
                    "timer": timer,
                    "plan": typ
                }
            else:
                json_data[user_id_str]['timer'] = timer
                json_data[user_id_str]['plan'] = typ
            del json_data[re]
            with open('data.json', 'w') as file:
                json.dump(json_data, file, indent=2, ensure_ascii=False)
            msg = f'''<b>  𝐕𝐈𝐏 𝐒𝐔𝐁𝐒𝐂𝐑𝐈𝐁𝐄𝐃 ✅
𝐒𝐔𝐁𝐒𝐂𝐑𝐈𝐏𝐓𝐈𝐎𝐍 𝐄𝐗𝐏𝐈𝐑𝐄𝐒 𝐈𝐍 ➜ {timer}
𝐓𝐘𝐏 ➜ {typ}</b>'''
            bot.reply_to(message, msg, parse_mode="HTML")
        except Exception as e:
            print('𝐄𝐑𝐑𝐎𝐑 : ', e)
            bot.reply_to(message, '<b>𝐈𝐧𝐜𝐨𝐫𝐫𝐞𝐜𝐭 𝐜𝐨𝐝𝐞 𝐨𝐫 𝐢𝐭 𝐡𝐚𝐬 𝐚𝐥𝐫𝐞𝐚𝐝𝐲 𝐛𝐞𝐞𝐧 𝐫𝐞𝐝𝐞𝐞𝐦𝐞𝐝</b>', parse_mode="HTML")
    my_thread = threading.Thread(target=my_function)
    my_thread.start()

def add_user(user_id: str, hours: int):
    file_path = "data.json"
    with open(file_path, "r") as f:
        data = json.load(f)
    end_time = (datetime.now() + timedelta(hours=hours)).strftime("%Y-%m-%d %H:%M")
    data[user_id] = {
        "plan": "𝗩𝗜𝗣",
        "timer": end_time
    }
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)
    return end_time

@bot.message_handler(commands=["add"])
def handle_add(message):
    if message.from_user.id != admin:
        bot.reply_to(message, "❌ 𝐓𝐡𝐢𝐬 𝐜𝐨𝐦𝐦𝐚𝐧𝐝 𝐢𝐬 𝐨𝐧𝐥𝐲 𝐟𝐨𝐫 𝐭𝐡𝐞 𝐚𝐝𝐦𝐢𝐧.")
        return
    try:
        parts = message.text.split()
        user_id = parts[1]
        hours = int(parts[2])
        end_time = add_user(user_id, hours)
        bot.reply_to(message, f"✅ 𝐕𝐈𝐏 𝐡𝐚𝐬 𝐛𝐞𝐞𝐧 𝐚𝐜𝐭𝐢𝐯𝐚𝐭𝐞𝐝 𝐟𝐨𝐫 𝐮𝐬𝐞𝐫 `{user_id}` 𝐮𝐧𝐭𝐢𝐥 `{end_time}`", parse_mode="Markdown")
        notify_message = f"""
ﺂﻟﹻٰۧﹷﻘﹻٰۧﹷﻧﹻٰۧﹷﺂص ۦٰ۪۫ﮮٰٰ۪۪۫۫ۦٰ۪۫ۦ 𝗩𝗜𝗣 𝗦𝗨𝗕𝗦𝗖𝗥𝗜𝗕𝗘𝗗 ✅
𝑺𝑼𝑩𝑺𝑪𝑹𝑰𝑷𝑻𝑰𝑶𝑵 𝗘𝗫𝗣𝗜𝗥𝗘𝗦 𝗜𝗡 ➜ {end_time}
𝗧𝗬𝗣 ➜ 𝗩𝗜𝗣
"""
        bot.send_message(chat_id=int(user_id), text=notify_message)
    except Exception as e:
        bot.reply_to(message, f"❌ 𝐄𝐫𝐫𝐨𝐫: {e}")

# ==================== أوامر الأدوات ====================

@bot.message_handler(func=lambda message: message.text.lower().startswith('.gen') or message.text.lower().startswith('/gen'))
def generate_cc(message):
    ko = (bot.reply_to(message, "𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗶𝗻𝗴 𝗰𝗮𝗿𝗱𝘀...⌛", parse_mode="HTML").message_id)
    generate_credit_card(message, bot, ko)

def generate_credit_card(message, bot, ko):
    try: 
        match = re.search(r'(\d{6,16})\D*(\d{1,2}|xx)?\D*(\d{2,4}|xx)?\D*(\d{3,4}|xxx)?', message.text)
        if match:
            card_number = match.group(1)
            start_time = time.time()
            if len(card_number) < 6 or card_number[0] not in ['4', '5', '3', '6']:
                bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='''𝐁𝐈𝐍 𝐧𝐨𝐭 𝐫𝐞𝐜𝐨𝐠𝐧𝐢𝐳𝐞𝐝. 𝐏𝐥𝐞𝐚𝐬𝐞 𝐞𝐧𝐭𝐞𝐫 𝐚 𝐯𝐚𝐥𝐢𝐝 𝐁𝐈𝐍 ❌''', parse_mode="HTML")
                return
            bin = card_number[:6]
            response_message = ""
            for _ in range(10):
                month = int(match.group(2)) if match.group(2) and match.group(2) != 'xx' else random.randint(1, 12)
                year = int(match.group(3)) if match.group(3) and match.group(3) != 'xx' else random.randint(2025, 2029)
                if card_number[:1] == "3":
                    cvv = int(match.group(4)) if match.group(4) and match.group(4) != 'xxx' else random.randint(1000, 9999)
                else:
                    cvv = int(match.group(4)) if match.group(4) and match.group(4) != 'xxx' else random.randint(100, 999)
                credit_card_info = generate_credit_card_info(card_number, month, year, cvv)
                response_message += f"<code>{credit_card_info}</code>\n"
            try:
                data = requests.get(f'https://bins.antipublic.cc/bins/{bin}').json()
                brand = data.get('brand', '𝐔𝐧𝐤𝐧𝐨𝐰𝐧')
                card_type = data.get('type', '𝐔𝐧𝐤𝐧𝐨𝐰𝐧')
                country = data.get('country', '𝐔𝐧𝐤𝐧𝐨𝐰𝐧')
                level = data.get('level', '𝐔𝐧𝐤𝐧𝐨𝐰𝐧')
                country_flag = data.get('country_flag', '𝐔𝐧𝐤𝐧𝐨𝐰𝐧')
                bank = data.get('bank', '𝐔𝐧𝐤𝐧𝐨𝐰𝐧')
            except:
                brand = '𝐔𝐧𝐤𝐧𝐨𝐰𝐧'
                card_type = '𝐔𝐧𝐤𝐧𝐨𝐰𝐧'
                country = '𝐔𝐧𝐤𝐧𝐨𝐰𝐧'
                country_flag = '𝐔𝐧𝐤𝐧𝐨𝐰𝐧'
                bank = '𝐔𝐧𝐤𝐧𝐨𝐰𝐧'
                level = '𝐔𝐧𝐤𝐧𝐨𝐰𝐧'
            bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=f"[⌥] 𝐂𝐂 𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐨𝐫 𝐀𝐩𝐢\n━━━━━━━━━━━━━━\n[⌬] 𝐁𝐢𝐧: <code>{bin}</code> || 𝐄𝐱𝐩𝐢𝐫𝐞: xx|xx || 𝐂𝐯𝐯: xxx\n[⌬] 𝐀𝐦𝐨𝐮𝐧𝐭: 10\n━━━━━━━━━━━━━━\n[⎐] 𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐞𝐝 𝐂𝐚𝐫𝐝𝐬:\n- - - - - - - - - - - - - - - - - - \n{response_message}\n- - - - - - - - - - - - - - - - - - \n[⌬] 𝐁𝐢𝐧 𝐈𝐧𝐟𝐨: {brand} - {card_type} - {level}\n[⌬] 𝐁𝐚𝐧𝐤:  {bank}\n[⌬] 𝐂𝐨𝐮𝐧𝐭𝐫𝐲: {country} - [{country_flag}]\n━━━━━━━━━━━━━━\n[≹] 𝐓𝐢𝐦𝐞: <code>0.00</code> seconds", parse_mode="HTML")
        else:
            bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='''𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐢𝐧𝐩𝐮𝐭. 𝐏𝐥𝐞𝐚𝐬𝐞 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐚 𝐁𝐈𝐍 (𝐁𝐚𝐧𝐤 𝐈𝐝𝐞𝐧𝐭𝐢𝐟𝐢𝐜𝐚𝐭𝐢𝐨𝐧 𝐍𝐮𝐦𝐛𝐞𝐫) 𝐭𝐡𝐚𝐭 𝐢𝐬 𝐚𝐭 𝐥𝐞𝐚𝐬𝐭 𝟔 𝐝𝐢𝐠𝐢𝐭𝐬 𝐛𝐮𝐭 𝐧𝐨𝐭 𝐞𝐱𝐜𝐞𝐞𝐝𝐢𝐧𝐠 𝟏𝟔 𝐝𝐢𝐠𝐢𝐭𝐬. 
𝐄𝐱𝐚𝐦𝐩𝐥𝐞: <code>/gen 412236xxxx |xx|2023|xxx</code>''', parse_mode="HTML")
    except IndexError:
        bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text="𝐁𝐈𝐍 𝐧𝐨𝐭 𝐫𝐞𝐜𝐨𝐠𝐧𝐢𝐳𝐞𝐝. 𝐏𝐥𝐞𝐚𝐬𝐞 𝐞𝐧𝐭𝐞𝐫 𝐚 𝐯𝐚𝐥𝐢𝐝 𝐁𝐈𝐍 ❌")
    except Exception as e:
        bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=f"𝐀𝐧 𝐞𝐫𝐫𝐨𝐫 𝐨𝐜𝐜𝐮𝐫𝐫𝐞𝐝: {str(e)}")

def generate_credit_card_info(card_number, expiry_month, expiry_year, cvv):
    generated_num = str(card_number)
    if card_number[:1] == "5" or card_number[:1] == "4" or card_number[:1] == "6":
        while len(generated_num) < 15:
            generated_num += str(random.randint(0, 9))
        check_digit = generate_check_digit(generated_num)
        credit_card_number = generated_num + str(check_digit)
        return f"{credit_card_number}|{str(expiry_month).zfill(2)}|{str(expiry_year)[-2:]}|{cvv}"
    elif card_number[:1] == "3":
        while len(generated_num) < 14:
            generated_num += str(random.randint(0, 9))
        check_digit = generate_check_digit(generated_num)
        credit_card_number = generated_num + str(check_digit)
        return f"{credit_card_number}|{str(expiry_month).zfill(2)}|{str(expiry_year)[-2:]}|{cvv}"

def generate_check_digit(num):
    num_list = [int(x) for x in num]
    for i in range(len(num_list) - 1, -1, -2):
        num_list[i] *= 2
        if num_list[i] > 9:
            num_list[i] -= 9
    return (10 - sum(num_list) % 10) % 10

@bot.message_handler(func=lambda message: message.text.lower().startswith('.bin') or message.text.lower().startswith('/bin'))
def bin_lookup(message):
    user = message.from_user.username
    name = message.from_user.first_name
    try:
        bm = message.reply_to_message.text
    except:
        bm = message.text
    regex = r'\d+'
    try:
        matches = re.findall(regex, bm)
    except:
        bot.reply_to(message, '🚫 Incorrect input. Please provide a 6-digit BIN number.', parse_mode="HTML")
        return
    bin = ''.join(matches)[:6]
    ko = bot.reply_to(message, "𝗖𝗵𝗲𝗰𝗸𝗶𝗻𝗴 𝗬𝗼𝘂𝗿 𝗯𝗶𝗻...⌛", parse_mode="HTML").message_id
    if len(bin) >= 6:
        try:
            data = requests.get(f'https://bins.antipublic.cc/bins/{bin}').json()
            brand = data.get('brand', 'Unknown')
            card_type = data.get('type', 'Unknown')
            country = data.get('country_name', 'Unknown')
            country_flag = data.get('country_flag', '🏳️')
            bank = data.get('bank', 'Unknown')
            msg = f'''
[⌥] 𝐁𝐈𝐍 𝐥𝐨𝐨𝐤𝐮𝐩 𝐀𝐩𝐢
━━━━━━━━━━━━━━━━━
[⌬] 𝐁𝐈𝐍 ⇢ <code>{bin}</code>
[⌬] 𝐈𝐧𝐟𝐨 ⇢ {card_type} - {brand}  
[⌬] 𝐈𝐬𝐬𝐮𝐞𝐫 ⇢  {bank}
[⌬] 𝐂𝐨𝐮𝐧𝐭𝐫𝐲 ⇢ {country} - [{country_flag}]
━━━━━━━━━━━━━━━━━
[⎇] 𝐑𝐞𝐪 𝐁𝐲: <a href="tg://resolve?domain={user}">{name}</a>'
 '''
        except:
            msg = '𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐁𝐈𝐍 ❌'
    else:
        msg = '🚫 Incorrect input. Please provide a 6-digit BIN number.'
    bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=msg, parse_mode="HTML")

@bot.message_handler(func=lambda message: message.text.lower().startswith('.fake') or message.text.lower().startswith('/fake'))
def fake_address(message):
    def my_function():
        try:
            try:
                u = message.text.split('fake ')[1]
            except:
                u = 'US'
            parsed_data = requests.get(f'https://randomuser.me/api/?nat={u}').json()
            results = parsed_data['results']
            result = results[0]
            name = f"{result['name']['title']} {result['name']['first']} {result['name']['last']}"
            street_number = result['location']['street']['number']
            street_name = result['location']['street']['name']
            city = result['location']['city']
            state = result['location']['state']
            country = result['location']['country']
            postcode = result['location']['postcode']
            fake = Faker()
            phone = fake.phone_number()
            email = fake.email()
            user = message.from_user.username
            name = message.from_user.first_name
            formatted_address = f"""<b>
[⌥] 𝐅𝐚𝐤𝐞 𝐀𝐝𝐝𝐫𝐞𝐬𝐬 𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐨𝐫
━━━━━━━━━━━━
[↯] 𝐍𝐚𝐦𝐞: <code>{name}</code>
[↯] 𝐒𝐭𝐫𝐞𝐞𝐭: <code>{street_number} {street_name}</code>                         
[↯] 𝐂𝐢𝐭𝐲: <code>{city}</code>
[↯] 𝐒𝐭𝐚𝐭𝐞: <code>{state}</code>
[↯] 𝐂𝐨𝐮𝐧𝐭𝐫𝐲: <code>{country}</code>
[↯] 𝐏𝐨𝐬𝐭𝐚𝐥 𝐂𝐨𝐝𝐞: <code>{postcode}</code>
[↯] 𝐏𝐡𝐨𝐧𝐞 𝐍𝐨.: <code>{phone}</code>
[↯] 𝐄𝐦𝐚𝐢𝐥: <code>{email}</code></b> [Inbox]
━━━━━━━━━━━━
[≹] 𝐓𝐢𝐦𝐞: 0.15 seconds
[⎇] 𝐑𝐞𝐪 𝐁𝐲: <a href="tg://resolve?domain={user}">{name}</a> [Free user]
            """
            bot.reply_to(message, formatted_address, parse_mode="HTML")
        except:
            bot.reply_to(message, "Country code not found or not available.")
    my_thread = threading.Thread(target=my_function)
    my_thread.start()

print("𝐉𝐨𝐤𝐞𝐫 𝐁𝐨𝐭 𝐢𝐬 𝐫𝐮𝐧𝐧𝐢𝐧𝐠... 🃏")
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"حدث خطأ: {e}")
        time.sleep(5)