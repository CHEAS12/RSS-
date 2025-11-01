#!/usr/bin/env python3
"""Главный файл запуска Telegram RSS бота с обучением структурированию постов."""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from telegram_bot import TelegramRSSBot
from rss_formatter import RSSFormatter
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

# Обучающий промпт для AI
TELEGRAM_POST_STRUCTURE_PROMPT = """Ты - эксперт по оформлению постов в Telegram. Следуй этим правилам:

**СТРУКТУРА ПОСТА:**
1. Начинай с ЯРКОГО заголовка (жирный текст), отделяй двумя переносами строки
2. Делай короткие абзацы по 2-3 предложения
3. Разделяй абзацы пустыми строками
4. Заканчивай призывом к действию (CTA)

**ФОРМАТИРОВАНИЕ:**
- *Жирный* для важного
- _Курсив_ для примеров
- `Моноширинный` для кода

**ЭМОДЗИ:** 2-3 максимум, для списков
**ВОВЛЕЧЁННОСТЬ:** Заголовок = 50% успеха
**ДЛИНА:** 300-800 символов оптимально
"""


async def main():
    try:
        logger.info("🚀 Запуск Telegram RSS Bot...")

        formatter = RSSFormatter(ai_enhance=True,
                                 enable_emojis=True,
                                 enable_link_preview=False,
                                 style="enhanced")

        logger.info("✅ AI обучен структурировать посты")

        bot = TelegramRSSBot()
        logger.info("✅ Бот инициализирован")

        while True:
            await asyncio.sleep(60)

    except KeyboardInterrupt:
        logger.info("⏹️ Остановка бота")
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
