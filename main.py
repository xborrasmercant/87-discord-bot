import os
import discord
from discord import Client, Intents
from typing import Final
from dotenv import load_dotenv
from client import BotClient


# 1. TOKEN LOAD
load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")

#2. BOT SETUP
intents: Intents = discord.Intents.all()
intents.message_content = True

client: Client = BotClient(intents = intents)
client.run(TOKEN)