import logging
import sys
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from GetOneTimeCode import getOneTimeCode
from config import BOT_TOKEN, LOG_LEVEL, AUTHORIZED_USERS, RESTRICT_ACCESS

# Устанавливаем кодировку UTF-8 для вывода
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, LOG_LEVEL)
)

# Получаем логгер
logger = logging.getLogger(__name__)

def check_authorization(update: Update) -> bool:
    """Проверяет, авторизован ли пользователь"""
    if not RESTRICT_ACCESS:
        return True
    
    user_id = update.effective_user.id
    if user_id in AUTHORIZED_USERS:
        return True
    
    logger.warning(f"Unauthorized access from user {user_id} ({update.effective_user.username})")
    return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    if not check_authorization(update):
        await update.message.reply_text(
            "❌ У вас нет доступа к этому боту.\n"
            "Обратитесь к администратору для получения доступа."
        )
        return
    
    user = update.effective_user
    await update.message.reply_text(
        f"Привет, {user.first_name}! 👋\n\n"
        "Я бот для получения Steam Guard кодов.\n"
        "Используйте команду /code <имя_аккаунта> для получения кода.\n\n"
        "Для справки используйте /help"
    )

async def get_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /code"""
    if not check_authorization(update):
        await update.message.reply_text(
            "❌ У вас нет доступа к этому боту.\n"
            "Обратитесь к администратору для получения доступа."
        )
        return
    
    if not context.args:
        await update.message.reply_text(
            "Пожалуйста, укажите имя аккаунта.\n"
            "Пример: /code account_name"
        )
        return
    
    account_name = context.args[0]
    
    try:
        # Получаем код
        code = getOneTimeCode(account_name)
        
        if code is None:
            await update.message.reply_text(
                f"❌ Не удалось получить код для аккаунта '{account_name}'.\n"
                "Проверьте, что аккаунт существует в папке accounts/ или accountStash/"
            )
        else:
            await update.message.reply_text(
                f"✅ Код для аккаунта '{account_name}': `{code}`",
                parse_mode='Markdown'
            )
            
    except Exception as e:
        logger.error(f"Error getting code: {e}")
        await update.message.reply_text(
            f"❌ Произошла ошибка при получении кода: {str(e)}"
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help"""
    if not check_authorization(update):
        await update.message.reply_text(
            "❌ У вас нет доступа к этому боту.\n"
            "Обратитесь к администратору для получения доступа."
        )
        return
    
    help_text = """
🤖 *Steam Guard Bot*

*Доступные команды:*
/start - Начать работу с ботом
/code <имя_аккаунта> - Получить Steam Guard код для указанного аккаунта
/help - Показать эту справку
/myid - Показать ваш ID (для настройки авторизации)

*Пример использования:*
`/code my_steam_account`

*Примечание:* Убедитесь, что файл Steamguard.txt существует в папке accounts/ или accountStash/ для указанного аккаунта.
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def my_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показывает ID пользователя (для настройки авторизации)"""
    user = update.effective_user
    await update.message.reply_text(
        f"🆔 Ваш ID: `{user.id}`\n\n"
        "Для получения доступа к боту, отправьте этот ID администратору.",
        parse_mode='Markdown'
    )

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик ошибок"""
    logger.error(f"Error processing update: {context.error}")
    if update and hasattr(update, 'message') and update.message:
        await update.message.reply_text(
            "❌ Произошла ошибка при обработке команды. Попробуйте позже."
        )

def main() -> None:
    """Запуск бота"""
    try:
        print("🤖 Starting bot...")
        
        # Проверяем токен
        if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" or not BOT_TOKEN:
            print("❌ Error: Bot token is required!")
            print("1. Get token from @BotFather in Telegram")
            print("2. Add token to .env file")
            return
        
        print(f"✅ Token loaded: {BOT_TOKEN[:10]}...")
        
        # Создаем приложение
        print("🔧 Creating application...")
        application = Application.builder().token(BOT_TOKEN).build()

        # Добавляем обработчики команд
        print("📝 Registering command handlers...")
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("code", get_code))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("myid", my_id))
        
        # Добавляем обработчик ошибок
        application.add_error_handler(error_handler)

        # Запускаем бота
        print("🤖 Bot started...")
        if RESTRICT_ACCESS:
            print(f"🔒 Authorization mode: ENABLED")
            print(f"👥 Authorized users: {AUTHORIZED_USERS}")
        else:
            print("🔓 Authorization mode: DISABLED (access for all)")
        print("📱 Send /start in Telegram to begin")
        print("⏹️ Press Ctrl+C to stop")
        
        # Запускаем polling
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Critical error: {e}")
        logger.error(f"Critical error starting bot: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main() 