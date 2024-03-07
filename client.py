import discord
from discord import *
from discord.ext import commands
from discord.commands import Option
from datetime import *

TEST_GUILD = discord.Object(id=788658822633619487)


class BotClient(discord.Client):

    def __init__(self, intents) -> None:
        super().__init__(intents = intents)
        

    async def on_ready(self) -> None: # On execution
        systemtime = datetime.now().strftime('%H:%M:%S')
        print("-----------------------------------------")
        print(f"Logged on as {self.user} at {systemtime}")
        print("-----------------------------------------")
        

    @bot.slash_command(name="medalla", description="Selecciona la medalla que deseas pedir")
    async def ping(ctx):
        await ctx.respond("Hola que ase")