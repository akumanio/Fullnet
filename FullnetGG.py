from fake_useragent import UserAgent
import requests
import random
import string
from termcolor import colored
import pyfiglet
import time

# Функция для создания градиента от вишневого к белому
def gradient_text(text):
    start_color = (255, 0, 0)  # Вишневый (RGB)
    end_color = (255, 255, 255)  # Белый (RGB)
    
    def rgb_to_ansi(r, g, b):
        return f'\x1b[38;2;{r};{g};{b}m'
    
    gradient_text = ''
    num_colors = len(text)
    for i, char in enumerate(text):
        ratio = i / num_colors
        r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
        gradient_text += rgb_to_ansi(r, g, b) + char
    
    gradient_text += '\x1b[0m'  # Сброс цвета
    return gradient_text

# ASCII-арт приветствия
ascii_banner = """
          █████████  ███     ███ ███      ███      ████    ███  ██████████ ███████████
          ███         ███     ███ ███      ███      █████   ███  ███            ███
          ███         ███     ███ ███      ███      ██████  ███  ███            ███
          ███████     ███     ███ ███      ███      ████  ███  ████████         ███
          ███         ███     ███ ███      ███      ███  ████  ███               ███
          ███         ███     ███ ███      ███      ███   █████  ███              ███
          ███         ███ ██████ ███      ███      ███    █████  ███             ███
          ███          ███████  ████████ ████████ ███    █████  ██████████    ███

"""
colored_banner = gradient_text(ascii_banner)

def generate_phone_number():
    country_codes = ['+7', '+380', '+375']
    country_code = random.choice(country_codes)
    phone_number = ''.join(random.choices('0123456789', k=10))
    formatted_phone_number = f'{country_code}{phone_number}'
    return formatted_phone_number

def generate_random_email():
    domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "mail.ru"]
    username = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
    domain = random.choice(domains)
    email = f"{username}@{domain}"
    return email

def send_complaint(username, telegram_id, number, email, repeats, complaint_choice, proxies=None):
    url = 'https://telegram.org/support'
    user_agent = UserAgent().random
    headers = {'User-Agent': user_agent}
    complaints_sent = 0

    complaint_texts = {
        "1": f'Добрый день поддержка Telegram! Аккаунт {username}, {telegram_id} использует виртуальный номер купленный на сайте по активации номеров. Отношения к номеру он не имеет, номер никак к нему не относиться.Прошу разберитесь с этим. Заранее спасибо!',
        "2": f'Аккаунт {username}, {telegram_id} приобрёл премиум в вашем сервисе чтобы обходить наказания за спам и совершает спам-рассылки в личные сообщения пользователям и в чаты. Прошу проверить информацию!',
        "3": f"Здраствуйте. Аккаунт {username}, id {telegram_id} оскорбляет меня и мою маму. Мне это очень не приятно, поэтому и пишу вам. Огромная прозьба разобраться и заблокировать данного пользователя т.к это нарушает политику сервиса. Блгаадарю",
        "4": f"Здраствуйте. Аккаунт {username}, id {telegram_id}. Очень много и частно нарушает политику сервиса Телеграмм. А именно, оскорбляет, сливает личные данные юзеров. Продает различные услуги. Прозьба разобраться и наказать данный аккаунт.",
        "5": f"Здравствуйте, я утерял свой телеграм-аккаунт путем взлома. Я попался на фишинговую ссылку, и теперь на моем аккаунте сидит какой-то человек. Он установил облачный пароль, так что я не могу зайти в свой аккаунт и прошу о помощи. Мой юзернейм — {username}, а мой айди, если злоумышленник поменял юзернейм —  {telegram_id} . Пожалуйста, перезагрузите сессии или удалите этот аккаунт, так как у меня там очень много важных данных.",
        "6": f"Здраствуйте, сидя на просторах сети телеграмм, я заметил пользователя который совершает спам-рассылки, мне и другим пользователям это очень не нравится.Его аккаунт: {username}, ID {telegram_id}.Огромная прозьба разобраться с этим и заблокировать данного пользователя. Заранее спасибо.",
        "7": f"Сидя на просторах телеграмма заметил юзера который продает услуги dеаnонa и лжеминирования, сыллка на канал и юзер админа: {username}, id админа: {telegram_id}. Большая прозьба заблокировать канал и пользователя, т.к это нарушает политику сервиса.",
        "8": f"На сервисе telegram обнаружил пользователя который накручивает на канал реакции, подписки и просмотры. Сыллка на посты с накруткой и аккаунт администратора: {username}, id администратора на случай если поменяет юзернейм: {telegram_id}. Прозьба разобраться и заблокировать пользователя т.к это нарушает правила telegramm"
    }
    
    text = complaint_texts.get(complaint_choice, '')
    if not text:
        print(gradient_text("Неверный выбор жалобы"))
        return

    payload = {'text': text, 'number': number, 'email': email}

    try:
        for _ in range(int(repeats)):
            response = requests.post(url, headers=headers, data=payload, proxies=proxies)
            if response.status_code == 200:
                complaints_sent += 1
                print(gradient_text("Жалоба успешно отправлена"))
                print(gradient_text(f"От: {email} {number}"))
            else:
                print(gradient_text("Не удалось отправить. Код ответа:") + str(response.status_code))
    except Exception as e:
        print(gradient_text("Произошла ошибка:") + str(e))

def complaint():
    print(colored_banner)
    print(gradient_text("                        |  [1] Виртуальный номер     [5] Снос сессий  |     "))
    print(gradient_text("                        |  [2] Премиум Аккаунт       [6] Спам         |     "))
    print(gradient_text("                        |  [3] Оскорбление           [7] Снос Прайса  |     "))
    print(gradient_text("                        |  [4] Нарушение правил      [8] Накрутка     |     "))

    complaint_choice = input(gradient_text("Введите номер: "))

    if complaint_choice in ["1", "2", "3", "4", "5", "6", "7", "8"]:
        username = input(gradient_text("Введите @юзер: "))
        telegram_id = input(gradient_text("Введите Telegram ID: "))
        repeats = int(input(gradient_text("Введите количество жалоб: ")))
        for _ in range(repeats):
            number = generate_phone_number()
            email = generate_random_email()
            proxies_list = [
                '8.218.149.193:80', '47.57.233.126:80', '47.243.70.197:80', '8.222.193.208:80', '144.24.85.158:80',
                '47.245.115.6:80', '47.245.114.163:80', '45.4.55.10:40486', '103.52.37.1:4145', '200.34.227.204:4153',
                '190.109.74.1:33633', '200.54.221.202:4145', '36.67.66.202:5678', '168.121.139.199:4145', '101.255.117.2:51122',
                '45.70.0.250:4145', '78.159.199.217:1080', '67.206.213.202:4145', '14.161.48.76:8080', '8.213.12.58:8080',
                '102.67.121.58:41890', '103.152.23.146:8080', '171.25.186.242:5208', '106.75.108.53:1317', '123.201.58.96:4145'
            ]
            proxy = random.choice(proxies_list)
            proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
            send_complaint(username, telegram_id, number, email, repeats, complaint_choice, proxies)
    else:
        print(gradient_text("Неверный выбор"))

if __name__ == "__main__":
    complaint()

        
        
complaint()
