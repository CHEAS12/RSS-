# Telegram RSS Formatter with RSStT Standard

AI-powered RSS to Telegram bot that formats feed posts following the RSStT standard using OpenAI GPT-5.

## Features

- **RSStT Standard Formatting**: Clean, professional message formatting following the RSStT bot standard
- **AI Enhancement**: Uses OpenAI GPT-5 to generate engaging titles and well-formatted content
- **Flexible Configuration**: Customize emojis, hashtags, link previews, and media attachments per feed
- **Multi-Feed Support**: Monitor multiple RSS feeds with different settings
- **Media Support**: Automatically includes images, videos, and other media from RSS feeds
- **Telegram Integration**: Sends formatted posts to Telegram channels or chats

## RSStT Format

The bot formats messages in the RSStT standard:

```
**Post Title** 📰

#hashtag1 #hashtag2

Post content goes here, cleanly formatted and easy to read...

_Author: Author Name_

[Feed Name](https://link-to-post.com)
```

## Setup

### 1. Configure Secrets

You need the following secrets:
- `OPENAI_API_KEY`: Your OpenAI API key
- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token (get from @BotFather)
- `TELEGRAM_CHAT_ID` (optional): Default chat ID for testing

### 2. Configure Feeds

Create a `config.json` file (see `config.example.json`):

```json
{
  "telegram_bot_token": "YOUR_TOKEN",
  "openai_api_key": "YOUR_KEY",
  "default_check_interval": 300,
  "feeds": [
    {
      "url": "https://example.com/rss",
      "name": "Example Feed",
      "chat_ids": ["@your_channel"],
      "check_interval": 300,
      "enable_emojis": true,
      "custom_hashtags": ["RSS", "News"],
      "enable_link_preview": true,
      "enable_media": true,
      "show_author": true,
      "ai_enhance": true
    }
  ]
}
```

Alternatively, use environment variables:
- `TELEGRAM_BOT_TOKEN`
- `OPENAI_API_KEY`
- `RSS_FEEDS`: JSON array of feed configurations

### 3. Run

```bash
python main.py
```

Or with a custom config file:

```bash
python main.py config.json
```

## Usage

### AIFormatterRSStT Class

```python
from src.rss_formatter import AIFormatterRSStT, RSSPost

formatter = AIFormatterRSStT(
    enable_emojis=True,
    custom_hashtags=["RSS", "Tech"],
    enable_link_preview=True,
    enable_media=True,
    show_author=True,
    ai_enhance=True
)

post = RSSPost(
    title="Article Title",
    author="Author Name",
    summary="Article summary...",
    link="https://example.com/article",
    feed_title="Example Feed"
)

formatted = formatter.format_post(post)
print(formatted["message"])
```

### Telegram Bot

```python
from src.telegram_bot import TelegramRSSBot
import asyncio

bot = TelegramRSSBot()

async def send_message():
    await bot.send_message(
        chat_id="@your_channel",
        message="**Hello World**\n\nTest message",
        parse_mode="Markdown"
    )

asyncio.run(send_message())
```

## Configuration Options

### Feed Settings

- `url`: RSS feed URL (required)
- `name`: Display name for the feed (required)
- `chat_ids`: List of Telegram chat IDs or channel usernames (required)
- `check_interval`: Check interval in seconds (default: 300)
- `enable_emojis`: Add AI-suggested emojis (default: false)
- `custom_hashtags`: List of custom hashtags to add
- `enable_link_preview`: Show link previews in Telegram (default: true)
- `enable_media`: Include media attachments (default: true)
- `show_author`: Display author information (default: true)
- `ai_enhance`: Use AI to enhance formatting (default: true)

## Dependencies

- `openai`: OpenAI API client
- `feedparser`: RSS/Atom feed parsing
- `python-telegram-bot`: Telegram Bot API
- `aiohttp`: Async HTTP client

## License

MIT License
