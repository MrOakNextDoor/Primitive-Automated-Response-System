
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
    cursor.execute("""CREATE TABLE censorlist
        (usr_id integer);
    """)

    conn.commit()
except sqlite3.OperationalError:
    pass

#   The actual discord bot
client = commands.Bot(command_prefix='cp! ')

@client.event
async def on_ready():
    print(f'Comrade Pears logged in as {client.user}.')

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    #   Check if the sender is part of the censorlist
    cursor.execute('SELECT * FROM censorlist WHERE usr_id == ?', [message.author.id])
    if not cursor.fetchall() == []:
        await message.channel.send(
            f'You may not speak, <@{message.author.id}>.')
        return

    #   Then process all commands
    await client.process_commands(message)

@client.command()
async def ping(ctx):
    await ctx.send(f'My ping is {round(client.latency * 1000, 1)} ms!')

@client.command()
async def clear(ctx, num: int=5):
    await ctx.channel.purge(limit=num+1)

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason: str=None):
    await member.kick(reason=reason)

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason: str=None):
    await member.ban(reason=reason)

@kick.error
async def kick_error(error, ctx):
    if isinstance(error, commands.MissingPermissions):
       await ctx.send(f'You don\'t have permission to do that, <@{ctx.author.id}>.')

@ban.error
async def ban_error(error, ctx):
    if isinstance(error, commands.MissingPermissions):
       await ctx.send(f'You don\'t have permission to do that, <@{ctx.author.id}>.')

if __name__ == '__main__':
    #   Run the bot
    client.run(os.getenv('TOKEN'))
