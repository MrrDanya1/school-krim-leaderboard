import os
import urllib.parse
import requests

TOKEN = os.environ["BOT_TOKEN"]
SITE = os.environ.get("SITE_URL", "https://mrrdanya1.github.io/school-krim-leaderboard/")

API = f"https://api.telegram.org/bot{TOKEN}"

def tg(method, data=None):
    r = requests.post(f"{API}/{method}", data=data or {}, timeout=40)
    r.raise_for_status()
    return r.json()

def main():
    offset = 0
    while True:
        data = tg("getUpdates", {"timeout": 30, "offset": offset + 1})
        for update in data.get("result", []):
            offset = update["update_id"]
            msg = update.get("message") or {}
            chat = msg.get("chat", {})
            user = msg.get("from", {})
            text = msg.get("text", "")
            if not chat:
                continue

            if text.startswith("/start"):
                username = user.get("username") or user.get("first_name") or "user"
                safe = urllib.parse.quote(username, safe="")
                link = f"{SITE}?registered=1&username={safe}"
                tg("sendMessage", {
                    "chat_id": chat["id"],
                    "text": "✅ Регистрация подтверждена!\n\nНажми кнопку ниже, чтобы открыть «Битву школ Евпатории».",
                    "reply_markup": '{"inline_keyboard":[[{"text":"🏫 Открыть сайт","url":"'+link+'"}]]}'
                })
            else:
                tg("sendMessage", {
                    "chat_id": chat["id"],
                    "text": "Привет! Для регистрации используй команду /start."
                })

if __name__ == "__main__":
    main()
