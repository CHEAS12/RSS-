import requests
import sys

BOT_TOKEN = "8337940960:AAERfK-BkRD_v8SYOjusrs5yTYWMta-v1Hc"
CHANNEL = "@NeuralPulseNews"

message = "🧪 Тестовое сообщение из RSS Bot\n\nЭто сообщение отправлено для проверки работы бота."

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
data = {
    "chat_id": CHANNEL,
    "text": message,
    "parse_mode": "HTML"
}

print(f"📨 Отправка тестового сообщения в {CHANNEL}...")
response = requests.post(url, json=data)

if response.status_code == 200:
    print("✅ Сообщение успешно отправлено!")
    print(f"🔗 Проверьте канал: https://t.me/NeuralPulseNews")
else:
    print(f"❌ Ошибка: {response.status_code}")
    print(response.json())
    sys.exit(1)
