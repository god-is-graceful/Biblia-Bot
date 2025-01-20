import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

class InviteView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(label="Dodaj bota", url="https://discord.com/oauth2/authorize?client_id=1090620310090420275&permissions=277025459200&scope=bot+applications.commands"))

@client.tree.command(name="invite", description="Dodaj bota na swój serwer")
async def invite(interaction: discord.Interaction):
    view = InviteView()
    await interaction.response.send_message(view=view)