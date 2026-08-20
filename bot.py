import os
import discord
from discord.ext import commands

TOKEN = os.environ.get("ddef08b7b5e10142673bdb9467fef74055ddc718459781363589a98f36420f4a")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot Working {bot.user}')

@bot.command()
async def help(ctx):
    await ctx.send("""
    Hi
    /help
    /Start
""")

@bot.command()
async def start(ctx):
    await ctx.send("What")

bot.run(TOKEN)
