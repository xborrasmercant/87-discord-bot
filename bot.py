import os
from dotenv import load_dotenv
from datetime import datetime
from random import randint
import discord
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

TEST_GUILD = discord.Object(id=788658822633619487)

class BotClient(commands.Bot):
    def __init__(self) -> None:
        # Initialize with a command_prefix, which can be a dummy in case of using only slash commands
        super().__init__(command_prefix="!", intents=discord.Intents.default())

    async def on_ready(self) -> None: # On execution
        systemtime = datetime.now().strftime('%H:%M:%S')
        print("-----------------------------------------")
        print(f"Logged on as {self.user} at {systemtime}")
        print("-----------------------------------------")

client = BotClient()

# MEDALLA
@client.slash_command(name="medalla", description="Selecciona la medalla que deseas pedir", guild_ids=[788658822633619487])
async def medalla(ctx):
    await ctx.respond("Hola que ase")

# DADO
@client.slash_command(name="dado", description="Lanza un dado de x caras", guild_ids=[788658822633619487])
async def dado(ctx, cantidad: discord.Option(int, "Cuantos dados quieres tirar."), caras: discord.Option(int, "Número de caras del dado.")):
    if cantidad <= 100:
        if cantidad > 1:
            dice_results = []
            for i in range(cantidad):
                dice_results.append(str(randint(1, caras)))
            dice_result = ", ".join(dice_results) 
        else:
            dice_result = str(randint(1, caras))
        
        await ctx.respond(dice_result)

    else:
        await ctx.respond("*Por favor, introduce un número menor que 100.*")
    

client.run(TOKEN)
