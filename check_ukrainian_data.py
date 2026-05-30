#!/usr/bin/env python3
"""
Скрипт для проверки статуса украинских данных
"""
import json
import os
from utils import Config, Logger, DataManager

logger = Logger()
config = Config()

print("\n" + "="*60)
print("📋 СТАТУС УКРАИНСКИХ ДАННЫХ".center(60))
print("="*60 + "\n")

# Проверяем конфиг
print("✓ Конфигурация:")
senders_file = config.get('data_storage.senders_file', 'data/senders.json')
receivers_file = config.get('data_storage.receivers_file', 'data/receivers.json')
print(f"  - Файл отправителей: {senders_file}")
print(f"  - Файл получателей: {receivers_file}")

# Проверяем украинские домены
ukr_domains = config.get('domains.ukraine', [])
print(f"\n✓ Украинские домены ({len(ukr_domains)}):")
for domain in ukr_domains:
    print(f"  - {domain}")

# Проверяем SMTP серверы
print(f"\n✓ SMTP провайдеры:")
providers = config.get('smtp.providers', {})
for provider, settings in providers.items():
    print(f"  - {provider}: {settings.get('server')} ({settings.get('port')})")

# Проверяем данные
print(f"\n📦 Файлы данных:")
for filename in ['data/ukraine_senders_1200.json', 'data/ukraine_senders_sample.json', 'data/receivers.json']:
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            count = len(data)
            print(f"  ✓ {filename}: {count} записей")
    else:
        print(f"  ✗ {filename}: НЕ НАЙДЕН")

print("\n" + "="*60)
print("✓ Конфигурация готова к использованию!".center(60))
print("="*60 + "\n")
