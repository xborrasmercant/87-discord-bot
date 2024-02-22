import discord
from discord import *
from discord.ui import *
from datetime import *

TEST_GUILD = discord.Object(788658822633619487)


class BotClient(discord.Client):

    def __init__(self, intents) -> None:
        super().__init__(intents = intents)
        self.tree = app_commands.CommandTree(self) # Create slash commands tree
        


    async def on_ready(self) -> None: # On execution
        systemtime = datetime.now().strftime('%H:%M:%S')

        print(f"Logged on as {self.user} at {systemtime}")
        print("-----------------------------------------")
        

    async def setup_hook(self) -> None:
        # Sync commands with Discord
        await self.tree.sync(guild=TEST_GUILD)