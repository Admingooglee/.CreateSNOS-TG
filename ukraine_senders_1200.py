import random
import string
from utils import Logger, DataManager, Config

logger = Logger()
config = Config()

DOMAINS = config.get('domains.ukraine', ['ukr.net', 'i.ua', 'ua.fm', 'ua.org', 'proton.me', 'protonmail.com'])

def gen_password(length=12):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

logger.info("=== Генератор украинских senders (1200 адресов) ===")

senders = {}
for i in range(1, 1201):
    domain = DOMAINS[(i-1) % len(DOMAINS)]
    email = f"user{i:04}@{domain}"
    pwd = gen_password(16)
    senders[email] = pwd

# Сохраняем в JSON
DataManager.save_senders(senders, "data/ukraine_senders_1200.json")

logger.info(f"✓ Первые 10 сендеров:")
for idx, (k, v) in enumerate(senders.items()):
    print(f"  '{k}': '{v}',")
    if idx == 9:
        print("  ...")
        break

print(f"\nВсего создано: {len(senders)} украинских email-адресов")
logger.info(f"Процесс завершен: {len(senders)} адресов сохранено в data/ukraine_senders_1200.json")