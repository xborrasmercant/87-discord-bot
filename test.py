import discord
from discord.ext import commands
from discord.ui import Select, View

bot = commands.Bot(command_prefix='!')

class RoleSelectMenu(Select):
    def __init__(self, roles):
        options = [discord.SelectOption(label=role.name, value=str(role.id)) for role in roles]
        super().__init__(placeholder="Choose a role...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        # Handle what happens after a user selects an option
        role_id = int(self.values[0])  # Get the selected role ID
        role = interaction.guild.get_role(role_id)
        if role:
            await interaction.response.send_message(f"You selected the role: {role.name}", ephemeral=True)
        else:
            await interaction.response.send_message("Role not found.", ephemeral=True)

class RoleSelectView(View):
    def __init__(self, roles):
        super().__init__(timeout=None)  # No timeout for the view
        # Add the role select menu to the view
        self.add_item(RoleSelectMenu(roles))

@bot.slash_command(guild_ids=[788658822633619487], description="Select a role")
async def select_role(ctx):
    guild = bot.get_guild(788658822633619487)
    roles = [role for role in guild.roles if roleIsAward(role)]
    view = RoleSelectView(roles)
    await ctx.respond("Select a role:", view=view, ephemeral=True)  # Use ephemeral=True if you want the message to be visible only to the user


def roleIsAward(role):
    if role.name.startswith("💠") or role.name.startswith("🔰") or role.name.startswith("🟡"):
        return True
    else :
        return False
    
bot.run('MTIwMDU5OTIyMTgyMTI1MTYzNA.GNwZuZ.AOO5nZcIRXcs8rtyi6bTzJq7e_4bDOY3KyvVMM')