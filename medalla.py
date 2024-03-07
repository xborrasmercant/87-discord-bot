import discord
from discord.ext import commands
from discord.ui import Select, View
class DropdownView(discord.ui.View):
    def __init__(self, roles):
        super().__init__(timeout=None)  # No timeout for the view
        self.add_item(DropdownSelect(roles))

    
class DropdownSelect(Select):
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