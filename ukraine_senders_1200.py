import random
import string

DOMAINS = ['ukr.net', 'i.ua', 'ua.fm', 'ua.org', 'proton.me', 'protonmail.com']

def gen_password(length=12):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

senders = {}
for i in range(1, 1201):
    domain = DOMAINS[(i-1) % len(DOMAINS)]
    email = f"user{i:04}@{domain}"
    pwd = gen_password(16)
    senders[email] = pwd

# Вывести первые 10 для примера
for idx, (k, v) in enumerate(senders.items()):
    print(f"'{k}': '{v}',")
    if idx == 9:
        print("...")
        break

# Весь словарь senders готов для вставки