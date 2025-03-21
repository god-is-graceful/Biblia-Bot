import discord
from discord.ext import commands
from typing import List
from collections import deque

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

class PaginatorView(discord.ui.View):
    def __init__(self, embeds: List[discord.Embed]) -> None:
        super().__init__(timeout=None)
        self.embeds = deque(embeds)
        self.current_page = 1
        self.total_pages = len(embeds)

        if self.total_pages == 1:
            self.previous_page.disabled = True
            self.next_page.disabled = True

    def update_footer(self) -> discord.Embed:
        embed = self.embeds[0]
        embed.set_footer(text=f"Strona {self.current_page} z {self.total_pages}")
        return embed

    async def change_page(self, interaction: discord.Interaction, direction: int):
        self.embeds.rotate(direction)
        self.current_page = (self.current_page - direction - 1) % self.total_pages + 1
        await interaction.response.edit_message(embed=self.update_footer())

    @discord.ui.button(style=discord.ButtonStyle.secondary, emoji="⬅️")
    async def previous_page(self, interaction: discord.Interaction, _):
        await self.change_page(interaction, 1)

    @discord.ui.button(style=discord.ButtonStyle.secondary, emoji="➡️")
    async def next_page(self, interaction: discord.Interaction, _):
        await self.change_page(interaction, -1)

    @property
    def initial(self) -> discord.Embed:
        return self.update_footer()

@client.tree.command(name="versions", description="Dostępne przekłady Pisma Świętego")
async def versions(interaction: discord.Interaction):
    description = [
        f'Oto dostępne przekłady Biblii: \n\n**Polskie:**\n\n`BB` - Biblia Brzeska (1563)\n`BN` - Biblia Nieświeska (1574)\n`BJW` - Biblia Jakuba Wujka (1599)\n`BG` - Biblia Gdańska (1881)\n`BS` - Biblia Szwedzka (1948)\n`BM` - Biblia Mesjańska (1975)\n`BP` - Biblia Poznańska (1975)\n`BW` - Biblia Warszawska (1975)\n`SZ` - Słowo Życia (1989)\n`BL` - Biblia Lubelska (1991)',
        f'Oto dostępne przekłady Biblii: \n\n`BWP` - Biblia Warszawsko-Praska (1997)\n`PNS` - Przekład Nowego Świata (1997)\n`BT` - Biblia Tysiąclecia: wydanie V (1999)\n`SNPD` - Słowo Nowego Przymierza: przekład dosłowny (2004)\n`GOR` - Biblia Góralska (2005)\n`NBG` - Nowa Biblia Gdańska (2012)\n`PAU` - Biblia Paulistów (2016)\n`UBG` - Uwspółcześniona Biblia Gdańska (2017)\n`BE` - Biblia Ekumeniczna (2018)\n`SNP` - Słowo Nowego Przymierza: przekład literacki (2018)\n`TNP` - Przekład Toruński Nowego Przymierza (2020)\n`TRO` - Textus Receptus Oblubienicy (2023)',
        f'Oto dostępne przekłady Biblii: \n\n**Angielskie:**\n\n`KJV` - King James Version (1769)\n`ASV` - American Standard Version (1901)\n`NKJV` - New King James Version (1982)\n`UKJV` - Updated King James Version (2000)\n`WEB` - World English Bible (2006)\n\n**Niemieckie:**\n\n`LUTH` - Luther Bibel (1545)\n`SCH` - Schlachter Bibel (1951)',
        f'Oto dostępne przekłady Biblii: \n\n**Łacińskie:**\n\n`VG` - Wulgata\n\n**Greckie:**\n\n`LXX` - Septuaginta\n`LXXs` - Septuaginta: system Stronga\n`TR` - Textus Receptus (1550)\n`TRs` - Textus Receptus (1550): system Stronga\n`NE` - Nestle (1904)\n`NEs` - Nestle (1904): system Stronga',
        f'Oto dostępne przekłady Biblii: \n\n`BYZ` - Tekst Bizantyjski (2013)\n\n**Hebrajskie:**\n\n`ALEP` - Aleppo Codex\n`WLC` - Westminster Leningrad Codex'
    ]
    embeds = [discord.Embed(title="Dostępne przekłady Biblii", description=desc, color=12370112) for desc in description]
    view = PaginatorView(embeds)
    await interaction.response.send_message(embed=view.initial, view=view)
