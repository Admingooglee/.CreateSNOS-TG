#!/usr/bin/env python3
"""
Конфигуратор отправок - позволяет быстро менять параметры
"""
import json
import os
from utils import Logger

logger = Logger()

class SendingConfig:
    """Управление конфигурацией отправок"""
    
    CONFIG_FILE = "data/sending_config.json"
    
    @staticmethod
    def load():
        """Загружает конфигурацию"""
        if os.path.exists(SendingConfig.CONFIG_FILE):
            try:
                with open(SendingConfig.CONFIG_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Ошибка загрузки конфиги: {e}")
        return SendingConfig.get_default()
    
    @staticmethod
    def get_default():
        """Возвращает конфигурацию по умолчанию"""
        return {
            "batch_settings": {
                "senders_per_batch": 30,
                "max_senders_to_use": 1000,
                "receivers_per_sender": 4,
                "total_emails_per_session": 0
            },
            "timing": {
                "min_delay_between_emails": 0.5,
                "max_delay_between_emails": 3.0,
                "batch_pause_min": 5.0,
                "batch_pause_max": 15.0,
                "pause_every_n_senders": 3
            },
            "proxy_settings": {
                "use_custom_proxies": True,
                "rotate_proxy_every_n_emails": 5,
                "retry_on_timeout": True,
                "timeout_seconds": 10
            }
        }
    
    @staticmethod
    def save(config):
        """Сохраняет конфигурацию"""
        try:
            os.makedirs("data", exist_ok=True)
            with open(SendingConfig.CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=2)
            logger.info(f"✓ Конфигурация сохранена")
            return True
        except Exception as e:
            logger.error(f"Ошибка сохранения конфиги: {e}")
            return False
    
    @staticmethod
    def interactive_setup():
        """Интерактивная настройка параметров"""
        print("\n" + "="*60)
        print("⚙️  ИНТЕРАКТИВНАЯ НАСТРОЙКА ПАРАМЕТРОВ ОТПРАВКИ")
        print("="*60)
        
        config = SendingConfig.load()
        
        print("\n📊 ПАРАМЕТРЫ БАТЧА (пакета отправок)")
        print(f"Текущие: {config['batch_settings']['senders_per_batch']} отправителей")
        print("\nОпции:")
        print("  1️⃣  - 30 отправителей (стандартно)")
        print("  2️⃣  - 100 отправителей (ускоренно)")
        print("  3️⃣  - 350 отправителей (быстро)")
        print("  4️⃣  - 500+ отправителей (максимум)")
        print("  5️⃣  - Свой размер")
        
        choice = input("\nВыбирай скорость отправки: ").strip()
        
        if choice == "1":
            config['batch_settings']['senders_per_batch'] = 30
            print("✓ Установлено: 30 отправителей")
        elif choice == "2":
            config['batch_settings']['senders_per_batch'] = 100
            print("✓ Установлено: 100 отправителей")
        elif choice == "3":
            config['batch_settings']['senders_per_batch'] = 350
            print("✓ Установлено: 350 отправителей")
        elif choice == "4":
            config['batch_settings']['senders_per_batch'] = 500
            print("✓ Установлено: 500+ отправителей")
        elif choice == "5":
            try:
                amount = int(input("Введи количество отправителей: "))
                config['batch_settings']['senders_per_batch'] = amount
                print(f"✓ Установлено: {amount} отправителей")
            except:
                print("❌ Неверный ввод")
                return False
        
        # Спрашиваем про таймауты
        print("\n⏱️  ТАЙМАУТЫ И ЗАДЕРЖКИ")
        print(f"Текущие задержки: {config['timing']['min_delay_between_emails']}s - {config['timing']['max_delay_between_emails']}s")
        
        speed_choice = input("Ускорить задержки? (y/n): ").strip().lower()
        if speed_choice == 'y':
            config['timing']['min_delay_between_emails'] = 0.2
            config['timing']['max_delay_between_emails'] = 1.0
            print("✓ Задержки ускорены")
        
        SendingConfig.save(config)
        print("\n" + "="*60)
        print("✅ Конфигурация сохранена!")
        print("="*60)
        
        # Показываем финальные параметры
        print("\n📋 ФИНАЛЬНЫЕ ПАРАМЕТРЫ:")
        print(f"  • Отправителей за сессию: {config['batch_settings']['senders_per_batch']}")
        print(f"  • Задержка между письмами: {config['timing']['min_delay_between_emails']:.1f}s - {config['timing']['max_delay_between_emails']:.1f}s")
        print(f"  • Итого писем за сессию: ~{config['batch_settings']['senders_per_batch'] * len(['sms@telegram.org', 'dmca@telegram.org', 'abuse@telegram.org', 'support@telegram.org'])}")
        
        return True


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "setup":
            SendingConfig.interactive_setup()
        elif sys.argv[1] == "show":
            config = SendingConfig.load()
            print("\n📋 ТЕКУЩАЯ КОНФИГУРАЦИЯ:")
            print(json.dumps(config, indent=2, ensure_ascii=False))
        elif sys.argv[1] == "reset":
            config = SendingConfig.get_default()
            SendingConfig.save(config)
            print("✓ Конфигурация сброшена")
    else:
        print("\nДоступные команды:")
        print("  python sending_config.py setup  - Интерактивная настройка")
        print("  python sending_config.py show   - Показать текущую конфиг")
        print("  python sending_config.py reset  - Сбросить на стандартную")
        SendingConfig.interactive_setup()
