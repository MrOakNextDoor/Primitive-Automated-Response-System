
#   Libraries
import os
import sqlite3

import discord
from discord.ext import commands
from dotenv import load_dotenv

#   Code
load_dotenv(os.path.join(os.getcwd(), 'data', '.env'))

#   Database
conn = sqlite3.connect(os.path.join('data', 'data.db'))
cursor = conn.cursor()

#   Initialize the database if possible
try:
    cursor.execute()
except sqlite3.OperationalError:
    pass

#   The actual discord bot
client = commands.Bot(command_prefix='cp! ')

@client.event
async def on_ready():
    print(f'Comrade Pears logged in as {client.user}.')

@client.event
async def on_message(message):

    await client.process_commands(message)

    if message.author == client.user:
        return

@client.command()
async def ping(ctx):
    await ctx.send(f'My ping is {round(client.latency * 1000, 1)} ms!')

@client.command()
async def clear(ctx, num=5):
    await ctx.channel.purge(limit=num+1)

if __name__ == '__main__':
    #   Run the bot
    client.run(os.getenv('TOKEN'))
