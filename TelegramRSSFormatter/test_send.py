import sys
import os
# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import json
import feedparser
from rss_formatter import RSSFormatter
from telegram_bot import TelegramRSSBot

print("✅ Загрузка конфигурации...")
with open('config.json', 'r', encoding='utf-8') as f:
    config_data = json.load(f)

print("✅ Инициализация...")
formatter = RSSFormatter(ai_enhance=True, enable_emojis=True, style="enhanced")
bot = TelegramRSSBot(config_data['telegram_bot_token'])

feed_config = config_data['feeds'][0]
feed_url = feed_config['url']

print(f"\n🌐 RSS лента: {feed_url}")
print(f"📢 Канал: {feed_config['chat_ids'][0]}")

print("\n🔄 Получение постов...")
feed = feedparser.parse(feed_url)

if feed.entries:
    entry = feed.entries[0]
    print(f"\n📝 Пост: {entry.title}")
    print(f"🔗 Ссылка: {entry.link}")

    print("\n⚙️ Форматирование с AI...")
    formatted_post = formatter.format_from_feedparser_entry(entry, feed_config)

    print("\n" + "="*50)
    print("📤 ОТФОРМАТИРОВАННЫЙ ПОСТ")
    print("="*50)
    print(formatted_post.content)
    print("="*50)

    print("\n📨 Отправка в Telegram...")
    chat_id = feed_config['chat_ids'][0]
    bot.send_post(chat_id, formatted_post, feed_config)

    print("\n✅ Тестовый пост успешно отправлен!")
else:
    print("❌ Нет постов в RSS-ленте")