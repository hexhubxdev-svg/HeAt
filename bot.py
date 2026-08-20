import discord
from discord.ext import commands
import re
import os

TOKEN = "ddef08b7b5e10142673bdb9467fef74055ddc718459781363589a98f36420f4a"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is ready as {bot.user}")

@bot.command()
async def decode(ctx):
    await ctx.send("Send your Lua code as a text message or upload a .lua file.")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    if message.attachments:
        for attachment in message.attachments:
            if attachment.filename.endswith(".lua") or attachment.filename.endswith(".txt"):
                try:
                    content = await attachment.read()
                    code = content.decode('utf-8', errors='ignore')
                    decoded = decode_lua(code)
                    if decoded:
                        filename = f"decoded_{attachment.filename}"
                        with open(filename, "w", encoding="utf-8") as f:
                            f.write(decoded)
                        await message.channel.send(file=discord.File(filename))
                        os.remove(filename)
                    else:
                        await message.channel.send("Failed to decode.")
                except Exception as e:
                    await message.channel.send(f"Error: {e}")
        return
    
    if message.content and not message.content.startswith("!"):
        code = message.content
        decoded = decode_lua(code)
        if decoded:
            if len(decoded) > 2000:
                filename = "decoded.lua"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(decoded)
                await message.channel.send(file=discord.File(filename))
                os.remove(filename)
            else:
                await message.channel.send(f"```lua\n{decoded}\n```")
        return
    
    await bot.process_commands(message)

def decode_lua(code):
    try:
        decoded = code
        decoded = re.sub(r'string\.char\(([\d\s,]+)\)', lambda m: '"' + ''.join(chr(int(n)) for n in m.group(1).split(',')) + '"', decoded)
        decoded = re.sub(r'\\(\d\d\d)', lambda m: chr(int(m.group(1))), decoded)
        return decoded
    except:
        return None

bot.run(TOKEN)
