# SNOSER-TG v2.0 — Система управления жалобами на Telegram

## 📁 Структура проекта

```
.CreateSNOS-TG/
├── NewLinks.py                 # Основной скрипт рассылки жалоб
├── crypto_email_gen.py         # Генератор email через randommer.io API
├── file1_generator_clean.py    # Улучшенная версия с батч-отправкой
├── ukraine_senders_1200.py     # Генератор 1200 украинских адресов
├── utils.py                    # Утилиты (логирование, конфиг, работа с JSON)
│
├── config/
│   └── settings.json           # Конфиг проекта (домены, SMTP, задержки)
│
├── data/                       # JSON-хранилище данных
│   ├── senders.json            # Сохранённые отправители
│   ├── receivers.json          # Список получателей
│   ├── reports.json            # История отправленных жалоб
│   ├── generated_senders.json  # Сгенерированные через API
│   └── ukraine_senders_1200.json  # Украинские адреса
│
├── logs/                       # Логи выполнения
│   └── snoser.log              # Основной лог файл
│
└── README.md                   # Этот файл
```

## 🔧 Основные улучшения v2.0

### ✅ Исправлена критичная ошибка
- **Проблема**: Переменная `senders` переопределялась только в первой ветви, что вызывало ошибки в остальных
- **Решение**: Создана функция `normalize_senders_domains()`, которая вызывается перед каждой отправкой

### 📊 Добавлено логирование
- Все действия записываются в `logs/snoser.log`
- Уровни логирования: INFO, ERROR, WARNING, DEBUG
- Каждая отправка фиксируется с временной меткой

### 💾 JSON-хранилище данных
- Все данные сохраняются в `data/` папке в JSON-формате
- Возможность загрузки и переиспользования данных
- История всех отправленных жалоб с временными метками

### ⚙️ Конфигурация
- Единый файл конфига `config/settings.json`
- Легко менять домены, SMTP-серверы, задержки
- Настройка логирования и хранилища

## 🚀 Как запустить

### 1. Генерация украинских senders (1200 адресов)
```bash
python3 ukraine_senders_1200.py
# Результат: data/ukraine_senders_1200.json
# Логи: logs/snoser.log
```

### 2. Генерация email через API
```bash
python3 crypto_email_gen.py
# Результат: data/generated_senders.json
```

### 3. Запуск основного скрипта (жалобы)
```bash
python3 NewLinks.py
# Меню с вариантами жалоб:
# 1 = Жалоба на пользователя
# 2 = Жалоба на канал
# 3 = Жалоба на бота
# 00 = Выход
```

### 4. Батч-отправка (demo)
```bash
python3 file1_generator_clean.py
# Меню:
# 1 = Генерация прокси
# 2 = Тест отправки (demo)
# 3 = Загрузить senders из JSON и отправить
```

## 📝 Конфигурация (config/settings.json)

### Домены
```json
"domains": {
  "ukraine": [
    "ukr.net",
    "i.ua",
    "meta.ua",
    "gmail.com.ua",
    "outlook.ua",
    "proton.me"
  ]
}
```

### SMTP-серверы
```json
"smtp": {
  "providers": {
    "mail.ru": {"server": "smtp.mail.ru", "port": 587},
    "gmail.com": {"server": "smtp.gmail.com", "port": 587},
    "rambler.ru": {"server": "smtp.rambler.ru", "port": 587}
  }
}
```

### Задержки (в миллисекундах)
```json
"delays": {
  "between_emails_ms": 500,
  "between_batches_ms": 3000
}
```

## 📊 Логирование

Все события записываются в `logs/snoser.log`:

```
2026-05-28 14:30:45,123 - SNOSER - INFO - Нормализировано 100 отправителей
2026-05-28 14:30:46,456 - SNOSER - INFO - ✓ Отправлено admin@mail.ru -> abuse@telegram.org
2026-05-28 14:30:47,789 - SNOSER - ERROR - ✗ Ошибка отправки user@mail.ru -> support@telegram.org
```

## 💾 JSON-файлы

### senders.json
```json
{
  "user1@ukr.net": "randomPassword123",
  "user2@i.ua": "anotherPassword456",
  ...
}
```

### reports.json
```json
[
  {
    "timestamp": "2026-05-28T14:30:45.123456",
    "data": {
      "sender": "admin@mail.ru",
      "receiver": "abuse@telegram.org",
      "status": "sent",
      "reason": "spam"
    }
  },
  ...
]
```

## 🔐 Безопасность

- Все пароли хранятся в JSON-файлах (не коммитить в git!)
- Логи содержат информацию о попытках отправки
- SMTP использует TLS (587 порт)

## 🛠️ Работа с функциями

### normalize_senders_domains()
Нормализирует домены на украинские:
```python
normalized = normalize_senders_domains(senders, use_ukrainian=True)
# user@mail.ru -> user@ukr.net
```

### send_email()
Отправляет письмо с логированием:
```python
success = send_email(receiver, sender_email, sender_password, subject, body)
```

### DataManager
Работа с JSON:
```python
# Сохранение
DataManager.save_senders(senders_dict)

# Загрузка
senders_dict = DataManager.load_senders()

# Сохранение отчёта
DataManager.save_report({"sender": "...", "receiver": "...", "status": "sent"})
```

### Logger
Логирование:
```python
logger = Logger()
logger.info("Сообщение")
logger.error("Ошибка")
logger.warning("Предупреждение")
logger.debug("Отладка")
```

## 📈 Пример использования

```python
from utils import Config, Logger, DataManager

# Инициализация
config = Config()
logger = Logger()

# Загрузка senders
senders = DataManager.load_senders("data/ukraine_senders_1200.json")

# Логирование
logger.info(f"Загружено {len(senders)} отправителей")

# Работа с конфигом
ukr_domains = config.get('domains.ukraine')
smtp_config = config.get('smtp.providers.mail.ru')
```

## 📞 Контакты и поддержка

- **Разработчик**: @ozxea
- **Версия**: 2.0
- **Обновлено**: 2026-05-28

## ⚖️ Дисклеймер

Этот инструмент предназначен только для **легальных целей** и в соответствии с законодательством. 
Автор не несёт ответственность за неправомерное использование.

---

**Последние обновления:**
- ✅ Исправлена критичная ошибка с `senders` (v2.0)
- ✅ Добавлено логирование всех операций
- ✅ Реализовано JSON-хранилище данных
- ✅ Создана утилита конфигурации
- ✅ Структурирована организация проекта

---

## 🇺🇦 ОБНОВЛЕНИЕ НА УКРАИНСКИЕ ДАННЫЕ

### Что было обновлено (2026-05-29):

✅ **Файлы данных:**
- `data/ukraine_senders_1200.json` — 1200 украинских email-адресов
- `data/ukraine_senders_sample.json` — Пример (100 адресов для тестирования)
- `data/receivers.json` — Адреса поддержки Telegram

✅ **Конфигурация (config/settings.json):**
- Обновлены пути к файлам на украинские версии
- Добавлены SMTP-серверы украинских провайдеров
- Настроены украинские домены по приоритету

✅ **Украинские домены:**
```
- ukr.net       (Укрнет)
- i.ua          (Інтернет України)
- ua.fm         (Альтернативный)
- ua.org        (Организационный)
- proton.me     (ProtonMail)
- protonmail.com (ProtonMail)
```

✅ **SMTP-провайдеры:**
```
- smtp.ukr.net       (587)
- smtp.i.ua          (587)
- smtp.meta.ua       (587)
- smtp.proton.me     (587)
```

### Как использовать украинские данные:

```bash
# 1. Проверить статус
python3 check_ukrainian_data.py

# 2. Сгенерировать новые если нужно
python3 ukraine_senders_1200.py

# 3. Запустить с украинскими данными
python3 NewLinks.py
# Автоматически используются:
# - ukraine_senders_1200.json
# - Украинские домены
# - SMTP-серверы для .ua доменов
```

### Структура файла данных:
```json
{
  "user0001@ukr.net": "randomPassword123!@#",
  "sender0002@i.ua": "anotherPassword456!@#",
  "account0003@ua.fm": "thirdPassword789!@#",
  ...
}
```

### Вспомогательные скрипты:
- `check_ukrainian_data.py` — Проверка статуса украинских данных
- `generate_ukrainian_data.py` — Генератор данных (альтернативный)

---

✨ **Готово к использованию украинских данных!**
