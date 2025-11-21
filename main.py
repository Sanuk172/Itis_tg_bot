from telegram_bot import TelegramBot
from bot_database import BotDatabase
from my_token import TOKEN_TG


def main():
    # Инициализация базы данных
    db = BotDatabase()

    # Ваш токен бота (замените на реальный)
    BOT_TOKEN = TOKEN_TG

    # Создание и запуск бота
    bot = TelegramBot(BOT_TOKEN, db)
    bot.run()


if __name__ == "__main__":
    main()
