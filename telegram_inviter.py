import asyncio
import random
from pathlib import Path
from typing import List

from pyrogram import Client

# ----- Настройки файлов -----
USERNAMES_FILE = Path("usernames.txt")
MESSAGES_FILE = Path("messages.txt")

# ----- Настройки Pyrogram -----
API_ID = 123456  # замените на свой api_id
API_HASH = "YOUR_API_HASH"  # замените на свой api_hash
SESSION_NAME = "birthday"  # имя файла сессии


def load_lines(path: Path) -> List[str]:
    """Читает непустые строки из файла, игнорируя комментарии."""
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def human_delay(a: float = 0.5, b: float = 1.5) -> None:
    """Асинхронная задержка для имитации человеческого поведения."""
    return asyncio.sleep(random.uniform(a, b))


async def main() -> None:
    usernames = load_lines(USERNAMES_FILE)
    messages = load_lines(MESSAGES_FILE)

    async with Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH) as app:
        for username in usernames:
            user = await app.get_users(username)
            text = random.choice(messages)

            for _ in text:
                await app.send_chat_action(user.id, "typing")
                await asyncio.sleep(random.uniform(0.02, 0.25))

            await app.send_message(user.id, text)
            print(f"Приглашение отправлено {username}!")
            await human_delay(2, 4)


if __name__ == "__main__":
    asyncio.run(main())
