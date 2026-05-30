#!/usr/bin/env python3
"""
Проверка и установка зависимостей проекта
"""
import sys
import subprocess
import os

REQUIRED_PACKAGES = {
    'colored': 'colored',
    'colorama': 'colorama',
    'pystyle': 'pystyle',
}

OPTIONAL_PACKAGES = {
    'requests': 'requests (для генерирования email)',
    'termcolor': 'termcolor (для цветного вывода)',
    'socks': 'PySocks (для SOCKS5 прокси)',
}

def check_imports():
    """Проверяет доступные импорты"""
    print("═" * 60)
    print("📦 ПРОВЕРКА ЗАВИСИМОСТЕЙ")
    print("═" * 60)
    
    missing = []
    available = []
    
    # Проверяем обязательные пакеты
    print("\n✓ ОБЯЗАТЕЛЬНЫЕ ПАКЕТЫ:")
    for module, name in REQUIRED_PACKAGES.items():
        try:
            __import__(module)
            print(f"  ✅ {name}")
            available.append(module)
        except ImportError:
            print(f"  ❌ {name} - ОТСУТСТВУЕТ!")
            missing.append(module)
    
    # Проверяем опциональные пакеты
    print("\n⚠️  ОПЦИОНАЛЬНЫЕ ПАКЕТЫ:")
    for module, description in OPTIONAL_PACKAGES.items():
        try:
            __import__(module)
            print(f"  ✅ {description}")
        except ImportError:
            print(f"  ⚠️  {description} - отсутствует (не критично)")
    
    print("\n" + "═" * 60)
    
    if missing:
        print(f"\n❌ ОШИБКА: Отсутствуют {len(missing)} пакетов!")
        print("\nУстанови их командой:")
        print(f"  pip install {' '.join(missing)}")
        return False
    else:
        print("✅ Все обязательные пакеты установлены!")
        return True

def install_requirements():
    """Установка всех зависимостей"""
    print("\n📥 УСТАНОВКА ЗАВИСИМОСТЕЙ...")
    
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install',
            'colored', 'colorama', 'pystyle',
            'requests', 'termcolor', 'PySocks'
        ])
        print("✅ Все зависимости установлены!")
        return True
    except Exception as e:
        print(f"❌ Ошибка установки: {e}")
        return False

if __name__ == "__main__":
    if not check_imports():
        print("\n🔧 Хочешь установить зависимости? (y/n): ", end='')
        response = input().strip().lower()
        if response == 'y':
            if install_requirements():
                print("\n✅ Теперь все готово к использованию!")
            else:
                print("\n❌ Установка не удалась, попробуй вручную")
                sys.exit(1)
        else:
            print("\nУстанови зависимости вручную:")
            print("  pip install colored colorama pystyle requests termcolor PySocks")
            sys.exit(1)
