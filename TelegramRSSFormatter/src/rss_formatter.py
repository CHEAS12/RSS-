import os
import json
import re
import logging
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from openai import OpenAI

logger = logging.getLogger(__name__)

@dataclass
class RSSPost:
    title: Optional[str] = None
    author: Optional[str] = None
    summary: Optional[str] = None
    link: Optional[str] = None
    feed_title: Optional[str] = None
    content: Optional[str] = None
    media_attachments: Optional[List[Dict[str, str]]] = None

    def __post_init__(self):
        if self.media_attachments is None:
            self.media_attachments = []

class RSSFormatter:
    MAX_TELEGRAM_LENGTH = 4096
    MAX_TELEGRAM_WITH_MEDIA = 1024

    def __init__(self, 
                 openai_api_key: Optional[str] = None,
                 enable_emojis: bool = False,
                 custom_hashtags: Optional[List[str]] = None,
                 length_limit: int = 4096,
                 enable_link_preview: bool = True,
                 enable_media: bool = True,
                 show_author: bool = True,
                 show_feed_title: bool = True,
                 ai_enhance: bool = True,
                 style: str = "RSStT"):
        self.openai_api_key = openai_api_key or os.environ.get("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY must be provided or set in environment")

        self.client = OpenAI(api_key=self.openai_api_key)
        self.enable_emojis = enable_emojis
        self.custom_hashtags = custom_hashtags or []
        self.length_limit = min(length_limit, self.MAX_TELEGRAM_LENGTH)
        self.enable_link_preview = enable_link_preview
        self.enable_media = enable_media
        self.show_author = show_author
        self.show_feed_title = show_feed_title
        self.ai_enhance = ai_enhance
        self.style = style

    def generate_telegram_post(self, news_item: RSSPost) -> Dict[str, Any]:
        """
        Генерирует пост для Telegram-канала на основе входной новости, 
        используя OpenAI API для копирайтерской обработки.

        Args:
            news_item: Объект RSSPost с информацией о новости

        Returns:
            Dict с ключами:
                - text: сгенерированный текст поста
                - media: список медиа-вложений
                - link_preview: URL для превью ссылки
        """
        try:
            # Формируем промпт для OpenAI API
            content_to_process = news_item.content or news_item.summary or ""

            prompt = f"""Ты - профессиональный копирайтер для Telegram-канала с новостями.
Твоя задача - создать привлекательный и информативный пост для Telegram на основе следующей новости.

НАЗВАНИЕ: {news_item.title or 'Без заголовка'}
ИСТОЧНИК: {news_item.feed_title or 'Неизвестный источник'}
СОДЕРЖАНИЕ: {content_to_process[:1000]}
ССЫЛКА: {news_item.link}

Требования:
1. Сделай текст ярким и привлекающим внимание
2. Добавь 1-3 релевантных эмодзи (но не перебарщивай)
3. Структурируй текст: заголовок, основное содержание, призыв к действию
4. Добавь 2-4 релевантных хэштега в конце
5. Максимальная длина - 1000 символов
6. Сохрани ключевые факты из исходного текста
7. Обязательно включи ссылку на источник в конце
8. Пиши на русском языке профессионально, но дружелюбно

Формат ответа:
<заголовок с эмодзи>

<основной текст>

<призыв к действию>

<хэштеги>"""

            # Отправляем запрос к OpenAI API
            logger.info(f"Генерация поста для: {news_item.title}")

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Используем эффективную модель
                messages=[
                    {"role": "system", "content": "Ты профессиональный копирайтер для Telegram с опытом в создании вирусного контента."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.7
            )

            generated_text = response.choices[0].message.content.strip()

            # Добавляем ссылку, если её еще нет
            if news_item.link and news_item.link not in generated_text:
                generated_text += f"\n\n🔗 {news_item.link}"

            # Проверяем длину
            if len(generated_text) > self.MAX_TELEGRAM_WITH_MEDIA:
                generated_text = generated_text[:self.MAX_TELEGRAM_WITH_MEDIA-3] + "..."

            result = {
                "text": generated_text,
                "media": news_item.media_attachments if self.enable_media else [],
                "link_preview": news_item.link if self.enable_link_preview else None
            }

            logger.info(f"Пост успешно сгенерирован. Длина: {len(generated_text)} символов")
            return result

        except Exception as e:
            logger.error(f"Ошибка при генерации поста: {e}")
            # Возвращаем базовый формат в случае ошибки
            return {
                "text": self._format_fallback(news_item),
                "media": news_item.media_attachments if self.enable_media else [],
                "link_preview": news_item.link if self.enable_link_preview else None
            }

    def _format_fallback(self, news_item: RSSPost) -> str:
        """Базовое форматирование на случай ошибки API"""
        parts = []

        if news_item.title:
            parts.append(f"📰 {news_item.title}")

        if news_item.summary:
            summary = news_item.summary[:300] + "..." if len(news_item.summary) > 300 else news_item.summary
            parts.append(f"\n\n{summary}")

        if news_item.link:
            parts.append(f"\n\n🔗 {news_item.link}")

        return "".join(parts)

    def format_post(self, post: RSSPost) -> Dict[str, Any]:
        """Форматирует пост с использованием AI-генерации"""
        if self.ai_enhance:
            return self.generate_telegram_post(post)
        else:
            # Базовое форматирование без AI
            return {
                "text": self._format_fallback(post),
                "media": post.media_attachments if self.enable_media else [],
                "link_preview": post.link if self.enable_link_preview else None
            }