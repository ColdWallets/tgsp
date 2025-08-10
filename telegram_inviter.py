import time
import random
from typing import List
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# URL Telegram Web
TELEGRAM_WEB_URL = "https://web.telegram.org/k/"

# Список юзернеймов, которым нужно отправить приглашение
CONTACT_USERNAMES: List[str] = [
    "second_account_username",
    # добавьте другие юзернеймы при необходимости
]

# Набор разных приглашений
INVITATION_TEXTS: List[str] = [
    "Привет! Хочу пригласить тебя на свой день рождения. Буду рад видеть! 🎉",
    "День рождения скоро! Буду счастлив, если ты придёшь праздновать со мной!",
    "Хэй! В эту субботу отмечаю др, приходи, будет весело!",
]


def human_delay(a: float = 0.5, b: float = 1.5) -> None:
    """Случайная задержка для имитации человеческого поведения."""
    time.sleep(random.uniform(a, b))


def type_like_human(element, text: str) -> None:
    """Печатает текст символ за символом с небольшими задержками."""
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.02, 0.25))


def send_invitation(driver, username: str) -> None:
    """Открывает чат по username и отправляет одно из случайных приглашений."""
    search_box = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.XPATH, "//input[@type='text' and contains(@class, 'search-input')]")
        )
    )
    search_box.click()
    human_delay()
    search_box.clear()
    search_box.send_keys(username)
    human_delay(1, 2)
    search_box.send_keys(Keys.ENTER)

    message_box = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true']"))
    )

    text = random.choice(INVITATION_TEXTS)
    type_like_human(message_box, text)
    human_delay(1, 2)
    message_box.send_keys(Keys.ENTER)
    print(f"Приглашение отправлено {username}!")


def main() -> None:
    service = Service("/path/to/chromedriver")  # замените на путь к драйверу
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(TELEGRAM_WEB_URL)
        print("Открылся Telegram Web — авторизуйтесь и затем нажмите Enter в консоли.")
        input()

        for username in CONTACT_USERNAMES:
            send_invitation(driver, username)
            human_delay(2, 4)
    finally:
        human_delay(2, 3)
        driver.quit()


if __name__ == "__main__":
    main()
