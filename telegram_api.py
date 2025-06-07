import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
from content_generator import ContentGenerator

load_dotenv()

class TelegramBot:
    def __init__(self):
        self.bot = Bot(token=os.getenv("BOT_TOKEN"))
        self.dp = Dispatcher()
        self.channel_id = os.getenv("CHANNEL_ID")
        self.content_generator = ContentGenerator()
        
        # Register command handlers
        self.dp.message.register(self.cmd_start, Command("start"))
        self.dp.message.register(self.cmd_newpost, Command("newpost"))

    async def cmd_start(self, message: types.Message):
        await message.answer(
            "👋 Привет! Я бот для автоматической публикации постов в канал @notonlypoke.\n\n"
            "Доступные команды:\n"
            "/start - показать это сообщение\n"
            "/newpost - сгенерировать и опубликовать новый пост"
        )

    async def cmd_newpost(self, message: types.Message):
        await message.answer("🔄 Генерирую новый пост...")
        try:
            topic, content = await self.content_generator.generate_full_post()
            post_text = f"📌 {topic}\n\n{content}"
            
            await self.bot.send_message(
                chat_id=self.channel_id,
                text=post_text
            )
            await message.answer("✅ Пост успешно опубликован в канал!")
        except Exception as e:
            await message.answer(f"❌ Произошла ошибка при публикации поста: {str(e)}")

    async def publish_scheduled_post(self):
        try:
            topic, content = await self.content_generator.generate_full_post()
            post_text = f"📌 {topic}\n\n{content}"
            
            await self.bot.send_message(
                chat_id=self.channel_id,
                text=post_text
            )
            return True
        except Exception as e:
            print(f"Error publishing scheduled post: {str(e)}")
            return False

    async def start(self):
        await self.dp.start_polling(self.bot) 