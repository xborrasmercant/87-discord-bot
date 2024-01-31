import discord
from discord import *
from discord.ui import *
from datetime import *



class MedalDropdown(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label='🥈Banda Borgoña', description='Concedida al soldado que obtenga 3 bajas.'),
            discord.SelectOption(label='🥉Mención de Riego', description='Concedida al soldado de infantería que logre 3.'),
        ]
        super().__init__(placeholder='Selecciona una medalla', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):


        selectedMedal = self.values[0]
        currentDate = datetime.now().strftime("%d/%m/%Y")
        medalProof = "Reporte"

        embed = discord.Embed(title="Medalla Recibida", color=0x00ff00)  # You can change the color
        embed.add_field(name="**Medalla**", value=selectedMedal, inline=False)
        embed.add_field(name="**Fecha**", value=currentDate, inline=False)
        embed.add_field(name="**Pruebas**", value=medalProof, inline=False)

        await interaction.response.send_message(embed=embed)