import sqlite3
from datetime import datetime, timedelta


class BotDatabase:
    def __init__(self, db_name='telegram_bot.db'):
        self.connection = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        """Создает таблицы пользователей и сообщений"""
        cursor = self.connection.cursor()

        # Таблица пользователей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT
            )
        ''')

        # Таблица с ошибками в тесте
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_test_errors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                present_simple INTEGER,
                present_continuous INTEGER,
                present_perfect INTEGER,
                past_simple INTEGER,
                past_continuous INTEGER,
                past_perfect INTEGER,
                future_simple INTEGER,
                future_continuous INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')

        # Таблица с ошибками в словах
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS user_words_errors (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(user_id)
                    )
                ''')

        self.connection.commit()

    def user_exists(self, user_id):
        """Проверяет существование пользователя в базе данных"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE user_id = ?", (user_id,))
        count = cursor.fetchone()[0]
        return count > 0

    def add_user(self, user_id, username, first_name):
        """Добавляет нового пользователя"""
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO users (user_id, username, first_name, activity_duration) VALUES (?, ?, ?, ?)",
            (user_id, username, first_name, 0)
        )
        self.connection.commit()

    def save_message(self, user_id, message_text):
        """Сохраняет сообщение пользователя"""
        cursor = self.connection.cursor()
        cursor.execute(
            'SELECT * FROM user_messages WHERE user_id = ?', (user_id,)
        )
        messages = cursor.fetchall()

        messages_dates = []
        date_today = (datetime.today() - timedelta(hours=5)).date()

        for i in messages:
            messages_dates.append(i[3][:10])
        if str(date_today) not in messages_dates:
            cursor.execute('UPDATE users SET activity_duration = activity_duration + 1 WHERE user_id = ?', (user_id,))
        self.connection.commit()



        cursor.execute(
            "INSERT INTO user_messages (user_id, message_text) VALUES (?, ?)",
            (user_id, message_text)
        )
        self.connection.commit()

    def get_statistics(self, user_id):
        """Получат статистику пользователя из таблиц"""
        cursor = self.connection.cursor()
        cursor.execute(
            'SELECT * FROM user_messages WHERE user_id = ?', (user_id,)
        )
        messages = cursor.fetchall()
        cursor.execute(
            'SELECT * FROM users WHERE user_id = ?', (user_id,)
        )
        user_info = cursor.fetchone()
        return (messages, user_info)