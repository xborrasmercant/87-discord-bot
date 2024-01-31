import discord
from discord import *
from discord.ui import *
from datetime import *
from medallasDropdown import *


class BotClient(discord.Client):

    def __init__(self, intents):
        super().__init__(intents = intents)
        self.commandsList: list = ["!medalla", "!trivial"]

    async def on_message(self, message): # Message recieved
        #print(f"Message from {message.author}: {message.content}")

        if message.author == self.user: # Ignore bot messages
            return
        else:
            if message.content in self.commandsList:
                if message.content == "!medalla":
                    await self.commandMedal(message)
                elif message.content == "!trivial":
                    await self.commandTrivial(message)
                else:
                    pass     
                    

    # COMMANDS FUNCTIONS

    async def commandMedal(self, message) -> None:
        await self.addMedalDropdown(message)
    
    async def commandTrivial(self, message) -> None:
        await message.channel.send(f"Comando para jugar trivial (WIP)")


        
    # OTHER FUNCTIONS

    async def addMedalDropdown(self, message) -> None:
        view = View()
        view.add_item(MedalDropdown())
        await message.channel.send('Select an option:', view=view)


    async def on_ready(self): # On execution
        systemtime = datetime.now().strftime('%H:%M:%S')

        print(f"Logged on as {self.user} at {systemtime}")
        

