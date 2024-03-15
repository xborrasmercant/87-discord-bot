import os

from discord import File
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


bot = BotClient()


# SHOW AWARDS
@bot.slash_command(name="stats",
                   description="Muestra tus condecoraciones ademas de la cantidad puntos condecorativos.",
                   guild_ids=[GUILD_ID])
async def get_awards(ctx):
    point_amount = 0
    member = ctx.guild.get_member(ctx.author.id)
    pfp = member.avatar.url if member.avatar else ctx.author.default_avatar.url

    awards = [role for role in member.roles if await role_is_award(role)]
    awards_dict = await get_award_dict(awards)

    embed = discord.Embed(
        title=f"🎖️ __Condecoraciones de {member.display_name}__ 🎖️",
        description=f"A continuación puedes ver la condecoraciones de {member.display_name}.",
        color=member.color
    )

    for award_type in awards_dict.__reversed__():
        award_type_value = ""
        for award in awards_dict[award_type]:
            point_amount = await sum_award_points(award, point_amount)
            award_type_value += f"{award} - ({await get_award_points(award)} pts)\n"

        embed.add_field(name=award_type.upper(), value=award_type_value, inline=False)
        embed.add_field(name=" ", value="", inline=False)

    embed.add_field(name=" ", value="", inline=False)
    embed.add_field(name="", value=f"La cantidad de puntos condecorativos totales es de **{point_amount}**",
                    inline=False)

    embed.set_author(name="Departamento de Condecoraciones",
                     icon_url="https://yt3.googleusercontent.com/ytc/AIdro_nnYadq0WqvS4Q5EMvjdbRvE5RqT-oRAUPV6GcS=s900-c-k-c0x00ffffff-no-rj")
    embed.set_thumbnail(url=pfp)
    embed.set_image(url="https://i.ytimg.com/vi/Kf1Y6pZPFyA/maxresdefault.jpg")

    await ctx.respond(embed=embed)


# FRANCO FRIDAY
@bot.slash_command(name="franco", description="franco friday", guild_ids=[GUILD_ID])
async def franco_friday(ctx):
    franco_friday_file = File("resources/vid/franco_friday.mp4")

    await ctx.send("## ¡Atención, el Franco Friday ha comenzado! \n"
                   f"¡Muestra tus respetos como es debido! Responde a este mensaje con <:chispy:1218281005971013692>",
                   file=franco_friday_file)


# TIMESTAMP
@bot.slash_command(name="timestamp", description="Introduce una hora (HH:MM)", guild_ids=[GUILD_ID])
async def timestamp(ctx,
                    hora: discord.Option(str, "Tu hora local en formato HH:MM"),
                    zona_horaria: discord.Option(str, "Tu zona horaria, por ejemplo Europe/Madrid")):
    # TODO: CONTINUE METHOD
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
@bot.slash_command(name="condecoración", description="Selecciona la condecoración que deseas pedir",
                   guild_ids=[GUILD_ID])
async def request_award(ctx):
    guild = bot.get_guild(GUILD_ID)
    roles = [role for role in guild.roles if await role_is_award(role)]
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


async def role_is_award(role):
    if (role.name.startswith("🎇")
            or role.name.startswith("🥇")
            or role.name.startswith("🥈")
            or role.name.startswith("🥉")
            or role.name.startswith("⚓")
            or role.name.startswith("🔰")):
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


async def get_award_points(award):
    if award.name.startswith("🎇"):
        return 100
    elif award.name.startswith("🥇"):
        return 50
    elif award.name.startswith("🥈"):
        return 25
    elif award.name.startswith("🥉"):
        return 10
    elif award.name.startswith("⚓"):
        return 15
    elif award.name.startswith("🔰"):
        return 5


async def get_award_dict(awards):
    awards_dict = {}
    for award in awards:
        if award.name.startswith("🎇"):
            if "Cruces" in awards_dict:
                awards_dict["Cruces"].append(award)
            else:
                awards_dict["Cruces"] = [award]
        elif award.name.startswith("🥇"):
            if "Medallas" in awards_dict:
                awards_dict["Medallas"].append(award)
            else:
                awards_dict["Medallas"] = [award]
        elif award.name.startswith("🥈"):
            if "Bandas" in awards_dict:
                awards_dict["Bandas"].append(award)
            else:
                awards_dict["Bandas"] = [award]
        elif award.name.startswith("🥉"):
            if "Menciones" in awards_dict:
                awards_dict["Menciones"].append(award)
            else:
                awards_dict["Menciones"] = [award]
        elif award.name.startswith("⚓"):
            if "Condecoraciones Navales" in awards_dict:
                awards_dict["Condecoraciones Navales"].append(award)
            else:
                awards_dict["Condecoraciones Navales"] = [award]
        elif award.name.startswith("🔰"):
            if "Reconocimientos" in awards_dict:
                awards_dict["Reconocimientos"].append(award)
            else:
                awards_dict["Reconocimientos"] = [award]
    return awards_dict


async def sum_award_points(award, point_amount):
    if award.name.startswith("🎇"):
        point_amount += 100
    elif award.name.startswith("🥇"):
        point_amount += 50
    elif award.name.startswith("🥈"):
        point_amount += 25
    elif award.name.startswith("🥉"):
        point_amount += 10
    elif award.name.startswith("⚓"):
        point_amount += 15
    elif award.name.startswith("🔰"):
        point_amount += 5

    return point_amount


bot.run(TOKEN)
