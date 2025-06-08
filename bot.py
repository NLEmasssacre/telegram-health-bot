import os
import logging
import json
import requests
from datetime import datetime, time
import pytz
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Constants
BOT_TOKEN = os.getenv('BOT_TOKEN')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
PORT = int(os.getenv('PORT', 8080))
CHANNEL_ID = '@notonlypoke'

# OpenRouter API configuration
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "anthropic/claude-3-opus-20240229"

async def generate_post():
    """Generate a post using OpenRouter API"""
    if not OPENROUTER_API_KEY:
        logger.error("OPENROUTER_API_KEY is not set in environment variables")
        return None

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/NLEmasssacre/telegram-health-bot",  # Required by OpenRouter
        "X-Title": "Telegram Health Bot"  # Required by OpenRouter
    }
    
    prompt = """Создай интересный пост для Telegram-канала о здоровом образе жизни. 
    Тема может быть связана с: ЗОЖ, правильным питанием, мотивацией, историями успеха, 
    полезными привычками, лайфхаками, интересными фактами или рецептами.
    Пост должен быть написан на русском языке, быть информативным и мотивирующим.
    Максимальная длина: 2000 символов."""
    
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "Ты - эксперт по здоровому образу жизни и созданию мотивирующего контента."},
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        logger.info("Sending request to OpenRouter API...")
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        logger.info("Successfully received response from OpenRouter API")
        return result['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        logger.error(f"Error generating post: {str(e)}")
        if hasattr(e.response, 'text'):
            logger.error(f"Response text: {e.response.text}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error generating post: {str(e)}")
        return None

async def send_post(context: ContextTypes.DEFAULT_TYPE):
    """Send generated post to the channel"""
    try:
        post = await generate_post()
        if post:
            await context.bot.send_message(chat_id=CHANNEL_ID, text=post)
            logger.info("Post successfully sent to channel")
        else:
            logger.error("Failed to generate post")
            await context.bot.send_message(chat_id=CHANNEL_ID, text="❌ Не удалось сгенерировать пост. Пожалуйста, попробуйте позже.")
    except Exception as e:
        logger.error(f"Error sending post: {e}")
        await context.bot.send_message(chat_id=CHANNEL_ID, text="❌ Произошла ошибка при отправке поста. Пожалуйста, попробуйте позже.")

async def newpost(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /newpost command"""
    await update.message.reply_text("🔄 Генерирую новый пост...")
    await send_post(context)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command"""
    status_text = "🤖 Бот активен и работает\n"
    status_text += f"📅 Последний пост: {datetime.now(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M:%S')}"
    await update.message.reply_text(status_text)

async def log(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /log command"""
    try:
        with open('bot.log', 'r') as f:
            logs = f.readlines()[-50:]  # Get last 50 lines
        log_text = "".join(logs)
        await update.message.reply_text(f"Последние логи:\n```\n{log_text}\n```", parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text(f"Ошибка при чтении логов: {e}")

def main():
    """Start the bot"""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("newpost", newpost))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("log", log))

    # Set up scheduler for daily posts
    scheduler = AsyncIOScheduler()
    moscow_tz = pytz.timezone('Europe/Moscow')
    
    # Create a context for the scheduler
    async def scheduled_job():
        context = ContextTypes.DEFAULT_TYPE()
        context.bot = application.bot
        await send_post(context)
    
    scheduler.add_job(scheduled_job, 'cron', hour=10, minute=0, timezone=moscow_tz)
    scheduler.start()

    # Get the webhook URL from environment
    webhook_url = os.getenv('WEBHOOK_URL')
    if not webhook_url:
        logger.error("WEBHOOK_URL environment variable is not set")
        return

    # Start the webhook
    application.run_webhook(
        listen='0.0.0.0',
        port=PORT,
        webhook_url=webhook_url,
        cert=None,  # No SSL certificate needed as Render provides HTTPS
        key=None,   # No SSL key needed as Render provides HTTPS
    )

if __name__ == '__main__':
    main() 