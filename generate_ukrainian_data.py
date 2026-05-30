#!/usr/bin/env python3
"""
Скрипт для генерации полного файла с 1200 украинскими отправителями
"""
import json
import string
import random

def gen_password(length=16):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choices(chars, k=length))

DOMAINS = ['ukr.net', 'i.ua', 'ua.fm', 'ua.org', 'proton.me', 'protonmail.com']

senders = {}
for i in range(1, 1201):
    domain = DOMAINS[(i-1) % len(DOMAINS)]
    # Создаем разнообразные username-ы
    username_styles = [
        f"user{i:04d}",
        f"sender{i:04d}",
        f"account{i:04d}",
        f"email{i:04d}",
    ]
    username = username_styles[(i-1) % len(username_styles)]
    
    email = f"{username}@{domain}"
    pwd = gen_password(20)
    senders[email] = pwd

# Сохраняем
with open('data/ukraine_senders_1200_full.json', 'w', encoding='utf-8') as f:
    json.dump(senders, f, indent=2, ensure_ascii=False)

print(f"✓ Создано {len(senders)} украинских email-адресов")
print(f"✓ Сохранено в data/ukraine_senders_1200_full.json")

# Показываем примеры
print("\n📋 Примеры украинских отправителей:")
for idx, (email, pwd) in enumerate(list(senders.items())[:5]):
    print(f"  {email}: {pwd[:15]}...")
