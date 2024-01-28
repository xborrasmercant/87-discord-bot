import discord
from discord import *
from datetime import *


class BotClient(discord.Client):

    def __init__(self, intents):
        super().__init__(intents = intents)
        self.commandsList: list = ["!hola"]


    def isValidCommand(self, command: str) -> bool:

        for i in range(0, len(self.commandsList)): 
            if self.commandsList[i] == command:
                return True
        return False


    async def on_message(self, message): # Message recieved
        #print(f"Message from {message.author}: {message.content}")
        #print(f"Is ({message.content}) a valid command? {self.isValidCommand(message.content)} ")

        if message.author == self.user: # Ignore bot messages
            return
        else:
            if message.content in self.commandsList:
                if message.content == "!hola":
                    await message.channel.send(f"Hola {message.author}, encantado de servirte! Mi nombre es {self.user}!")
                elif message.content == "!adios":
                    await message.channel.send(f"Adiós {message.author}, hasta otra!")
                else:
                      pass
                

            
    async def on_ready(self): # On execution
        systemtime = datetime.now().strftime('%H:%M:%S')

        print(f"Logged on as {self.user} at {systemtime}")