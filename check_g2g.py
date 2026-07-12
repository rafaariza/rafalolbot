import os
import requests
from playwright.sync_api import sync_playwright

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
        timeout=15
    )


def website_contains_no_offer():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/137.0.0.0 Safari/537.36"
            )
        )

        page.goto(URL, wait_until="networkidle", timeout=60000)

        # Give JavaScript a little extra time
        page.wait_for_timeout(3000)

        text = page.locator("body").inner_text()

        browser.close()

        return "No offer yet" in text


def main():
    try:
        if website_contains_no_offer():
            send_telegram("❌ No offer")
            print("No offer.")
        else:
            send_telegram(f"🚨 OFFER FOUND!\n{URL}")
            print("Offer detected!")

    except Exception as e:
        send_telegram(f"⚠️ Error:\n{e}")
        raise


if __name__ == "__main__":
    main()
