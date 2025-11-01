import os
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class FeedConfig:
    url: str
    name: str
    chat_ids: List[str]
    check_interval: int = 300
    enable_emojis: bool = False
    custom_hashtags: Optional[List[str]] = None
    enable_link_preview: bool = True
    enable_media: bool = True
    show_author: bool = True
    ai_enhance: bool = True
    
    def __post_init__(self):
        if self.custom_hashtags is None:
            self.custom_hashtags = []


@dataclass
class BotConfig:
    telegram_bot_token: str
    openai_api_key: str
    feeds: List[FeedConfig]
    default_check_interval: int = 300
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BotConfig':
        feeds = []
        for feed_data in data.get('feeds', []):
            feeds.append(FeedConfig(**feed_data))
        
        return cls(
            telegram_bot_token=data.get('telegram_bot_token', ''),
            openai_api_key=data.get('openai_api_key', ''),
            feeds=feeds,
            default_check_interval=data.get('default_check_interval', 300)
        )
    
    @classmethod
    def from_json_file(cls, file_path: str) -> 'BotConfig':
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)
    
    @classmethod
    def from_env(cls) -> 'BotConfig':
        telegram_bot_token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
        openai_api_key = os.environ.get('OPENAI_API_KEY', '')
        
        feeds_json = os.environ.get('RSS_FEEDS', '[]')
        try:
            feeds_data = json.loads(feeds_json)
            feeds = [FeedConfig(**feed) for feed in feeds_data]
        except json.JSONDecodeError:
            feeds = []
        
        return cls(
            telegram_bot_token=telegram_bot_token,
            openai_api_key=openai_api_key,
            feeds=feeds,
            default_check_interval=int(os.environ.get('DEFAULT_CHECK_INTERVAL', '300'))
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'telegram_bot_token': self.telegram_bot_token,
            'openai_api_key': self.openai_api_key,
            'feeds': [asdict(feed) for feed in self.feeds],
            'default_check_interval': self.default_check_interval
        }
    
    def to_json_file(self, file_path: str):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)


def load_config(config_file: Optional[str] = None) -> BotConfig:
    if config_file and os.path.exists(config_file):
        return BotConfig.from_json_file(config_file)
    elif os.path.exists('config.json'):
        return BotConfig.from_json_file('config.json')
    else:
        return BotConfig.from_env()
