import discord
from discord import guild
from discord.ext import commands
from discord.ui import Select, View


class AwardsDropdown(discord.ui.View):
    def __init__(self, roles):
        super().__init__(timeout=None)  # No timeout for the view
        self.add_item(AwardsSelect(roles))


class AwardsSelect(Select):
    def __init__(self, roles):
        options = [discord.SelectOption(label=role.name, value=str(role.id)) for role in roles]
        super().__init__(placeholder="Escoge una medalla:",
                         min_values=1,
                         max_values=1,
                         options=options)

    async def callback(self, interaction: discord.Interaction):
        # Handle what happens after a user selects an option
        role_id = int(self.values[0])  # Get the selected role ID
        role = interaction.guild.get_role(role_id)
        if role:
            await interaction.response.send_message(f"You selected the role: {role.name}", ephemeral=True)
        else:
            await interaction.response.send_message("Role not found.", ephemeral=True)


class RanksDropdown(discord.ui.View):
    def __init__(self, guild):
        super().__init__(timeout=None)  # No timeout for the view
        self.guild = guild
        self.add_item(RanksSelect(guild))


class RanksSelect(Select):
    def __init__(self, guild):
        self.guild = guild
        self.ranks = ["Enlistado", "Recluta", "Soldado Regular", "Soldado Veterano",
                      "Tropa de Élite", "Cuerpo de Granaderos", "Guardia Valona",
                      "Guardia Real", "Cabo", "Sargento", "Alférez", "Teniente",
                      "Capitán", "Coronel", "General", "Mariscal"]
        super().__init__(placeholder="Escoge un rango...",
                         min_values=1,
                         max_values=1,
                         options=[discord.SelectOption(label=rank, value=rank) for rank in self.ranks])

    async def callback(self, interaction: discord.Interaction):
        selected_rank = self.values[0]
        members_list_str = ""

        embed = discord.Embed(
            title=f"__{selected_rank.upper()}__",
            description=f"Actualmente hay {get_rank_count(selected_rank, self.guild)} miembros con el rango {selected_rank}.",
            color=discord.Color.blue()
        )

        for member in self.guild.members:
            for role in member.roles:
                if role.name == selected_rank:
                    members_list_str += f"- {member.display_name}\n"

        embed.add_field(name="", value=members_list_str, inline=False)
        embed.set_thumbnail(url="")
        embed.set_image(url="")

        await interaction.response.send_message(embed=embed)


def get_rank_count(rank, guild):
    rank_role = discord.utils.get(guild.roles, name=rank)

    if not rank_role:
        return 0

    role_count = sum(rank_role in member.roles for member in guild.members)

    return role_count
