import os
import discord
import requests
from dotenv import load_dotenv

# token .env information
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')  # replace with your API key

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!stock'):
        stock_symbol = message.content.split()[1]

        # Build the API request URL
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock_symbol}&apikey={ALPHA_VANTAGE_API_KEY}'

        # Make the API request and get the JSON response
        response = requests.get(url)
        stock_data = response.json()

        if 'Global Quote' in stock_data:
            stock_info = stock_data['Global Quote']
            price = stock_info['05. price']
            change = stock_info['09. change']
            change_percent = stock_info['10. change percent']

            response_message = f'**{stock_symbol.upper()}**: Price: {price}, Change: {change}, Change Percent: {change_percent}'
        else:
            response_message = f'Stock symbol {stock_symbol.upper()} not found.'

        await message.channel.send(response_message)

client.run(BOT_TOKEN)
