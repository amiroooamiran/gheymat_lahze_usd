import requests
import time
import random
from datetime import datetime
from playwright.sync_api import sync_playwright
import pytz

bot_token = "6703834100:AAEVs5ccc5Mjzg9rd3wHvlXEVlxW_VvZTyQ"
channel_id = "@gheymat_lahze_usd"

def is_market_open():
    # Get current time in Iran timezone
    tz = pytz.timezone('Asia/Tehran')
    iran_time = datetime.now(tz)
    # Check if current time is between 7 AM and 10 PM in Iran
    return 7 <= iran_time.hour < 22

def check_dollar_price():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://mobinzar.com/priceable-object/dollar")
        try:
            dollar = page.locator(
                "//div[contains(@class, 'flex items-center justify-center gap-1 w-full sm:w-[calc(100%-90px)]') and contains(@class, 'sm:rounded-md text-center sm:px-2 md:pt-1 h-6 leading-8 sm:leading-6 mx-0 sm:ms-2 text-sm sm::text-xl md:text-2xl font-bold')]"
            ).inner_text()
            time_of_dollar = page.locator(
                "//div[@class='leading-4 md:leading-[1px]']"
            ).inner_text()

            # Assuming the time from the website is in Persian (Farsi) numerals
            persian_to_english = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")
            time_of_dollar_english = time_of_dollar.translate(persian_to_english)
            dollar = int(dollar.translate(persian_to_english).replace(",", ""))

            # Add a random amount between 50 and 1100 to the price ceiling
            random_addition = random.randint(50, 1100)
            price_ceiling = dollar + random_addition

            # Subtract a random amount between 50 and 1100 from the price floor
            random_subtraction = random.randint(50, 1100)
            price_floor = dollar - random_subtraction

            # Calculate the traded price as the average of the modified ceiling and floor prices
            traded_price = (price_ceiling + price_floor) // 2

            # Increase prices by specified amounts
            price_ceiling += 0
            price_floor += 0
            traded_price += 0

            # Format prices with commas
            price_ceiling_str = f"{price_ceiling:,}"
            price_floor_str = f"{price_floor:,}"
            traded_price_str = f"{traded_price:,}"

            return (
                price_ceiling_str,
                price_floor_str,
                traded_price_str,
                time_of_dollar,
            )

        except Exception as e:
            print(f"Error: {e}")
            return None, None, None, None
        finally:
            browser.close()

def send_message(token, chat_id, text):
    """Function to send a message via the Telegram bot."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {"chat_id": chat_id, "text": text}
    response = requests.post(url, json=params)
    if response.status_code != 200:
        print(f"Failed to send message. Status code: {response.status_code}")
    else:
        print("Message sent successfully!")

def send_start_end_messages(start=True):
    """Send start or end message."""
    price_ceiling, price_floor, traded_price, time_of_dollar = check_dollar_price()
    if price_ceiling is not None and price_floor is not None and traded_price is not None:
        if start:
            message = f"شروع معاملات اولین معامله فردایی:\n\n🔴 قیمت فروش: {price_ceiling} \n\n🔵 قیمت خرید: {price_floor} \n\n✅ معامله شده: {traded_price} \n"
        else:
            message = f"پایان معاملات آخرین معامله فردایی:\n\n🔴 قیمت فروش: {price_ceiling} \n\n🔵 قیمت خرید: {price_floor} \n\n✅ معامله شده: {traded_price} \n"
        send_message(bot_token, channel_id, message)

if __name__ == "__main__":
    sent_start_message = False
    sent_end_message = False

    while True:
        tz = pytz.timezone('Asia/Tehran')
        iran_time = datetime.now(tz)

        if iran_time.hour == 7 and not sent_start_message:
            send_start_end_messages(start=True)
            sent_start_message = True
            sent_end_message = False  # Reset for the next day

        if iran_time.hour == 22 and not sent_end_message:
            send_start_end_messages(start=False)
            sent_end_message = True
            sent_start_message = False  # Reset for the next day

        if is_market_open():
            price_ceiling, price_floor, traded_price, time_of_dollar = check_dollar_price()
            if price_ceiling is not None and price_floor is not None and traded_price is not None:
                gh_froshe = f"🔴 قیمت فروش: {price_ceiling}"
                gh_kharid = f"🔵 قیمت خرید: {price_floor}"
                gh_moamle = f"✅ معامله شده: {traded_price}"

                send_message(bot_token, channel_id, gh_froshe)
                send_message(bot_token, channel_id, gh_kharid)
                send_message(bot_token, channel_id, gh_moamle)

        time.sleep(180)
