import time
import random
from datetime import datetime
from playwright.sync_api import sync_playwright

def is_market_open(persian_time_str):
    # Convert Persian time string to standard time
    persian_time = datetime.strptime(persian_time_str, "%H:%M:%S").time()
    market_open_time = datetime.strptime("07:00:00", "%H:%M:%S").time()
    market_close_time = datetime.strptime("19:00:00", "%H:%M:%S").time()
    return market_open_time <= persian_time <= market_close_time

def check_dollar_price():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://mobinzar.com/priceable-object/dollar")
        
        try:
            dollar = page.locator("//div[contains(@class, 'flex items-center justify-center gap-1 w-full sm:w-[calc(100%-90px)]') and contains(@class, 'sm:rounded-md text-center sm:px-2 md:pt-1 h-6 leading-8 sm:leading-6 mx-0 sm:ms-2 text-sm sm::text-xl md:text-2xl font-bold')]").inner_text()
            time_of_dollar = page.locator("//div[@class='leading-4 md:leading-[1px]']").inner_text()
            
            # Assuming the time from the website is in Persian (Farsi) numerals
            persian_to_english = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")
            time_of_dollar_english = time_of_dollar.translate(persian_to_english)
            dollar = int(dollar.translate(persian_to_english).replace(',', ''))
            
            # Add a random amount between 50 and 1100 to the price ceiling
            random_addition = random.randint(50, 1100)
            price_ceiling = dollar + random_addition

            # Subtract a random amount between 50 and 1100 from the price floor
            random_subtraction = random.randint(50, 1100)
            price_floor = dollar - random_subtraction

            # Calculate the traded price as the average of the modified ceiling and floor prices
            traded_price = (price_ceiling + price_floor) // 2
            
            market_open = is_market_open(time_of_dollar_english)
            
            # Format prices with commas
            price_ceiling_str = f"{price_ceiling:,}"
            price_floor_str = f"{price_floor:,}"
            traded_price_str = f"{traded_price:,}"
            
            return price_ceiling_str, price_floor_str, traded_price_str, time_of_dollar, market_open
        except Exception as e:
            print(f"Error: {e}")
            return None, None, None, None, None
        finally:
            browser.close()

# Initialize previous market state
previous_market_open = None

while True:
    price_ceiling, price_floor, traded_price, time_of_dollar, market_open = check_dollar_price()
    
    if price_ceiling is not None and price_floor is not None and traded_price is not None:
        if market_open and (previous_market_open is None or not previous_market_open):
            print(f"Market is now open. Ceiling price: {price_ceiling}, Floor price: {price_floor}, Traded price: {traded_price} | Time: {time_of_dollar}")
        elif not market_open and (previous_market_open is None or previous_market_open):
            print(f"Market is now closed. Ceiling price: {price_ceiling}, Floor price: {price_floor}, Traded price: {traded_price} | Time: {time_of_dollar}")
        else:
            print(f"Ceiling price: {price_ceiling}, Floor price: {price_floor}, Traded price: {traded_price} | Time: {time_of_dollar}")
        
        previous_market_open = market_open
    else:
        print("Failed to retrieve data.")
    
    time.sleep(180)  # Wait for 3 minutes (180 seconds)
