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

     def main():
    sent_emails = 0
    choice = input(f'{color_code["cyan"]}[root]{color_code["bold"]} Выбор пункта >{color_code["yellow"]} ')

    if choice == '1':
        print("1. ЗА СПАМ, РЕКЛАМУ")
        print("2. ЗА ДОКСUНГ")
        print("3. ЗА ТРОЛЛUНГ(ОСК)")
        print("4. ПР0ДАЖА/РЕКЛАМА НАРК0ТЫ")
        print("5. КУРАТ0РСТВО В НАРК0ШОПЕ")
        print("6. ПРОДАЖА ЦП")
        print("7. ВbIМ0ГАНUЕ UНТUМНЫХ ФОТО У НЕСОВЕРШЕННОЛЕТНUХ")
        print("8. УГНЕТАНUЕ НАЦИИ")
        print("9. УГНЕТАНUЕ РЕЛUГUU")
        print("10. РАСПР0СТР0НЯЕТ РАСЧЛЕНЕНКУ")
        print("11. РАСПР0СТР0НЯЕТ ЖUВОДЕРКУ")
        print("12. РАСПР0СТР0НЯЕТ ПОРНУХУ")
        print("13. СУТЕНЕР(ШЛЮХ ПРОДАЕТ)")
        print("14. ПРUЗЫВ К САМ0ВbIПUЛУ")
        print("15. ПРUЗbIВ К ТЕРР0РУ")
        print("16. УГРОЗbI СВАТА U ТП")
        print("17. УГРОЗbI РАСПРАВbI")
        print("18. СНОС СЕССИЙ")
        print("19. С ВUРТ Н0МЕРОМ")
        print("20. С ПРEМКОЙ")
        print("21. ПР0СТ0 СН0С (НЕ ЭФФЕКТUВЕН)")
        cprint("----------------------------------" , "black")
        comp_choice = input("Выбор пункта > ")
        cprint("----------------------------------" , "black")

        if comp_choice in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17" ]:
            print("СЛЕДУЙ УКАЗАНUЯМ")
            username = input("USERNAME: ")
            id = input("TG ID: ")
            chat_link = input("CCbIЛКА НА ЧАТ: ")
            violation_link = input("ССbIЛКА НА НАРУШЕНUЕ В ЧАТЕ: ")
            cprint("----------------------------------" , "black")
            cprint("АТАКА НАЧАЛАСb" , "red")
            cprint("----------------------------------" , "black")
            comp_texts = {
                "1": f"Здравствуйте, уважаемая поддержка. На вашей платформе я нашел пользователя который отправляет много ненужных сообщений - СПАМ. Его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушения - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю.",
                "2": f"Здравствуйте, уважаемая поддержка, на вашей платформе я нашел пользователя, который распространяет чужие данные без их согласия. его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение/нарушения - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю путем блокировки его акккаунта.",
                "3": f"Здравствуйте, уважаемая поддержка телеграм. Я нашел пользователя который открыто выражается нецензурной лексикой и спамит в чатах. его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение/нарушения - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю путем блокировки его акккаунта.",
                "4": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который продает и рекламирует наркотические вещества. Его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение - {violation_link}. Пожалуйста примите меры по отношению к данному пользоателю путем блокировки его аккаунта.",
                "5": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который привлекает людей в сферу нарко-бизнеса. Его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю путем блокировни его аккаунта.",
                "6": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который продает порнографические материалы с участием несовешеннолетних. Его юзернейм - {username}, его айди {id}, ссылка на чат - {chat_link}, ссылка на нарушение - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю путем блокировки его аккаунта.",
                "7": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который вымогает фото интимного характера у несовершенно летних, его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение - {violation_link}. Пожалуйста примите меры к данному пользователю путем блокировки его аккаунта.",
                "8": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который угнетает нацию и разжигает конфликты. Его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение - {violation_link}. Пожалуйста примите меры по отношению к данному пользователб=ю путем блокировки его аккаунта.",
                "9": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который угнетает религию и разжигает конфликты. Его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение - {violation_link}. Пожалуйста примите меры по отношению к данному пользоателю путем блокировки его аккаунта.",
                "10": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который распростроняет видео и фото шокирущего контента с убийством людей. Его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю путем блокировки его аккаунта.",
                "11": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который распростроняет видео и фото шокирующего контента с убийством животных. Его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю путем блокировки его аккаунта.",
                "12": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который распростроняет фото и видео порнографического типа. Его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю путем блокировки его аккаунта.",
                "13": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который продает услуги проституции. Его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю путем блокировки его аккаунта.",
                "14": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который отправляет сообщения которые приводят людей к суициду. Его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение - {violation_link}. Пожалуйста примине меры по отношению к данному пользователю путем блокировки его аккаунта.",
                "15": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который отправляет сообщения с призывом к террризму. Его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю путем блокировки его аккаунта.",
                "16": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который угрожает людям распростронением личной информации. Его юзернейи - {username}, его айди {id}, ссылка на чат - {chat_link}, ссылка на нарушение - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю путем блокировки его аккаунта.",
                "17": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя который угрожает людям расправой. Его юзернейм - {username}, его айди - {id}, ссылка на чат - {chat_link}, ссылка на нарушение - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю путем блокировки его аккаунта."
            }
            for sender_email, sender_password in senders.items():
                for receiver in receivers:
                    comp_text = comp_texts[comp_choice]
                    comp_body = comp_text.format(username=username.strip(), id=id.strip(), chat_link=chat_link.strip(),
                                                 violation_link=violation_link.strip())
                    send_email(receiver, sender_email, sender_password, 'Жалоба на аккаунт телеграм', comp_body)
                    cprint(f"ОТПРАВЛЕНО НА {receiver} 0Т {sender_email}", "green")
                    sent_emails += 00
                    time.sleep(5)

        elif comp_choice in ["18", "21"]:
            print("СЛЕДУЙ УКАЗАНUЯМ")
            username = input("USERNAME: ")
            id = input("TG ID: ")
            cprint("----------------------------------" , "black")
            cprint("АТАКА НАЧАЛАСb" , "red")
            cprint("----------------------------------" , "black")
            comp_texts = {
                "18": f"Здравствуйте, уважаемая поддержка. Я случайно перешел по фишинговой ссылке и утерял доступ к своему аккаунту. Его юзернейм - {username}, его айди - {id}. Пожалуйста удалите аккаунт или обнулите сессии",
                "21": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел пользователя с подозрительной активностью на аккаунте. Его юзернейм - {username}, его айди - {id}. Пожалуйста примите меры по отношению к данному пользователю путем блокировки аккаунта."
            }

            for sender_email, sender_password in senders.items():
                for receiver in receivers:
                    comp_text = comp_texts[comp_choice]
                    comp_body = comp_text.format(username=username.strip(), id=id.strip())
                    send_email(receiver, sender_email, sender_password, 'Я утерял свой аккаунт в телеграм', comp_body)
                    cprint(f"ОТПРАВЛЕНО НА {receiver} 0Т {sender_email}", "green")
                    sent_emails += 00
                    time.sleep(5)

        elif comp_choice in ["19", "20"]:
            print("СЛЕДУЙ УКАЗАНUЯМ")
            username = input("USERNAME: ")
            id = input("TG ID: ")
            cprint("----------------------------------" , "black")
            cprint("АТАКА НАЧАЛАСb" , "red")
            cprint("----------------------------------" , "black")
            comp_texts = {
                "19": f"Добрый день поддержка Telegram!Аккаунт {username} , {id} использует виртуальный номер купленный на сайте по активации номеров. Отношения к номеру он не имеет, номер никак к нему не относиться.Прошу разберитесь с этим. Заранее спасибо!",
                "20": f"Добрый день поддержка Telegram! Аккаунт {username} {id} приобрёл премиум в вашем мессенджере чтобы рассылать спам-сообщения и обходить ограничения Telegram.Прошу проверить данную жалобу и принять меры!"
            }

            for sender_email, sender_password in senders.items():
                for receiver in receivers:
                    comp_text = comp_texts[comp_choice]
                    comp_body = comp_text.format(username=username.strip(), id=id.strip())
                    send_email(receiver, sender_email, sender_password, 'Жалоба на пользователя телеграм', comp_body)
                    cprint(f"ОТПРАВЛЕНО НА {receiver} 0Т {sender_email}", "green")
                    sent_emails += 00
                    time.sleep(5)


    elif choice == "2":
        
        print("1. С ЛUЧНЫМU ДАННЫМU")
        print("2. С ЖUВОДЕРСТВ0М ")
        print("3. С ДЕТСКUМ П0РНО")
        print("4. ДЛЯ КАНАЛ0В ТИПА ПРАЙСОВ")
        print("5. С РАСЧЛЕНЕНК0Й")
        print("6. РУЛЕТКU (КАЗUК)")
        print("7. НАРК0-Ш0П")
        print("8. ПРUЗbIВ К ТЕРРОРУ")
        print("9. ПРUЗbIВ К САМ0ВbIПUЛУ")
        print("10. РАЗЖUГАНUE НЕНАВUCTU")
        print("11. ПРОПОГАНДА НАСUЛUЯ")
        print("12. ПРОДАЖА ДЕТСКUХ UНТUМ0К")
        print("13. УГНЕТЕНUЕ НАЦUU")
        print("14. УГНЕТЕНUЕ РЕЛUГUU")
        print("15. С П0РНУХОЙ")
        cprint("----------------------------------" , "black")
        ch_choice = input("ВbIБUРАЙ: ")
        cprint("----------------------------------" , "black")

        if ch_choice in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"]:
            channel_link = input("ССbIЛКА НА КАНАЛ: ")
            channel_violation = input("ССbIЛКА НА НАРУШЕНUЕ В КАНАЛЕ: ")
            cprint("----------------------------------" , "black")
            cprint("АТАКА НАЧАЛАCb" , "red")
            cprint("----------------------------------" , "black")
            comp_texts = {
                "1": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел канал, который распространяет личные данные невинных людей. Ссылка на канал - {channel_link}, ссылки на нарушения - {channel_violation}. Пожалуйста заблокируйте данный канал.",
                "2": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел канал который распространяет жестокое обращение с животными. Ссылка на канал - {channel_link}, сслыки на нарушения - {channel_violation}. Пожалуйста заблокируйте данный канал.",
                "3": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел канал который распространяет порнографию с участием несовершеннолетних. Ссылка на канал - {channel_link}, сслыки на нарушения - {channel_violation}. Пожалуйста заблокируйте данный канал.",
                "4": f"Здравствуйте, уважаемый модератор телеграмма. хочу пожаловаться вам на канал,который продает услуги доксинга, сваттинга. Ссылка на телеграмм канал:{channel_link} Ссылка на нарушение:{channel_violation} Просьба заблокировать данный канал.",
                "5": f"Здравствуйте, уважаемая поддержка Телеграмма. На вашей платформе я нашел канал который распространяет шокирующие кадры убийства людей. Ссылка на телеграмм канал:{channel_link} Ссылка на нарушение:{channel_violation} Просьба заблокировать данный канал.",
                "6": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел канал который распростроняет рулетки или же казино, которые запрещены на территории РФ статьей 171 УКРФ. Ссылка на телеграмм канал:{channel_link} Ссылка на нарушение:{channel_violation} Просьба заблокировать данный канал.",
                "5": f"Здравствуйте, уважаемая поддержка Телеграмма. На вашей платформе я нашел канал который распространяет шокирующие кадры убийства людей. Ссылка на телеграмм канал:{channel_link} Ссылка на нарушение:{channel_violation} Просьба заблокировать данный канал.",
                "7": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел канал который пропогондирует продажу наркотических веществ, которые запрещены на территории РФ статьей 228.1 УКРФ. Ссылка на телеграмм канал:{channel_link} Ссылка на нарушение:{channel_violation} Просьба заблокировать данный канал.",
                "8": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел канал который призывает людей к террору что запрещено на территории РФ статьей 205.2 УКРФ. Ссылка на телеграмм канал:{channel_link} Ссылка на нарушение:{channel_violation} Просьба заблокировать данный канал.",
                "9": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел канал который призывает людей к суициду что запрещено на территории РФ статьей 110.1 УКРФ. Ссылка на телеграмм канал:{channel_link} Ссылка на нарушение:{channel_violation} Просьба заблокировать данный канал.",
                "10": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел канал который разжигает ненависть в сторону определенных людей или же групп лиц. Ссылка на канал:{channel_link} Ссылка на нарушение:{channel_violation} Просьба заблокировать данный канал.",
                "11": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел канал который пропогандирует насилие что запрещено на территории РФ статьей 282 УКРФ. Ссылка на канал:{channel_link} Ссылка на нарушение:{channel_violation} Просьба заблокировать данный канал.",
                "12": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел канал который занимается продажей детских интимных фото что запрещено на территории РФ статьей 242.1 УКРФ. Ссылка на канал:{channel_link} Ссылка на нарушение:{channel_violation} Просьба заблокировать данный канал.",
                "13": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел канал который пропогондирует угнетение нации что запрещено на территории РФ статьей 282 УКРФ. Ссылка на канал:{channel_link} Ссылка на нарушение:{channel_violation} Просьба заблокировать данный канал.",
                "14": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел канал который пропогондирует угнетение религии что запрещено на территории РФ статьей 148 УКРФ. Ссылка на канал:{channel_link} Ссылка на нарушение:{channel_violation} Просьба заблокировать данный канал.",
                "15": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел канал который пропогонирует порнографические материалы. Ссыока на канал - {channel_link}, Ссылка на нарушение - {channel_violation}. Просьба заблокировать данный канал."
            }
            for sender_email, sender_password in senders.items():
                for receiver in receivers:
                    comp_text = comp_texts[ch_choice]
                    comp_body = comp_text.format(channel_link=channel_link.strip(), channel_violation=channel_violation.strip)
                    send_email(receiver, sender_email, sender_password, 'Жалоба на телеграм канал', comp_body)
                    cprint(f"ОТПРАВЛЕНО НА {receiver} 0Т {sender_email}", "green")
                    sent_emails += 100000
                    time.sleep(5)


    elif choice == "3":
        print("1. ГЛА3 Б0ГА ")
        print("2. ТUПА СUНЕГ0 КUТА")
        print("3. ПР0ДАЖА ЦП")
        print("4. М0ШЕННИЧЕСКUЕ СХЕМЫ")
        print("5. СПАМ, РЕКЛАМА")
        print("6. ШАНТАЖ")
        print("7. UЗВРАЩЕНUЯ(СНАФФ,ЦП U ТП)")
        cprint("----------------------------------" , "black")
        bot_ch = input("ВbIБUРАЙ: ")
        cprint("----------------------------------" , "black")

        if bot_ch in ["1", "2", "3", "4", "5", "6", "7"]:
            bot_user = input("USERNAME BOTA: ")
            cprint("----------------------------------" , "black")
            cprint("АТАКА НАЧАЛАСb" , "red")
            cprint("----------------------------------" , "black")
            comp_texts = {
                "1": f"Здравствуйте, уважаемая поддержка телеграм. На вашей платформе я нашел бота, который осуществляет поиск по личным данным ваших пользователей. Ссылка на бота - {bot_user}. Пожалуйста разберитесь и заблокируйте данного бота.",
                "2": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел бота который путем заданий приводит людей к суициду что запрещено на территории РФ статьей 110.1 УКРФ. Ссылка на бота {bot_user}. Пожалуйста разберитесь и заблокируйте данного бота.",
                "3": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел бота который продает порнографические материалы с участием лиц не достигших совершеннолетия, что запрещено на территории РФ статьей 242.1 УКРФ. Ссылка на бота {bot_user}. Пожалуйста разберитесь и заблокируйте данного бота.",
                "4": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел бота который занимается мошенническими схемами и обманывает людей на деньги что запрещено на территории РФ статьей 159 УКРФ. Ссылка на бота {bot_user}. Пожалуйста разберитесь и заблокируйте данного бота.",
                "5": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел бота который рассылает навязчивую рекламу и спамит ей в чатах. Ссылка на бота {bot_user}. Пожалуйста разберитесь и заблокируйте данного бота.",
                "6": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел бота который путем шантажа вымогает из людей деньги, личные данные и другие вещи. Ссылка на бота {bot_user}. Пожалуйста разберитесь и заблокируйте данного бота.",
                "7": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел бота который распростроняет видео шокируещего контента по типу детского порно и расчленения людей. Ссылка на бота {bot_user}. Пожалуйста разберитесь и заблокируйте данного бота."
             }
            for sender_email, sender_password in senders.items():
                for receiver in receivers:
                    comp_text = comp_texts[bot_ch]
                    comp_body = comp_text.format(bot_user=bot_user.strip())
                    send_email(receiver, sender_email, sender_password, 'Жалоба на бота телеграм', comp_body)
                    cprint(f"ОТПРАВЛЕНО НА {receiver} 0Т {sender_email}", "green")
                    sent_emails += 10000
                    time.sleep(5)
        
    elif choice == "4":
        print("1. ПРОСТО СНОС(НЕ ЭФФЕКТUВЕН)")
        print("2. СПАМ/РЕКЛАМА")
        print("3. ЗА АВУ UЛU НАЗВАНUЕ")
        print("4. ПР0П0ГАНДА НАСИЛИЯ U ТП")
        print("5. НАКРУТКА")
        print("6. ОСКU В ЧАТЕ")
        cprint("----------------------------------" , "black")
        bottik = input("ВbIБUРАЙ: ")
        cprint("----------------------------------" , "black")

        if bottik in ["1", "2", "3", "4", "5"]:
            user_chat = input("ССbIЛКА НА ЧАТ: ")
            id_chat = input("TG ID ЧАТА: ")
            cprint("----------------------------------" , "black")
            cprint("АТАКА НАЧАЛАСb" , "red")
            cprint("----------------------------------" , "black")
            comp_texts = {
                "1": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел группу с подозрительной активностью. Ссылка на группу - {user_chat}, Айди группы - {id_chat}. Пожалуйста примите меры в сторону данной группы и заблокируйте ее.",
                "2": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел группу в которой проходят спам-рассылки. Ссылка на группу - {user_chat}, Айди группы - {id_chat}. Пожалуйста примите меры в сторону этой группы и заблокируйте ее как можно скорее.",
                "3": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел группу в которой стоит вызывающая аватарка и имя, разжигающее конфликты. Ссылка на группу - {user_chat}, Айди группы - {id_chat}. Пожалуйста примите меры в сторону этой группы и заблокируйте ее как можно скорее.",
                "4": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел группу в которой пропогондируется насилие и другие подобные жестокости. Ссылка на группу - {user_chat}, Айди группы - {id_chat}. Пожалуйста примите меры в сторону этой группы и заблокируйте ее как можно скорее",
                "5": f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел группу в которой происходит накрутка подписчиков. Ссылка на группу - {user_chat}, Айди группы - {id_chat}. Пожалуйста примите меры в сторону этой группы и заблокируйте ее как можно скорее"
            }
            for sender_email, sender_password in senders.items():
                for receiver in receivers:
                    comp_text = comp_texts[bottik]
                    comp_body = comp_text.format(user_chat=user_chat.strip(), id_chat=id_chat.strip())
                    send_email(receiver, sender_email, sender_password, 'Жалоба на группу телеграм', comp_body)
                    cprint(f"ОТПРАВЛЕНО НА {receiver} 0Т {sender_email}", "green")
                    sent_emails += 10000
                    time.sleep(5)     

        elif bottik == "6":
            username_chat = input("ССbIЛКА НА ЧАТ: ")    
            idtg_chata = input("TG ID CHATA: ")   
            ssilka = input("ССbIЛКА НА НАРУШЕНUЕ: ")
            cprint("----------------------------------" , "black")  
            cprint("ATAKA НАЧАЛАСb" , "red")
            cprint("----------------------------------" , "black")
            comp_texts = {
                "6": f"Здравствуйте, уважаемая поддержка телеграмма. Я нашел группу с которой оскорбляют людей и используют ненормативную лексику в их сторону. Ссылка на группу - {username_chat}, Айди группы - {idtg_chata}, Ссылка на нарушение - {ssilka}. Пожалуйста примите меры в сторону этой группы и заблокируйте ее как можно скорее"
            }
            for sender_email, sender_password in senders.items():
                for receiver in receivers:
                    comp_text = comp_texts[bottik]
                    comp_body = comp_text.format(username_chat=username_chat.strip(), idtg_chata=idtg_chata.strip(), ssilka=ssilka.strip())
                    send_email(receiver, sender_email, sender_password, 'Жалоба на группу телеграм', comp_body)
                    cprint(f"ОТПРАВЛЕНО НА {receiver} 0Т {sender_email}", "green")
                    sent_emails += 10000
                    time.sleep(5)     

  
if __name__ == "__main__":
    main()
