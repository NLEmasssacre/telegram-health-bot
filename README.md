# Telegram Health & Wellness Bot

Автоматический бот для публикации постов о здоровом образе жизни в Telegram-канал.

## Функциональность

- Ежедневная публикация постов в 10:00 МСК
- Автоматическая генерация контента через OpenRouter API
- Тематика: ЗОЖ, ПП, мотивация, истории, полезные привычки, лайфхаки, интересные факты, рецепты
- Команды для управления: /newpost, /status, /log

## Установка и запуск на macOS

1. Убедитесь, что у вас установлен Python 3.8 или выше:
```bash
python3 --version
```

2. Клонируйте репозиторий:
```bash
git clone https://github.com/NLEmasssacre/telegram-health-bot.git
cd telegram-health-bot
```

3. Создайте и активируйте виртуальное окружение:
```bash
python3 -m venv venv
source venv/bin/activate
```

4. Создайте файл .env в корневой директории проекта:
```bash
touch .env
```

5. Откройте .env в текстовом редакторе и добавьте следующие переменные:
```
BOT_TOKEN=your_bot_token
OPENROUTER_API_KEY=your_openrouter_api_key
WEBHOOK_URL=your_webhook_url
PORT=8080
```

6. Установите зависимости:
```bash
pip3 install -r requirements.txt
```

7. Запустите бота:
```bash
python3 bot.py
```

## Деплой на Render

1. Создайте аккаунт на [Render](https://render.com)
2. Подключите ваш GitHub репозиторий
3. Создайте новый Web Service
4. В настройках сервиса добавьте переменные окружения из .env файла
5. Render автоматически определит конфигурацию из render.yaml

## Команды бота

- `/newpost` - Сгенерировать и отправить новый пост
- `/status` - Проверить статус бота
- `/log` - Показать последние логи

## Технологии

- Python 3.8+
- python-telegram-bot
- OpenRouter API
- APScheduler
- Render (хостинг)

## Примечания для macOS

- Если у вас не установлен Python, вы можете установить его через Homebrew:
```bash
brew install python3
```

- Если у вас не установлен Git, установите его через Homebrew:
```bash
brew install git
```

- Для удобной работы с .env файлом можно использовать Visual Studio Code:
```bash
code .env
``` 