import random
import time
import smtplib
from termcolor import cprint, colored
from pystyle import Colors, Colorate
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from utils import Logger, Config, DataManager

# -- если нужен SMTP через SOCKS5 --
# pip install PySocks
logger = Logger()
config = Config()

USE_PROXY = config.get('features.use_proxies', False)
PROXY_HOST = '127.0.0.1'
PROXY_PORT = 1080

if USE_PROXY:
    import socks
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, PROXY_HOST, PROXY_PORT)
    socks.wrapmodule(smtplib)

# -- красивый баннер --
banner = Colorate.Horizontal(Colors.green_to_cyan, '''
 _______      _             _           _   _             
|__   __|    | |           | |         | | (_)            
   | |  ___  | |_ ___   ___| | __ _  __| |  _  ___  _ __  
   | | / _ \ | __/ _ \ / __| |/ _` |/ _` | | |/ _ \| '_ \ 
   | ||  __/ | || (_) | (__| | (_| | (_| | | | (_) | | | |
   |_| \___|  \__\___/ \___|_|\__,_|\__,_| |_|\___/|_| |_|                                      
       Этичный тестовый скрипт для отправки писем
''')
print(banner)

def generate_proxies(filename, count=5):
    """
    ⚠️ ВНИМАНИЕ: Эта функция генерирует ФЕЙКОВЫЕ прокси!
    Используй только для тестирования.
    
    Для реальной работы используй рабочие прокси:
    - proxy_generator.py add
    - Или добавь в data/custom_proxies.json
    """
    logger.warning("⚠️  Функция generate_proxies() создает ФЕЙКОВЫЕ прокси!")
    logger.warning("    Используй proxy_generator.py для добавления рабочих прокси")
    
    proxies = []
    for _ in range(count):
        # ПРИМЕЧАНИЕ: Это НЕ рабочие прокси! Только для демонстрации
        ip = ".".join(str(random.randint(1, 254)) for _ in range(4))
        port = random.randint(1000, 9999)
        proxy = f"{ip}:{port}"
        proxies.append(proxy)
    
    try:
        with open(filename, "w") as f:
            for proxy in proxies:
                f.write(proxy + "\n")
        logger.warning(f"⚠️  Сгенерировано {count} ФЕЙКОВЫХ прокси в {filename}")
        logger.warning("    Замени их на рабочие прокси перед использованием!")
        return proxies
    except Exception as e:
        logger.error(f"Ошибка сохранения прокси: {e}")
        return []

def send_email(receiver, sender_email, sender_password, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        # сервер по домену
        providers = config.get('smtp.providers', {})
        smtp_server, smtp_port = None, None
        
        for domain_key, domain_config in providers.items():
            if domain_key in sender_email:
                smtp_server = domain_config.get('server')
                smtp_port = domain_config.get('port')
                break
        
        if not smtp_server:
            # fallback на mail.ru если домен не найден
            smtp_server, smtp_port = 'smtp.mail.ru', 587
        
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver, msg.as_string())
        server.quit()
        
        logger.info(f"✓ Email отправлен: {sender_email} -> {receiver}")
        return True
    except Exception as e:
        logger.error(f"✗ SMTP ERROR: {sender_email} -> {receiver}: {e}")
        cprint(f"[SMTP ERROR] {sender_email} -> {receiver}: {e}", "red")
        return False

def batch_send(senders_dict=None):
    if senders_dict is None:
        senders_dict = {
            'alice.one@gmail.com': 'password_for_demo',
            'bob.two@mail.ru': 'password_demo2'
        }
    
    logger.info("=== Начало батч-отправки ===")
    receivers = config.get('data_storage.receivers_file', ['abuse@telegram.org', 'support@telegram.org'])
    
    subject = config.get('subject', "Тестовая жалоба")
    body = config.get('body', "Это тестовое письмо для проверки SMTP отправки.")
    
    total_sent = 0
    for sender_email, sender_password in senders_dict.items():
        for receiver in receivers:
            ok = send_email(receiver, sender_email, sender_password, subject, body)
            status = colored("ОТПРАВЛЕНО", "green") if ok else colored("ОШИБКА", "red")
            print(f"[{status}] от {sender_email} -> {receiver}")
            time.sleep(config.get('delays.between_emails_ms', 500) / 1000)
            total_sent += 1
    
    logger.info(f"Всего попыток отправки: {total_sent}")
    cprint(f"Всего попыток отправки: {total_sent}", "yellow")

def main():
    logger.info("=== Меню batch-отправки ===")
    cprint("\nМеню:\n1) Генерация прокси\n2) Тест рассылки email (demo)\n3) Загрузить senders из JSON\n", "cyan")
    choice = input("Выбор пункта: ").strip()
    
    if choice == "1":
        generate_proxies("proxies_demo.txt", 5)
    elif choice == "2":
        batch_send()
    elif choice == "3":
        logger.info("Загрузка senders из JSON...")
        senders_dict = DataManager.load_senders()
        if senders_dict:
            batch_send(senders_dict)
        else:
            logger.error("Не удалось загрузить senders")
            cprint("✗ Ошибка загрузки senders", "red")
    else:
        logger.warning(f"Неизвестный пункт: {choice}")
        cprint("Неизвестный пункт", "red")

if __name__ == "__main__":
    main()