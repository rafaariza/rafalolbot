import requests, os
from bs4 import BeautifulSoup

URL = "https://www.g2g.com/dreamsmurfs"

BOT_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


def send_telegram(message):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": message
        },
        timeout=10
    )


def website_contains_no_offer():
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 Chrome/137.0 Safari/537.36"
        )
    }

    response = requests.get(URL, headers=headers, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    page_text = soup.get_text(" ", strip=True)

    return "No offer yet" in page_text


def main():
    try:
        if website_contains_no_offer():
            send_telegram("❌ No offer")
        else:
            send_telegram(f"🚨 Offer available!\n{URL}")
    except Exception as e:
        send_telegram(f"⚠️ Error checking website:\n{e}")


if __name__ == "__main__":
    main()
