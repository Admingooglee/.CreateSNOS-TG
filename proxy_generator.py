#!/usr/bin/env python3
"""
Генератор прокси и рандомизация для SNOSER
Поддержка ручной вставки прокси и загрузки из файла
"""
import random
import string
import time
import json
import os
from utils import Logger

logger = Logger()

class ProxyGenerator:
    """Генератор и управление прокси"""
    
    PROXY_FILE = "data/custom_proxies.json"
    
    @staticmethod
    def load_custom_proxies():
        """Загружает пользовательские прокси из файла"""
        if os.path.exists(ProxyGenerator.PROXY_FILE):
            try:
                with open(ProxyGenerator.PROXY_FILE, 'r') as f:
                    data = json.load(f)
                    if isinstance(data, dict) and 'proxies' in data:
                        proxies = data['proxies']
                        if proxies:
                            logger.info(f"✓ Загружено {len(proxies)} пользовательских прокси")
                            return proxies
            except Exception as e:
                logger.warning(f"Ошибка загрузки пользовательских прокси: {e}")
        return None
    
    @staticmethod
    def save_custom_proxies(proxies):
        """Сохраняет пользовательские прокси в файл"""
        try:
            os.makedirs("data", exist_ok=True)
            with open(ProxyGenerator.PROXY_FILE, 'w') as f:
                json.dump({"proxies": proxies, "count": len(proxies)}, f, indent=2)
            logger.info(f"✓ Сохранено {len(proxies)} прокси в {ProxyGenerator.PROXY_FILE}")
            return True
        except Exception as e:
            logger.error(f"Ошибка сохранения прокси: {e}")
            return False
    
    @staticmethod
    def generate_free_proxy_list():
        """Генерирует список бесплатных публичных прокси"""
        # Проверяем наличие пользовательских прокси
        custom = ProxyGenerator.load_custom_proxies()
        if custom:
            return custom
        
        # Стандартный список как резервный вариант
        free_proxies = [
            "http://10.10.1.10:3128",
            "http://10.10.1.11:1080",
            "http://198.101.192.20:80",
            "http://195.20.114.31:8080",
            "http://196.27.106.76:3128",
            "http://203.142.68.45:9999",
            "http://61.19.145.113:8080",
            "http://103.236.48.165:8000",
            "http://203.192.199.114:8080",
            "http://123.231.248.41:3128",
        ]
        return free_proxies
    
    @staticmethod
    def get_random_proxy():
        """Возвращает случайный прокси из списка"""
        proxies = ProxyGenerator.generate_free_proxy_list()
        if not proxies:
            logger.warning("⚠️  Нет доступных прокси!")
            return None
        proxy = random.choice(proxies)
        logger.debug(f"Выбран прокси: {proxy}")
        return proxy
    
    @staticmethod
    def get_proxy_dict(proxy_url):
        """Преобразует URL прокси в словарь для requests"""
        if not proxy_url:
            return None
        return {
            "http": proxy_url,
            "https": proxy_url
        }
    
    @staticmethod
    def add_custom_proxy_interactive():
        """Интерактивное добавление пользовательского прокси"""
        print("\n" + "="*50)
        print("🔐 ДОБАВЛЕНИЕ СОБСТВЕННОГО ПРОКСИ")
        print("="*50)
        print("Примеры формата: http://1.2.3.4:8080")
        print("                socks5://user:pass@1.2.3.4:1080")
        print("                http://proxy.example.com:3128")
        print()
        
        # Загружаем существующие прокси
        custom = ProxyGenerator.load_custom_proxies() or []
        
        try:
            while True:
                proxy = input(f"📍 Введи прокси [{len(custom)} добавлено] (или 'exit' для выхода): ").strip()
                
                if proxy.lower() == 'exit':
                    break
                
                if not proxy:
                    print("❌ Прокси не может быть пустым!")
                    continue
                
                # Базовая валидация
                if not (proxy.startswith('http://') or proxy.startswith('https://') or proxy.startswith('socks')):
                    print("❌ Прокси должен начинаться с http://, https:// или socks")
                    continue
                
                if ':' not in proxy:
                    print("❌ Прокси должен содержать порт (например, :8080)")
                    continue
                
                # Добавляем прокси если его нет
                if proxy not in custom:
                    custom.append(proxy)
                    print(f"✅ Добавлен прокси #{len(custom)}")
                else:
                    print(f"⚠️  Этот прокси уже в списке")
        
        except KeyboardInterrupt:
            print("\n⚠️  Отмена")
        
        # Сохраняем
        if custom:
            ProxyGenerator.save_custom_proxies(custom)
            print(f"\n✓ Сохранено {len(custom)} прокси")
            return True
        
        return False


class DataRandomizer:
    """Рандомизация данных для избежания повторений"""
    
    @staticmethod
    def generate_random_user_agent():
        """Генерирует случайный User-Agent"""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15",
            "Mozilla/5.0 (Android 11; Mobile; rv:89.0) Gecko/89.0 Firefox/89.0",
        ]
        return random.choice(user_agents)
    
    @staticmethod
    def randomize_delays():
        """Возвращает случайную задержку в секундах"""
        # Задержка от 0.5 до 3 секунд
        delay = random.uniform(0.5, 3.0)
        return delay
    
    @staticmethod
    def randomize_sender_name(email):
        """Добавляет случайное отображаемое имя отправителю"""
        first_names = ['Alex', 'Jordan', 'Sam', 'Casey', 'Morgan', 'Riley', 'Taylor', 'Quinn']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis']
        
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        
        display_name = f"{first_name} {last_name}"
        return display_name
    
    @staticmethod
    def add_variation_to_text(text):
        """Добавляет небольшие вариации в текст для избежания фильтров"""
        # Заменяет некоторые символы на похожие
        variations = {
            'а': ['а', 'а'],  # кириллица и латиница могут выглядеть одинаково
            'е': ['е', 'ё'],
            'о': ['о', 'о'],
        }
        
        result = text
        for char, variants in variations.items():
            if random.random() > 0.7:  # 30% вероятность
                result = result.replace(char, random.choice(variants))
        
        return result
    
    @staticmethod
    def randomize_phone_format(phone):
        """Рандомизирует формат телефонного номера"""
        if not phone:
            return phone
        
        # Удаляем все кроме цифр
        digits = ''.join(filter(str.isdigit, phone))
        
        if len(digits) < 10:
            return phone
        
        formats = [
            f"+{digits[0]} ({digits[1:4]}) {digits[4:7]}-{digits[7:]}",
            f"+{digits[0]} {digits[1:4]} {digits[4:7]} {digits[7:]}",
            f"{digits[:4]}-{digits[4:7]}-{digits[7:]}",
            f"({digits[:3]}) {digits[3:6]}-{digits[6:]}",
        ]
        
        return random.choice(formats)
    
    @staticmethod
    def randomize_timing():
        """Возвращает случайное время в диапазоне"""
        timing = {
            "min_delay": random.uniform(0.3, 1.0),
            "max_delay": random.uniform(2.0, 5.0),
            "batch_delay": random.uniform(3.0, 10.0),
        }
        return timing


class IPRotator:
    """Ротирует IP адреса для избежания блокировки"""
    
    def __init__(self, use_custom_proxies=True):
        self.current_proxy_index = 0
        
        # Пробуем загрузить пользовательские прокси
        if use_custom_proxies:
            custom = ProxyGenerator.load_custom_proxies()
            if custom:
                self.proxies = custom
                logger.info(f"✓ Используются {len(custom)} пользовательских прокси")
            else:
                self.proxies = ProxyGenerator.generate_free_proxy_list()
                logger.info(f"⚠️  Используются стандартные прокси ({len(self.proxies)})")
        else:
            self.proxies = ProxyGenerator.generate_free_proxy_list()
        
        self.rotation_count = 0
        self.failed_proxies = []
    
    def get_next_proxy(self):
        """Возвращает следующий прокси в списке"""
        if not self.proxies:
            logger.warning("❌ Нет доступных прокси!")
            return None
        
        proxy = self.proxies[self.current_proxy_index]
        self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxies)
        self.rotation_count += 1
        
        logger.debug(f"Ротация прокси #{self.rotation_count}: {proxy}")
        return proxy
    
    def get_random_proxy(self):
        """Возвращает случайный прокси"""
        if not self.proxies:
            return None
        return random.choice(self.proxies)
    
    def add_proxy(self, proxy_url):
        """Добавляет новый прокси в список"""
        if proxy_url not in self.proxies:
            self.proxies.append(proxy_url)
            logger.info(f"✓ Добавлен новый прокси: {proxy_url}")
            return True
        return False
    
    def remove_bad_proxy(self, proxy_url):
        """Удаляет неработающий прокси"""
        if proxy_url in self.proxies:
            self.proxies.remove(proxy_url)
            self.failed_proxies.append(proxy_url)
            logger.warning(f"❌ Удален неработающий прокси: {proxy_url}")
            return True
        return False
    
    def get_proxy_stats(self):
        """Возвращает статистику прокси"""
        return {
            "total": len(self.proxies),
            "failed": len(self.failed_proxies),
            "rotations": self.rotation_count,
            "current_index": self.current_proxy_index
        }


class SendingProfile:
    """Профиль отправителя для избежания паттернов"""
    
    def __init__(self, sender_email, sender_password):
        self.email = sender_email
        self.password = sender_password
        self.display_name = DataRandomizer.randomize_sender_name(sender_email)
        self.user_agent = DataRandomizer.generate_random_user_agent()
        self.proxy = ProxyGenerator.get_random_proxy()
        self.send_count = 0
        self.error_count = 0
        self.last_send_time = 0
    
    def increment_send_count(self):
        """Увеличивает счетчик отправок"""
        self.send_count += 1
    
    def increment_error_count(self):
        """Увеличивает счетчик ошибок"""
        self.error_count += 1
    
    def get_stats(self):
        """Возвращает статистику отправителя"""
        return {
            "email": self.email,
            "display_name": self.display_name,
            "sent": self.send_count,
            "errors": self.error_count,
            "success_rate": (self.send_count - self.error_count) / max(self.send_count, 1) * 100
        }
    
    def should_rotate_proxy(self):
        """Определяет, нужно ли ротировать прокси"""
        # Ротируем каждые 5 отправок или после 3 ошибок
        return self.send_count % 5 == 0 or self.error_count >= 3


# Пример использования и интерактивный режим
if __name__ == "__main__":
    import sys
    
    print("\n" + "="*60)
    print("🔄 ГЕНЕРАТОР ПРОКСИ И УПРАВЛЕНИЕ")
    print("="*60)
    
    # Проверяем аргументы командной строки
    if len(sys.argv) > 1:
        if sys.argv[1] == "add":
            # Интерактивное добавление прокси
            ProxyGenerator.add_custom_proxy_interactive()
        elif sys.argv[1] == "list":
            # Показываем текущие прокси
            proxies = ProxyGenerator.load_custom_proxies()
            if proxies:
                print(f"\n✓ Загружено {len(proxies)} пользовательских прокси:")
                for i, proxy in enumerate(proxies, 1):
                    print(f"  {i}. {proxy}")
            else:
                print("\n⚠️  Пользовательские прокси не найдены")
                print("Используются стандартные прокси:")
                for i, proxy in enumerate(ProxyGenerator.generate_free_proxy_list(), 1):
                    print(f"  {i}. {proxy}")
        else:
            print(f"❌ Неизвестная команда: {sys.argv[1]}")
            print("\nДоступные команды:")
            print("  python proxy_generator.py add   - Добавить свои прокси")
            print("  python proxy_generator.py list  - Показать текущие прокси")
    else:
        # Интерактивное меню
        menu = """
┌─────────────────────────────────────┐
│  УПРАВЛЕНИЕ ПРОКСИ                  │
├─────────────────────────────────────┤
│  1️⃣  - ДОБАВИТЬ ПРОКСИ              │
│  2️⃣  - ПОКАЗАТЬ ПРОКСИ              │
│  3️⃣  - ТЕСТ ВСЕХ СИСТЕМ             │
│  0️⃣  - ВЫХОД                        │
└─────────────────────────────────────┘
"""
        print(menu)
        choice = input("Выбери опцию: ").strip()
        
        if choice == "1":
            ProxyGenerator.add_custom_proxy_interactive()
        elif choice == "2":
            proxies = ProxyGenerator.load_custom_proxies()
            if proxies:
                print(f"\n✓ Загружено {len(proxies)} пользовательских прокси:")
                for i, proxy in enumerate(proxies, 1):
                    print(f"  {i}. {proxy}")
            else:
                print("\n⚠️  Пользовательские прокси не найдены")
        elif choice == "3":
            print("\n🔄 Тестирование прокси:")
            for i in range(3):
                proxy = ProxyGenerator.get_random_proxy()
                print(f"  {i+1}. {proxy}")
            
            print("\n🎲 Тестирование рандомизации:")
            print(f"  User-Agent: {DataRandomizer.generate_random_user_agent()[:50]}...")
            print(f"  Задержка: {DataRandomizer.randomize_delays():.2f}с")
            print(f"  Имя: {DataRandomizer.randomize_sender_name('user@mail.ru')}")
            
            print("\n🔁 Тестирование ротатора IP:")
            rotator = IPRotator()
            for i in range(3):
                proxy = rotator.get_next_proxy()
                print(f"  {i+1}. {proxy}")
            
            print("\n👤 Тестирование профиля отправителя:")
            profile = SendingProfile("user@ukr.net", "password123")
            print(f"  Email: {profile.email}")
            print(f"  Display Name: {profile.display_name}")
            print(f"  Proxy: {profile.proxy}")
        elif choice == "0":
            print("Выход...")
        else:
            print("❌ Неизвестная опция")
