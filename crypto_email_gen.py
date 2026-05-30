import requests
import time
import json
import os
from utils import Logger, DataManager, Config

# ⚠️ ВНИМАНИЕ: API ключ должен быть установлен в переменную окружения!
# export RANDOMMER_API_KEY="your_key_here"
# Или в config/settings.json

logger = Logger()
config = Config()

RANDOMMER_API_KEY = os.getenv('RANDOMMER_API_KEY') or config.get('randommer.api_key', None)
EMAIL_COUNT = config.get('email_generation.count', 200)

if not RANDOMMER_API_KEY:
    logger.error("❌ RANDOMMER_API_KEY не установлен!")
    logger.error("   1. Установи переменную окружения: export RANDOMMER_API_KEY='your_key'")
    logger.error("   2. Или добавь в config/settings.json: \"randommer\": {\"api_key\": \"your_key\"}")
    RANDOMMER_API_KEY = None

def fetch_emails(count):
    emails = []
    url = "https://randommer.io/api/Email/Free"
    headers = {"X-Api-Key": RANDOMMER_API_KEY}
    batch_size = 20  # максимальный лимит per request у randommer.io
    while len(emails) < count:
        try:
            resp = requests.get(url, headers=headers)
            if resp.ok:
                email = resp.json()
                if email not in emails:
                    emails.append(email)
                    logger.debug(f"Получен email: {email}")
            else:
                logger.error(f"API error: {resp.status_code} - {resp.text}")
            time.sleep(0.2)  # чтобы не ловить rate-limit
        except Exception as ex:
            logger.error(f"Ошибка при запросе randommer.io: {ex}")
            time.sleep(2)
    return emails[:count]

# Пример использования
if __name__ == "__main__":
    logger.info("=== Генератор email-ов через randommer.io ===")
    logger.info(f"Генерируем {EMAIL_COUNT} тестовых email-адресов...")
    
    emails = fetch_emails(EMAIL_COUNT)
    logger.info(f"Сгенерировано {len(emails)} email-ов.")
    
    # Превращаем в senders-словарь с дефолтными паролями (или генерируй свои)
    senders = {email: "test_password1234" for email in emails}
    
    # Сохраняем в JSON
    DataManager.save_senders(senders, "data/generated_senders.json")
    
    logger.info(f"✓ Первые 5 сендеров:")
    for idx, (k, v) in enumerate(senders.items()):
        print(f"  '{k}': '{v}',")
        if idx == 4:
            break
    
    print("...")
