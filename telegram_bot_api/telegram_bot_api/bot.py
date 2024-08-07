import os
import django
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from django.conf import settings

# Django ayarlarını yükle
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "telegram_bot_project.settings")
django.setup()

from users.models import User

# Telegram bot token'ınızı buraya ekleyin
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

def start(update, context):
  telegram_user_id = update.effective_user.id
  username = update.effective_user.username

  user, created = User.objects.get_or_create(
      telegram_user_id=telegram_user_id,
      defaults={'username': username}
  )

  if created:
      message = f"Hoş geldiniz! Referans linkiniz: {settings.BASE_URL}/ref/{user.referral_link}"
  else:
      message = "Tekrar hoş geldiniz!"

  update.message.reply_text(message)

def main():
  updater = Updater(TOKEN, use_context=True)
  dp = updater.dispatcher

  dp.add_handler(CommandHandler("start", start))

  updater.start_polling()
  updater.idle()

if __name__ == '__main__':
  main()