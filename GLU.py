import requests
import time


bot_token = '6703834100:AAEVs5ccc5Mjzg9rd3wHvlXEVlxW_VvZTyQ'

channel_id = '@gheymat_lahze_usd'



def get_usd_farda_values():
    """Function to fetch the USD farda buy and sell values from the API."""
    url = 'https://raw.githubusercontent.com/margani/pricedb/main/tgju/current/price_dollar_rl/latest.json'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        usd_farda_buy_value = data['p'].replace(',', '')  # Remove commas and convert to integer
        usd_farda_sell_value = data['h'].replace(',', '')  # Remove commas and convert to integer
        date_time = data['t-g'].replace(',', '')  # Remove commas and convert to integer

        print(data)
        return int(usd_farda_buy_value), int(usd_farda_sell_value), date_time
    else:
        print("Failed to retrieve data from the API. Status code:", response.status_code)
        return None, None

def send_message(token, chat_id, text):
    """Function to send a message via the Telegram bot."""
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    params = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(url, json=params)
    if response.status_code != 200:
        print(f"Failed to send message. Status code: {response.status_code}")
    else:
        print("Message sent successfully!")

if __name__ == "__main__":
    while True:
        usd_farda_buy_value, usd_farda_sell_value, date_time = get_usd_farda_values()
        if usd_farda_buy_value is not None and usd_farda_sell_value is not None and date_time is not None:

            buy_message = f"فردایی تهران ⏳ {usd_farda_buy_value} :خرید 🟢"
            send_message(bot_token, channel_id, buy_message)
            

            sell_message = f"فردایی تهران ⏳ {usd_farda_sell_value} :فروش 🔴, {date_time}"
            send_message(bot_token, channel_id, sell_message)
        
        time.sleep(600)  # 10 دقیقس