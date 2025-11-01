# Telegram RSS Formatter with RSStT Standard

## Project Overview

This is a Telegram RSS bot that formats feed posts following the RSStT standard using OpenAI GPT-5 for AI-enhanced content generation.

### Purpose
- Monitor RSS feeds and send formatted posts to Telegram
- Use AI (OpenAI GPT-5) to generate clean, engaging content
- Follow the RSStT formatting standard for professional-looking messages

### Current State
- Core formatter implemented in `rss_formatter.py`
- Telegram bot integration in `telegram_bot.py`
- Feed monitoring system in `main.py`
- Configuration system in `config.py`

## Recent Changes

- **2025-10-23**: Initial implementation
  - Created AIFormatterRSStT class with full RSStT support
  - Added Telegram bot integration
  - Implemented RSS feed monitoring
  - Added configuration system (JSON and environment variables)
  - Integrated OpenAI GPT-5 for content enhancement

## Project Architecture

### Core Components

1. **rss_formatter.py**: RSS post formatting with AI enhancement
   - `AIFormatterRSStT`: Main formatter class
   - `RSSPost`: Data class for RSS posts
   - Supports: titles, authors, summaries, links, emojis, hashtags, media

2. **telegram_bot.py**: Telegram bot wrapper
   - `TelegramRSSBot`: Async Telegram bot client
   - Handles message sending with media support
   - Error handling and retry logic

3. **config.py**: Configuration management
   - `FeedConfig`: Per-feed settings
   - `BotConfig`: Global bot configuration
   - Supports JSON files and environment variables

4. **main.py**: Main application
   - `RSSMonitor`: Feed monitoring and processing
   - Initialization and main event loop
   - Graceful error handling

### Dependencies

- Python 3.11
- openai: OpenAI API client (GPT-5)
- feedparser: RSS parsing
- python-telegram-bot: Telegram API
- aiohttp: Async HTTP

### Required Secrets

- `OPENAI_API_KEY`: OpenAI API key for GPT-5
- `TELEGRAM_BOT_TOKEN`: Telegram bot token from @BotFather
- `TELEGRAM_CHAT_ID` (optional): Default chat for testing

## User Preferences

- Language: Russian/English
- Wants AI-enhanced RSStT formatting
- Prefers comprehensive parameter support
- Values clean code with good architecture

## Configuration

### Using config.json

Create a `config.json` file with your feed settings (see `config.example.json`).

### Using Environment Variables

Set these environment variables:
- `TELEGRAM_BOT_TOKEN`
- `OPENAI_API_KEY`
- `RSS_FEEDS` (JSON array)
- `DEFAULT_CHECK_INTERVAL` (optional)

## Development Notes

- Uses async/await for Telegram operations
- GPT-5 model for AI enhancement (released Aug 7, 2025)
- Follows RSStT standard formatting
- Supports media attachments from RSS feeds
- Tracks seen entries to avoid duplicates
