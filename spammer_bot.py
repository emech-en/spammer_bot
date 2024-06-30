import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import time
import os
import asyncio

# تنظیم لاگینگ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# تنظیمات اسپم
PERSONAL_MAX_PER_MINUTE = int(os.environ.get('PERSONAL_MAX_PER_MINUTE', 5))
FORWARD_MAX_PER_HOUR = int(os.environ.get('FORWARD_MAX_PER_HOUR', 1))
FORWARD_MAX_PER_FIVE_HOURS = int(os.environ.get('FORWARD_MAX_PER_FIVE_HOURS', 3))
WARNING_COOLDOWN = int(os.environ.get('WARNING_COOLDOWN', 3600))

# ذخیره اطلاعات پیام‌های کاربران و زمان آخرین هشدار
user_messages = {}
user_last_warning = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "سلام! من یک ربات ضد اسپم هستم که با استفاده از هوش مصنوعی ساخته شده‌ام. "
        "وظیفه من محافظت از این گروه در برابر پیام‌های اسپم و ناخواسته است.\n\n"
        "قوانین و محدودیت‌های اعمال شده توسط من به شرح زیر است:\n"
        f"1. حداکثر {PERSONAL_MAX_PER_MINUTE} پیام شخصی در هر دقیقه مجاز است.\n"
        f"2. حداکثر {FORWARD_MAX_PER_HOUR} پیام فوروارد شده در هر ساعت مجاز است.\n"
        f"3. حداکثر {FORWARD_MAX_PER_FIVE_HOURS} پیام فوروارد شده در هر 5 ساعت مجاز است.\n"
        f"4. در صورت تشخیص اسپم، پیام‌های اضافی حذف خواهند شد.\n"
        f"5. هشدارها هر {WARNING_COOLDOWN // 3600} ساعت یکبار صادر می‌شوند.\n\n"
        "لطفاً به این قوانین احترام بگذارید تا محیطی سالم و مفید برای همه اعضا فراهم شود. "
        "در صورت رعایت نکردن این قوانین، ممکن است دسترسی شما به ارسال پیام محدود شود.\n\n"
        "با تشکر از همکاری شما!"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_message)


async def check_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    current_time = time.time()

    if user_id not in user_messages:
        user_messages[user_id] = {'personal': [], 'forward': []}

    is_forward = update.message.forward_date is not None

    if is_forward:
        is_spam = check_forward_spam(user_id, current_time)
    else:
        is_spam = check_personal_spam(user_id, current_time)

    if is_spam:
        await delete_and_warn(update, context, user_id, current_time)
        return True
    return False


def check_personal_spam(user_id, current_time):
    user_messages[user_id]['personal'] = [t for t in user_messages[user_id]['personal'] if current_time - t < 60]
    user_messages[user_id]['personal'].append(current_time)
    return len(user_messages[user_id]['personal']) > PERSONAL_MAX_PER_MINUTE


def check_forward_spam(user_id, current_time):
    # حذف پیام‌های قدیمی‌تر از 5 ساعت
    user_messages[user_id]['forward'] = [t for t in user_messages[user_id]['forward'] if current_time - t < 5 * 3600]

    # بررسی محدودیت 5 ساعته
    if len(user_messages[user_id]['forward']) >= FORWARD_MAX_PER_FIVE_HOURS:
        return True

    # بررسی محدودیت ساعتی
    hour_messages = [t for t in user_messages[user_id]['forward'] if current_time - t < 3600]
    if len(hour_messages) >= FORWARD_MAX_PER_HOUR:
        return True

    # اگر اسپم نیست، پیام جدید را اضافه کن
    user_messages[user_id]['forward'].append(current_time)
    return False


async def delete_and_warn(update, context, user_id, current_time):
    await update.message.delete()

    last_warning_time = user_last_warning.get(user_id, 0)
    if current_time - last_warning_time >= WARNING_COOLDOWN:
        username = update.message.from_user.username
        warning = f"@{username}، شما در حال ارسال اسپم هستید. لطفاً از ارسال پیام‌های مکرر خودداری کنید."
        await context.bot.send_message(chat_id=update.effective_chat.id, text=warning)
        user_last_warning[user_id] = current_time


def main():
    bot_token = os.environ.get('BOT_TOKEN')
    if not bot_token:
        raise ValueError("لطفاً توکن ربات را در متغیر محیطی BOT_TOKEN تنظیم کنید.")

    application = ApplicationBuilder().token(bot_token).build()

    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(filters.ALL & (~filters.COMMAND), check_spam)

    application.add_handler(start_handler)
    application.add_handler(message_handler)

    application.run_polling()


if __name__ == '__main__':
    asyncio.run(main())
