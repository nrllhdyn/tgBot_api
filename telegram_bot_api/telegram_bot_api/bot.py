import os
import django
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from django.conf import settings

# Django ayarlarını yükle
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "telegram_bot_project.settings")
django.setup()

from users.models import User
from referrals.models import Referral
from referrals.utils import generate_referral_link

# Telegram bot token'ınızı buraya ekleyin
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

def start(update, context):
    telegram_user_id = update.effective_user.id
    username = update.effective_user.username
    args = context.args

    user, created = User.objects.get_or_create(
        telegram_user_id=telegram_user_id,
        defaults={'username': username}
    )

    if args and args[0].isdigit():
        referrer_id = int(args[0])
        try:
            referrer = User.objects.get(id=referrer_id)
            if referrer != user and not Referral.objects.filter(referrer=referrer, referred=user).exists():
                Referral.objects.create(referrer=referrer, referred=user)
                update.message.reply_text(f"Sizi {referrer.username} davet etti!")
        except User.DoesNotExist:
            pass

    referral_link = generate_referral_link(user.id, context.bot.username)

    if created:
        message = f"Hoş geldiniz! Referans linkiniz: {referral_link}"
    else:
        message = f"Tekrar hoş geldiniz! Referans linkiniz: {referral_link}"

    update.message.reply_text(message)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()