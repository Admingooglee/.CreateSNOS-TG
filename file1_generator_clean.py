import random
import time
import smtplib
from termcolor import cprint, colored
from pystyle import Colors, Colorate
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# -- если нужен SMTP через SOCKS5 --
# pip install PySocks
USE_PROXY = False
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
    proxies = []
    for _ in range(count):
        ip = ".".join(str(random.randint(1, 254)) for _ in range(4))
        port = random.randint(1000, 9999)
        proxy = f"{ip}:{port}"
        proxies.append(proxy)
    with open(filename, "w") as f:
        for proxy in proxies:
            f.write(proxy + "\n")
    cprint(f"[INFO] Сгенерировано {count} прокси, сохранено в {filename}", "cyan")
    return proxies

def send_email(receiver, sender_email, sender_password, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        # сервер по домену
        if 'gmail.com' in sender_email:
            smtp_server, smtp_port = 'smtp.gmail.com', 587
        elif 'rambler.ru' in sender_email:
            smtp_server, smtp_port = 'smtp.rambler.ru', 587
        elif 'mail.ru' in sender_email:
            smtp_server, smtp_port = 'smtp.mail.ru', 587
        else:
            raise ValueError('Не поддерживается email-провайдер')
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        cprint(f"[SMTP ERROR] {sender_email} -> {receiver}: {e}", "red")
        return False

# -- тестовые сендеры --
senders = {
    'alice.one@gmail.com': 'password_for_demo',
    'bob.two@mail.ru': 'password_demo2'
    # ... свои сгенерированные
}

receivers = [
    'abuse@telegram.org',
    'support@telegram.org'
]

def batch_send():
    subject = "Тестовая жалоба"
    body = "Это тестово�� письмо для проверки SMTP отправки."
    total_sent = 0
    for sender_email, sender_password in senders.items():
        for receiver in receivers:
            ok = send_email(receiver, sender_email, sender_password, subject, body)
            status = colored("ОТПРАВЛЕНО", "green") if ok else colored("ОШИБКА", "red")
            print(f"[{status}] от {sender_email} -> {receiver}")
            time.sleep(3)
            total_sent += 1
    cprint(f"Всего попыток отправки: {total_sent}", "yellow")

def main():
    cprint("\nМеню:\n1) Генерация прокси\n2) Тест рассылки email (demo)\n", "cyan")
    choice = input("Выбор пункта: ").strip()
    if choice == "1":
        generate_proxies("proxies_demo.txt", 5)
    elif choice == "2":
        batch_send()
    else:
        cprint("Неизвестный пункт", "red")

if __name__ == "__main__":
    main()