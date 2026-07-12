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

        page = browser.new_page()

        page.goto(URL, wait_until="domcontentloaded", timeout=60000)

        # Wait until the page finishes rendering
        page.wait_for_timeout(5000)

        print("Current URL:", page.url)
        print("Title:", page.title())

        text = page.locator("body").inner_text()

        print("=" * 50)
        print(text)
        print("=" * 50)
        
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
