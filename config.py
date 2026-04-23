import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Получаем токен бота из переменной окружения или используем значение по умолчанию
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

# Другие настройки
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Авторизованные пользователи (ID пользователей Telegram)
# Получить ID можно через @userinfobot в Telegram
AUTHORIZED_USERS = os.getenv('AUTHORIZED_USERS', '').split(',')
AUTHORIZED_USERS = [int(user_id.strip()) for user_id in AUTHORIZED_USERS if user_id.strip().isdigit()]

# Режим авторизации (True - только авторизованные пользователи, False - все пользователи)
RESTRICT_ACCESS = os.getenv('RESTRICT_ACCESS', 'True').lower() == 'true' 