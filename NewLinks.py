from colored import cprint
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import sys
import time
from colorama import init
init()
from colorama import Fore, Back, Style
from pystyle import *
from utils import Config, Logger, DataManager
from proxy_generator import ProxyGenerator, DataRandomizer, IPRotator, SendingProfile
from sending_config import SendingConfig

# ═══════════════════════════════════════════════════════════
# 🎨 ГЛАВНЫЙ ЛОГОТИП
# ═══════════════════════════════════════════════════════════

intro = r"""
 ______     ______     __  __     ______     ______    
/\  __ \   /\___  \   /\_\_\_\   /\  ___\   /\  __ \   
\ \ \/\ \  \/_/  /__  \/_/\_\/_  \ \  __\   \ \  __ \  
 \ \_____\   /\_____\   /\_\/\_\  \ \_____\  \ \_\ \_\ 
  \/_____/   \/_____/   \/_/\/_/   \/_____/   \/_/\/_/ 

            🔥 SNOSER-TG 2.0 (UKRAINIAN) 🔥
           ╔═════════════════════════════╗
           ║   Нажми Enter для старта    ║
           ╚═════════════════════════════╝
"""

Anime.Fade(Center.Center(intro), Colors.red_to_blue, Colorate.Vertical, interval=0.05, enter=True)

# ═══════════════════════════════════════════════════════════
# 📊 МЕНЮ
# ═══════════════════════════════════════════════════════════

menu_text = r"""
 ______     ______     __  __     ______     ______    
/\  __ \   /\___  \   /\_\_\_\   /\  ___\   /\  __ \   
\ \ \/\ \  \/_/  /__  \/_/\_\/_  \ \  __\   \ \  __ \  
 \ \_____\   /\_____\   /\_\/\_\  \ \_____\  \ \_\ \_\ 
  \/_____/   \/_____/   \/_/\/_/   \/_____/   \/_/\/_/ 

            РАЗРАБ: Andrii | ВЕРСИЯ: 2.0+
                  ЧТО ЕБНЕМ?
            
  1️⃣  - ПОЛЬЗОВАТЕЛЬ      3️⃣  - БОТ
  2️⃣  - КАНАЛ            4️⃣  - НАСТРОИТЬ ПРОКСИ
  5️⃣  - ПАРАМЕТРЫ ОТПРАВКИ 0️⃣0️⃣  - ВЫХОД
"""

print(Colorate.Vertical(Colors.green_to_cyan, Center.XCenter(menu_text)))

COLOR_CODE = {
    "RESET": "\033[0m",
    "UNDERLINE": "\033[04m",
    "GREEN": "\033[32m",
    "YELLOW": "\033[93m",
    "RED": "\033[31m",
    "CYAN": "\033[36m",
    "BOLD": "\033[01m",
    "PINK": "\033[95m",
    "URL_L": "\033[36m",
    "LI_G": "\033[92m",
    "F_CL": "\033[0m",
    "DARK": "\033[90m",
}



def load_senders():
    config = Config()
    # Приоритет: ukraine_senders -> сендеры из конфига -> другие источники
    ukraine_file = 'data/ukraine_senders_1200.json'
    senders_file = config.get('data_storage.senders_file', 'data/ukraine_senders_1200.json')
    
    # Сначала пробуем украинский файл
    senders = DataManager.load_senders(ukraine_file)
    if isinstance(senders, dict) and senders:
        Logger().info(f"✓ Украинские отправители загружены: {len(senders)} адресов")
        return senders
    
    # Потом файл из конфига
    senders = DataManager.load_senders(senders_file)
    if isinstance(senders, dict) and senders:
        Logger().info(f"Senders загружены из {senders_file}: {len(senders)}")
        return senders
    
    # Другие источники
    for fallback in ('data/generated_senders.json', 'data/senders.json'):
        senders = DataManager.load_senders(fallback)
        if isinstance(senders, dict) and senders:
            Logger().warning(f"Senders загружены из {fallback}: {len(senders)}")
            return senders
    
    Logger().error('❌ Не найдены отправители. Запустите ukraine_senders_1200.py')
    return {}


def load_receivers():
    config = Config()
    receivers_file = config.get('data_storage.receivers_file', 'data/receivers.json')
    receivers = DataManager.load_senders(receivers_file)
    if isinstance(receivers, str):
        receivers = [item.strip() for item in receivers.split(',') if item.strip()]
    if isinstance(receivers, list):
        addresses = [item.strip() for item in receivers if isinstance(item, str) and item.strip()]
        if addresses:
            return addresses
    if isinstance(receivers, dict):
        addresses = [item.strip() for item in receivers.keys() if isinstance(item, str) and item.strip()]
        if addresses:
            return addresses
    default_receivers = [
        'sms@telegram.org',
        'dmca@telegram.org',
        'abuse@telegram.org',
        'support@telegram.org'
    ]
    Logger().warning(f"Receivers не найдены в {receivers_file}, используется дефолтный список")
    return default_receivers


senders = load_senders()
receivers = load_receivers()

def normalize_senders_domains(senders_dict, use_ukrainian=True):
    """Нормализирует домены отправителей на украинские с рандомизацией"""
    logger = Logger()
    config = Config()
    
    if not use_ukrainian:
        return senders_dict
    
    UKR_DOMAINS = config.get('domains.ukraine', [
        'ukr.net', 'i.ua', 'meta.ua', 'gmail.com.ua', 'outlook.ua', 'proton.me'
    ])
    
    try:
        normalized = {}
        for email, pwd in list(senders_dict.items()):
            try:
                local = email.split('@')[0]
                new_domain = random.choice(UKR_DOMAINS)
                new_email = f"{local}@{new_domain}"
                normalized[new_email] = pwd
                logger.debug(f"Нормализирован домен: {email} -> {new_email}")
            except Exception as e:
                logger.warning(f"Ошибка нормализации {email}: {e}")
                normalized[email] = pwd
        
        logger.info(f"✓ Нормализировано {len(normalized)} отправителей (украинские домены)")
        return normalized
    except Exception as e:
        logger.error(f"Критичная ошибка нормализации: {e}")
        return senders_dict

def menu():
    choice = input(f'{COLOR_CODE["RED"]}[ДАВАЙ ВЫБИРАЙ, И ПУСТЬ ВЕСЕЛЬЕ НАЧНЕТЬСЯ)]➤ {COLOR_CODE["RED"]} ')
    return choice

def send_email(receiver, sender_email, sender_password, subject, body):
    logger = Logger()
    try:
        # Рандомизируем задержку перед отправкой
        delay = DataRandomizer.randomize_delays()
        time.sleep(delay)
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver
        msg['Subject'] = subject
        
        # Добавляем вариацию в текст для избежания фильтров
        varied_body = DataRandomizer.add_variation_to_text(body)
        msg.attach(MIMEText(varied_body, 'plain', 'utf-8'))

        config = Config()
        providers = config.get('smtp.providers', {})
        smtp_server = None
        smtp_port = None
        
        # Определяем SMTP сервер по домену
        for domain_key, domain_config in providers.items():
            if domain_key in sender_email:
                smtp_server = domain_config.get('server')
                smtp_port = domain_config.get('port')
                break
        
        if not smtp_server:
            smtp_server = 'smtp.mail.ru'
            smtp_port = 587

        # Подключаемся с таймаутом
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver, msg.as_string())
        time.sleep(0.5)
        server.quit()
        
        logger.info(f"✓ Отправлено {sender_email} -> {receiver}")
        return True
        
    except smtplib.SMTPAuthenticationError:
        logger.error(f"✗ Ошибка аутентификации {sender_email}")
        return False
    except smtplib.SMTPException as e:
        logger.error(f"✗ SMTP ошибка {sender_email}: {e}")
        return False
    except Exception as e:
        logger.error(f"✗ Ошибка отправки {sender_email} -> {receiver}: {e}")
        return False

def main():
    sent_emails = 0
    choice = menu()
    
    # Инициализируем IP ротатор для смены прокси
    ip_rotator = IPRotator()
    logger = Logger()
    
    # Обработка опции 4 - Настройка прокси
    if choice == '4':
        print("\n" + "="*50)
        print("⚙️  НАСТРОЙКА ПРОКСИ")
        print("="*50)
        proxy_menu = """
  1️⃣  - ДОБАВИТЬ СВОИ ПРОКСИ
  2️⃣  - ПОКАЗАТЬ ТЕКУЩИЕ ПРОКСИ
  3️⃣  - НАЗАД В ГЛАВНОЕ МЕНЮ
"""
        print(proxy_menu)
        proxy_choice = input("Выбирай: ").strip()
        
        if proxy_choice == '1':
            ProxyGenerator.add_custom_proxy_interactive()
            # Перезагружаем ротатор с новыми прокси
            ip_rotator = IPRotator(use_custom_proxies=True)
        elif proxy_choice == '2':
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
            stats = ip_rotator.get_proxy_stats()
            print(f"\n📊 Статистика:")
            print(f"  Всего прокси: {stats['total']}")
            print(f"  Неработающих: {stats['failed']}")
            print(f"  Ротаций: {stats['rotations']}")
        return  # Выходим после настройки
    
    # Обработка опции 5 - Параметры отправки
    if choice == '5':
        SendingConfig.interactive_setup()
        return  # Выходим после настройки
    
    if choice == '1':
        print("за что ебнем быдлу?")
        print("1. спам/реклама ")
        print("2. докс/деанон ")
        print("3. ненормативная лексика (троллинг) ")
        print("4. пиздит сессии")
        print("5. вирт номер ")
        comp_choice = input("выберай : ")
        
        # Загружаем конфигурацию
        config = SendingConfig.load()
        batch_size = config.get('batch_settings', {}).get('senders_per_batch', 30)
        timing_config = config.get('timing', {})
        min_delay = timing_config.get('min_delay_between_emails', 0.5)
        max_delay = timing_config.get('max_delay_between_emails', 3.0)
        
        print(f"\n📊 ПАРАМЕТРЫ ОТПРАВКИ:")
        print(f"  • Отправителей за сессию: {batch_size}")
        print(f"  • Задержка между письмами: {min_delay}-{max_delay}s")
        total_emails = batch_size * len(receivers)
        print(f"  • Итого писем: ~{total_emails}")
        
        if comp_choice in ["1", "2", "3"]:
            print("Пиши то что прошу)")
            username = input("юз: ")
            id = input("айди: ")
            chat_link = input("ссылка на чат: ")
            violation_link = input("ссылка на нарушение: ")
            print("⏳ Подготовка отправки...")
            
            comp_texts = {
                "1": f"Здравствуйте, уважаемая поддержка. На вашей платформе я нашел пользователя который отправляет много ненужных сообщений - СПАМ. Его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушения - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю.",
                "2": f"Здравствуйте, уважаемая поддержка, на вашей платформе я нашел пользователя, который распространяет чужие данные без их согласия. его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение/нарушения - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю путем блокировки его акккаунта.",
                "3": f"Здравствуйте, уважаемая поддержка телеграм. Я нашел пользователя который открыто выражается нецензурной лексикой и спамит в чатах. его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение/нарушения - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю путем блокировки его акккаунта."
            }

            normalized_senders = normalize_senders_domains(senders, use_ukrainian=True)
            
            # Ограничиваем до batch_size отправителей
            senders_to_use = dict(list(normalized_senders.items())[:batch_size])
            
            for idx, (sender_email, sender_password) in enumerate(senders_to_use.items()):
                for receiver in receivers:
                    try:
                        # Ротируем IP каждые 5 отправок
                        if idx % 5 == 0:
                            proxy = ip_rotator.get_next_proxy()
                            logger.debug(f"IP ротация: {proxy}")
                        
                        comp_text = comp_texts[comp_choice]
                        comp_body = comp_text.format(username=username.strip(), id=id.strip(), chat_link=chat_link.strip(),
                                                     violation_link=violation_link.strip())
                        
                        if send_email(receiver, sender_email, sender_password, 'О Т П Р А В И Л О С Ь', comp_body):
                            cprint(f"✓ отправилось на {receiver} от {sender_email}!", "green")
                            sent_emails += 1
                        else:
                            cprint(f"✗ ошибка отправки на {receiver} от {sender_email}", "red")
                        
                        # Используем конфигурируемую задержку между отправками
                        delay = random.uniform(min_delay, max_delay)
                        time.sleep(delay)
                        
                    except Exception as e:
                        logger.error(f"Критичная ошибка в цикле отправки: {e}")
                        continue
                
                # Большая задержка после каждого отправителя
                if idx % 3 == 0 and idx != 0:
                    big_delay = random.uniform(5, 15)
                    print(f"⏸️  Пауза {big_delay:.1f}сек (защита от бана)...")
                    time.sleep(big_delay)
                    
        elif comp_choice == "4":
            print("по сессий.")
            username = input("юз: ")
            id = input("айди: ")
            print("⏳ Подготовка отправки...")
            
            comp_texts = {
                "4": f"Здравствуйте, уважаемая поддержка. Я случайно перешел по фишинговой ссылке и утерял доступ к своему аккаунту. Его юзернейм - {username}, его айди - {id}. Пожалуйста удалите аккаунт или обнулите сессии"
            }

            normalized_senders = normalize_senders_domains(senders, use_ukrainian=True)
            for idx, (sender_email, sender_password) in enumerate(normalized_senders.items()):
                for receiver in receivers:
                    try:
                        comp_text = comp_texts[comp_choice]
                        comp_body = comp_text.format(username=username.strip(), id=id.strip())
                        
                        if send_email(receiver, sender_email, sender_password, 'Я утерял свой аккаунт в телеграм', comp_body):
                            cprint(f"✓ отправилось на {receiver} от {sender_email}!", "green")
                            sent_emails += 1
                        
                        delay = DataRandomizer.randomize_delays()
                        time.sleep(delay)
                    except Exception as e:
                        logger.error(f"Ошибка: {e}")
                        continue

        elif comp_choice in ["5", "6"]:
            print("ой красава")
            username = input("юз : ")
            id = input("айди : ")
            print("⏳ Подготовка отправки...")
            
            comp_texts = {
                "5": f"Добрый день поддержка Telegram!Аккаунт {username} , {id} использует виртуальный номер купленный на сайте по активации номеров. Отношения к номеру он не имеет, номер никак к нему не относиться.Прошу разберитесь с этим. Заранее спасибо!"
            }

            normalized_senders = normalize_senders_domains(senders, use_ukrainian=True)
            for idx, (sender_email, sender_password) in enumerate(normalized_senders.items()):
                for receiver in receivers:
                    try:
                        comp_text = comp_texts[comp_choice]
                        comp_body = comp_text.format(username=username.strip(), id=id.strip())
                        
                        if send_email(receiver, sender_email, sender_password, 'О Т П Р А В И Л О С Ь', comp_body):
                            cprint(f"✓ отправилось на {receiver} от {sender_email}!", "green")
                            sent_emails += 1
                        
                        delay = DataRandomizer.randomize_delays()
                        time.sleep(delay)
                    except Exception as e:
                        logger.error(f"Ошибка: {e}")
                        continue

    elif choice == "2":
        print("за что ебнем канал?")
        print("1. слив данных ")
        print("2. живодёрство ")
        print("3. детское п... ")
        print("4. прайс лист по типу докса и свата")
        ch_choice = input("выбирай: ")
        
        if ch_choice in ["1", "2", "3", "4"]:
            channel_link = input("ссылка на канал: ")
            channel_violation = input("ссылка на нарушение (в канале): ")
            print("⏳ Подготовка отправки...")
            
            comp_texts = {
                "1": f"Здравствуйте, уважаемая поддержка телеграм. На вашей платформе я нашел канал, который распространяет личные данные невинных людей. Ссылка на канал - {channel_link}, сслыки на нарушения - {channel_violation}. Пожалуйста заблокируйте данный канал.",
                "2": f"Здравствуйте, уважаемая поддержка телеграма. На вашей платформе я нашел канал который распространяет жестокое обращение с животными. Ссылка на канал - {channel_link}, сслыки на нарушения - {channel_violation}. Пожалуйста заблокируйте данный канал.",
                "3": f"Здравствуйте, уважаемая поддержка телеграма. На вашей платформе я нашел канал который распространяет порнографию с участием несовершеннолетних. Ссылка на канал - {channel_link}, сслыки на нарушения - {channel_violation}. Пожалуйста заблокируйте данный канал.",
                "4": f"Здравствуйте,уважаемый модератор телеграмм,хочу пожаловаться вам на канал,который продает услуги доксинга, сваттинга. Ссылка на телеграмм канал:{channel_link} Ссылка на нарушение:{channel_violation} Просьба заблокировать данный канал."
            }

            normalized_senders = normalize_senders_domains(senders, use_ukrainian=True)
            for idx, (sender_email, sender_password) in enumerate(normalized_senders.items()):
                for receiver in receivers:
                    try:
                        comp_text = comp_texts[ch_choice]
                        comp_body = comp_text.format(channel_link=channel_link.strip(), channel_violation=channel_violation.strip())
                        
                        if send_email(receiver, sender_email, sender_password, 'О Т П Р А В И Л О С Ь', comp_body):
                            cprint(f"✓ успешно отправилось на {receiver} от {sender_email}!", "green")
                            sent_emails += 1
                        
                        delay = DataRandomizer.randomize_delays()
                        time.sleep(delay)
                    except Exception as e:
                        logger.error(f"Ошибка: {e}")
                        continue
                
                if idx % 3 == 0 and idx != 0:
                    big_delay = random.uniform(5, 15)
                    print(f"⏸️  Пауза {big_delay:.1f}сек (защита от бана)...")
                    time.sleep(big_delay)

    elif choice == "3":
        print("мне лень много вариантов давать, по этому по рофлу только за пробив (по типу гб)")
        print("1. пробив ")
        bot_ch = input("выбирай ")

        if bot_ch == "1":
            bot_user = input("юз ")
            print("⏳ Подготовка отправки...")
            
            comp_texts = {
                "1": f"Здравствуйте, уважаемая поддержка телеграм. На вашей платформе я нашел бота, который осуществляет поиск по личным данным ваших пользователей. Ссылка на бота - {bot_user}. Пожалуйста разберитесь и заблокируйте данного бота."
            }
            
            normalized_senders = normalize_senders_domains(senders, use_ukrainian=True)
            for idx, (sender_email, sender_password) in enumerate(normalized_senders.items()):
                for receiver in receivers:
                    try:
                        comp_text = comp_texts[bot_ch]
                        comp_body = comp_text.format(bot_user=bot_user.strip())
                        
                        if send_email(receiver, sender_email, sender_password, 'Жалоба на бота телеграм', comp_body):
                            cprint(f"✓ Отправлено на {receiver} от {sender_email}!", "green")
                            sent_emails += 1
                        
                        delay = DataRandomizer.randomize_delays()
                        time.sleep(delay)
                    except Exception as e:
                        logger.error(f"Ошибка: {e}")
                        continue
    
    elif choice == "00":
        print("👋 До свидания!")
        sys.exit(0)
    
    # Итоговый отчет
    print("\n" + "="*50)
    print(f"📊 ИТОГОВЫЙ ОТЧЕТ")
    print("="*50)
    print(f"✓ Всего отправлено: {sent_emails} писем")
    print(f"✓ IP ротаций: {ip_rotator.rotation_count}")
    logger.info(f"Сессия завершена. Всего отправлено: {sent_emails} писем")
          
if __name__ == "__main__":
    main()
