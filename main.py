import os
import discord
from discord import *
from typing import *
from dotenv import *
from botclient import *


# 1. TOKEN LOAD
load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")

#2. BOT SETUP
intents: Intents = discord.Intents.default()
intents.message_content = True

client: Client = BotClient(intents = intents)
client.run(TOKEN)