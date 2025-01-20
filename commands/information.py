import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

@client.tree.command(name="information", description="Informacje o bocie")
async def information(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Informacje",
        description="**Biblia** to bot, który daje możliwość czytania Pisma Świętego w różnych językach, co pozwala na dokładne porównywanie tekstów oryginalnych z ich tłumaczeniami\n\nBot zawiera przekłady Pisma Świętego w **6** językach: **polskim**, **angielskim**, **niemieckim**, **łacińskim**, **greckim** i **hebrajskim**\n\n**Strona internetowa:** https://biblia-bot.netlify.app/\n\n[Terms of Service](https://biblia-bot.netlify.app/terms-of-service) | [Privacy Policy](https://biblia-bot.netlify.app/privacy-policy)",
        color=12370112)
    await interaction.response.send_message(embed=embed)