import os
from dotenv import load_dotenv
from datetime import datetime
from random import randint
from medalla import DropdownView
import discord
from discord.ext import commands
import pytz

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = 788658822633619487


class BotClient(commands.Bot):
    def __init__(self) -> None:
        self.last_mention = None
        self.mention_counter = None
        intents = discord.Intents.all()

        super().__init__(command_prefix="!", intents=intents)

    async def on_ready(self) -> None:  # On execution
        systemtime = datetime.now().strftime('%H:%M:%S')
        print("-----------------------------------------")
        print(f"Logged in as {self.user} at {systemtime}")
        print("-----------------------------------------")

    # INCOMING MESSAGES
    async def on_message(self, message):
        if message.author.bot:
            return

        # Handle mentions
        if message.mentions:
            await mention_user_control(self, message)
        elif message.role_mentions:
            await mention_role_control(self, message)
        else:
            await message.reply(f"Received {message.content}", mention_author=True)


bot = BotClient()


# TIMESTAMP
@bot.slash_command(name="timestamp", description="Introduce una hora (HH:MM)", guild_ids=[GUILD_ID])
async def timestamp(ctx,
                    hora: discord.Option(str, "Tu hora local en formato HH:MM"),
                    zona_horaria: discord.Option(str, "Tu zona horaria, por ejemplo Europe/Madrid")):
    """Converts a time in HH:MM format to a Discord timestamp for the current date."""
    try:
        today = datetime.today()
        datetime_str = f"{today.strftime('%Y-%m-%d')} {hora}"
        local_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        local_timezone = pytz.timezone(zona_horaria)
        local_datetime = local_timezone.localize(local_datetime)
        utc_datetime = local_datetime.astimezone(pytz.utc)

        timestamp = int(utc_datetime.timestamp())

        # Respond with the timestamp formatted to include hours
        await ctx.send(f"The timestamp for today at {hora} UTC is <t:{timestamp}:t>.")
    except ValueError:
        # The time was not in the expected format
        await ctx.send("Please enter the time in HH:MM format.")


# CONDECORACIONES
@bot.slash_command(name="condecoración", description="Selecciona la condecoración que deseas pedir", guild_ids=[GUILD_ID])
async def request_award(ctx):
    guild = bot.get_guild(GUILD_ID)
    roles = [role for role in guild.roles if role_is_award(role)]
    view = DropdownView(roles)
    await ctx.respond("Select a role:", view=view, ephemeral=True)


# DADO
@bot.slash_command(name="dado", description="Lanza un dado de x caras", guild_ids=[GUILD_ID])
async def throw_dice(ctx,
                     cantidad: discord.Option(int, "La cantidad de dados a tirar."),
                     caras: discord.Option(int, "Número de caras del dado.")):  # type: ignore
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
        await ctx.respond("*Por favor, introduce un número menor que 100.")


def role_is_award(role):
    if role.name.startswith("💠") or role.name.startswith("🔰") or role.name.startswith("🟡"):
        return True
    else:
        return False


async def mention_user_control(self, message):
    if self.last_mention == message.mentions:
        self.mention_counter = self.mention_counter + 1
    else:
        self.mention_counter = 0
    self.last_mention = message.mentions

    if self.mention_counter > 4:
        await message.reply("Relaja las tetas", mention_author=True)
        # TODO: grant timeout method to message author


async def mention_role_control(self, message):
    if self.last_mention == message.role_mentions:
        self.mention_counter = self.mention_counter + 1
    else:
        self.mention_counter = 0
    self.last_mention = message.role_mentions

    if self.mention_counter > 4:
        self.mention_counter = 0
        await message.reply("Relaja las tetas", mention_author=True)
        # TODO: grant timeout method to message author


bot.run(TOKEN)
