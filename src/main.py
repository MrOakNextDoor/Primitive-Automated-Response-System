
#   Libraries
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

#   Code
client = commands.Bot(command_prefix='cp!')

load_dotenv(os.path.join(os.getcwd(), 'data', '.env'))

@client.event
async def on_ready():
    print(f'Comrade Pears logged in as {client.user}.')

if __name__ == '__main__':
    client.run(os.getenv('TOKEN'))
