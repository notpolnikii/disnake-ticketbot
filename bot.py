import disnake
from disnake.ext import commands

import os
from config import TOKEN

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix="!",
                   intents=intents,
                   help_command=None)

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")

for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")

bot.run(TOKEN)