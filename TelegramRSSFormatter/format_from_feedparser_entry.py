import asyncio
import feedparser
import logging
import time
from typing import Dict, Set, Optional
from datetime import datetime
from src.config import load_config, FeedConfig
from src.rss_formatter import AIFormatterRSStT, RSSPost
from src.telegram_bot import TelegramRSSBot

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


class RSSMonitor:

    def __init__(self, config_file: Optional[str] = None):
        self.config = load_config(config_file)
        self.bot = TelegramRSSBot(self.config.telegram_bot_token)
        self.seen_entries: Dict[str, Set[str]] = {}
        self.formatters: Dict[str, AIFormatterRSStT] = {}

        for feed in self.config.feeds:
            self.seen_entries[feed.url] = set()
            self.formatters[feed.url] = AIFormatterRSStT(
                openai_api_key=self.config.openai_api_key,
                enable_emojis=feed.enable_emojis,
                custom_hashtags=feed.custom_hashtags,
                enable_link_preview=feed.enable_link_preview,
                enable_media=feed.enable_media,
                show_author=feed.show_author,
                ai_enhance=feed.ai_enhance)

    async def check_feed(self, feed_config: FeedConfig):
        try:
            logger.info(
                f"Checking feed: {feed_config.name} ({feed_config.url})")

            parsed_feed = feedparser.parse(feed_config.url)

            if parsed_feed.bozo:
                logger.warning(
                    f"Feed parsing warning for {feed_config.name}: {parsed_feed.bozo_exception}"
                )

            if not parsed_feed.entries:
                logger.warning(f"No entries found in feed: {feed_config.name}")
                return

            formatter = self.formatters[feed_config.url]
            new_entries = []

            for entry in parsed_feed.entries:
                entry_id = entry.get('id') or entry.get('link') or entry.get(
                    'title', '')

                if entry_id not in self.seen_entries[feed_config.url]:
                    new_entries.append(entry)
                    self.seen_entries[feed_config.url].add(entry_id)

            if new_entries:
                logger.info(
                    f"Found {len(new_entries)} new entries in {feed_config.name}"
                )

                for entry in reversed(new_entries):
                    feed_title = parsed_feed.feed.get('title',
                                                      feed_config.name)
                    # Create RSSPost object from feedparser entry
                    from src.rss_formatter import RSSPost
                    rss_post = RSSPost(
                        title=entry.get('title'),
                        author=entry.get('author'),
                        summary=entry.get('summary', ''),
                        link=entry.get('link'),
                        feed_title=feed_title,
                        content=entry.get('content', [{}])[0].get('value', '')
                        if entry.get('content') else '')
                    formatted_post = formatter.format_post(rss_post)
                    for chat_id in feed_config.chat_ids:
                        success = await self.bot.send_formatted_post(
                            chat_id, formatted_post)
                        if success:
                            logger.info(
                                f"Sent post to {chat_id}: {entry.get('title', 'Untitled')}"
                            )
                        else:
                            logger.error(f"Failed to send post to {chat_id}")

                        await asyncio.sleep(1)
            else:
                logger.info(f"No new entries in {feed_config.name}")

        except Exception as e:
            logger.error(f"Error checking feed {feed_config.name}: {e}",
                         exc_info=True)

    async def initialize_feeds(self):
        logger.info("Initializing feeds (marking existing entries as seen)...")
        for feed_config in self.config.feeds:
            try:
                parsed_feed = feedparser.parse(feed_config.url)
                for entry in parsed_feed.entries:
                    entry_id = entry.get('id') or entry.get(
                        'link') or entry.get('title', '')
                    self.seen_entries[feed_config.url].add(entry_id)
                logger.info(
                    f"Initialized {feed_config.name} with {len(self.seen_entries[feed_config.url])} existing entries"
                )
            except Exception as e:
                logger.error(
                    f"Error initializing feed {feed_config.name}: {e}")

    async def run(self):
        logger.info("Starting RSS to Telegram Bot with RSStT formatter")

        if not await self.bot.test_connection():
            logger.error("Failed to connect to Telegram. Exiting.")
            return

        logger.info(f"Monitoring {len(self.config.feeds)} feeds")
        for feed in self.config.feeds:
            logger.info(f"  - {feed.name}: {feed.url}")

        await self.initialize_feeds()

        logger.info("Starting monitoring loop...")

        while True:
            try:
                for feed_config in self.config.feeds:
                    await self.check_feed(feed_config)
                    await asyncio.sleep(2)

                min_interval = min(
                    [feed.check_interval for feed in self.config.feeds]
                    or [self.config.default_check_interval])

                logger.info(f"Sleeping for {min_interval} seconds...")
                await asyncio.sleep(min_interval)

            except KeyboardInterrupt:
                logger.info("Shutting down gracefully...")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}", exc_info=True)
                await asyncio.sleep(60)


async def main():
    import sys

    config_file = sys.argv[1] if len(sys.argv) > 1 else None

    monitor = RSSMonitor(config_file)
    await monitor.run()


if __name__ == "__main__":
    asyncio.run(main())
