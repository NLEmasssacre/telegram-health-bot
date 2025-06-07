import os
import httpx
from dotenv import load_dotenv

load_dotenv()

class ContentGenerator:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://notonlypoke.com",
            "Content-Type": "application/json"
        }

    async def generate_topic(self) -> str:
        prompt = """Сгенерируй интересную тему для поста в Telegram-канале о здоровом образе жизни, 
        правильном питании или мотивации. Тема должна быть актуальной и привлекательной. 
        Ответь только темой, без дополнительных пояснений."""

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.base_url,
                headers=self.headers,
                json={
                    "model": "openai/gpt-4-turbo-preview",
                    "messages": [{"role": "user", "content": prompt}]
                }
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()

    async def generate_post(self, topic: str) -> str:
        prompt = f"""Напиши экспертный пост на тему: {topic}
        
        Требования:
        - Длина до 2000 символов
        - Профессиональный, но понятный язык
        - Полезная информация для читателей
        - Структурированный текст с абзацами
        - Можно добавить практические советы или рецепты
        - Пиши на русском языке
        
        Формат: только текст поста, без заголовков и дополнительных пояснений."""

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.base_url,
                headers=self.headers,
                json={
                    "model": "openai/gpt-4-turbo-preview",
                    "messages": [{"role": "user", "content": prompt}]
                }
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()

    async def generate_full_post(self) -> tuple[str, str]:
        topic = await self.generate_topic()
        content = await self.generate_post(topic)
        return topic, content 