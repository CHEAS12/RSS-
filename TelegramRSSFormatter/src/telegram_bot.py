import os
import asyncio
from typing import Optional, List, Dict, Any
from telegram import Bot, InputMediaPhoto, InputMediaVideo
from telegram.error import TelegramError
from telegram.constants import ParseMode
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class TelegramRSSBot:
    def __init__(self, bot_token: Optional[str] = None):
        self.bot_token = bot_token or os.environ.get("TELEGRAM_BOT_TOKEN")
        if not self.bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN must be provided or set in environment")
        
        self.bot = Bot(token=self.bot_token)
    
    async def send_message(
        self,
        chat_id: str,
        message: str,
        parse_mode: str = "Markdown",
        disable_web_page_preview: bool = False
    ) -> bool:
        try:
            await self.bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode=parse_mode,
                disable_web_page_preview=disable_web_page_preview
            )
            logger.info(f"Message sent to {chat_id}")
            return True
        except TelegramError as e:
            logger.error(f"Failed to send message to {chat_id}: {e}")
            return False
    
    async def send_message_with_media(
        self,
        chat_id: str,
        message: str,
        media_attachments: List[Dict[str, str]],
        parse_mode: str = "Markdown"
    ) -> bool:
        try:
            if not media_attachments:
                return await self.send_message(
                    chat_id=chat_id,
                    message=message,
                    parse_mode=parse_mode
                )
            
            first_media = media_attachments[0]
            media_type = first_media.get('type', '').lower()
            
            if 'image' in media_type or 'photo' in media_type:
                await self.bot.send_photo(
                    chat_id=chat_id,
                    photo=first_media['url'],
                    caption=message,
                    parse_mode=parse_mode
                )
            elif 'video' in media_type:
                await self.bot.send_video(
                    chat_id=chat_id,
                    video=first_media['url'],
                    caption=message,
                    parse_mode=parse_mode
                )
            else:
                await self.bot.send_document(
                    chat_id=chat_id,
                    document=first_media['url'],
                    caption=message,
                    parse_mode=parse_mode
                )
            
            if len(media_attachments) > 1:
                media_group = []
                for media in media_attachments[1:]:
                    media_type = media.get('type', '').lower()
                    if 'image' in media_type or 'photo' in media_type:
                        media_group.append(InputMediaPhoto(media=media['url']))
                    elif 'video' in media_type:
                        media_group.append(InputMediaVideo(media=media['url']))
                
                if media_group:
                    await self.bot.send_media_group(
                        chat_id=chat_id,
                        media=media_group
                    )
            
            logger.info(f"Message with media sent to {chat_id}")
            return True
        except TelegramError as e:
            logger.error(f"Failed to send message with media to {chat_id}: {e}")
            return await self.send_message(
                chat_id=chat_id,
                message=message,
                parse_mode=parse_mode
            )
    
    async def send_formatted_post(
        self,
        chat_id: str,
        formatted_post: Dict[str, Any]
    ) -> bool:
        message = formatted_post.get("message", "")
        parse_mode = formatted_post.get("parse_mode", "Markdown")
        disable_web_page_preview = formatted_post.get("disable_web_page_preview", False)
        has_media = formatted_post.get("has_media", False)
        media_attachments = formatted_post.get("media_attachments", [])
        
        if has_media and media_attachments:
            return await self.send_message_with_media(
                chat_id=chat_id,
                message=message,
                media_attachments=media_attachments,
                parse_mode=parse_mode
            )
        else:
            return await self.send_message(
                chat_id=chat_id,
                message=message,
                parse_mode=parse_mode,
                disable_web_page_preview=disable_web_page_preview
            )
    
    async def test_connection(self) -> bool:
        try:
            bot_info = await self.bot.get_me()
            logger.info(f"Bot connected: @{bot_info.username}")
            return True
        except TelegramError as e:
            logger.error(f"Failed to connect to Telegram: {e}")
            return False


async def main():
    bot = TelegramRSSBot()
    
    if await bot.test_connection():
        print("✅ Telegram bot is ready!")
        
        test_post = {
            "message": "**Test Message**\n\nThis is a test message from RSStT formatter.\n\n[Source](https://example.com)",
            "parse_mode": "Markdown",
            "disable_web_page_preview": False,
            "has_media": False,
            "media_attachments": []
        }
        
        chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")
        if chat_id:
            await bot.send_formatted_post(chat_id, test_post)
        else:
            print("⚠️  TELEGRAM_CHAT_ID not set. Set it to send test messages.")
    else:
        print("❌ Failed to connect to Telegram bot.")


if __name__ == "__main__":
    asyncio.run(main())
