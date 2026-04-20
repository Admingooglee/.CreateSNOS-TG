import requests
import time

RANDOMMER_API_KEY = "тут_твой_API_ключ_от_randommer.io"  # https://randommer.io/signup
EMAIL_COUNT = 1000

def fetch_emails(count):
    emails = []
    url = "https://randommer.io/api/Email/Free"
    headers = {"X-Api-Key": RANDOMMER_API_KEY}
    batch_size = 20  # максимальный лимит per request у randommer.io
    while len(emails) < count:
        try:
            resp = requests.get(url, headers=headers)
            if resp.ok:
                email = resp.json()
                if email not in emails:
                    emails.append(email)
            else:
                print("API error:", resp.status_code, resp.text)
            time.sleep(0.2)  # чтобы не ловить rate-limit
        except Exception as ex:
            print("Ошибка при запросе randommer.io:", ex)
            time.sleep(2)
    return emails[:count]

# Пример использования
if __name__ == "__main__":
    print("Генерируем тестовые email-адреса через randommer.io...")
    emails = fetch_emails(EMAIL_COUNT)
    print(f"Сгенерировано {len(emails)} email-ов.")
    # Превращаем в senders-словарь с дефолтными паролями (или генерируй свои)
    senders = {email: "test_password1234" for email in emails}
    # Можно сохранить в файл или сразу юзать в твоем рассыльщике:
    # with open('generated_senders.txt', 'w') as f:
    #     for k, v in senders.items():
    #         f.write(f"{k}:{v}\n")