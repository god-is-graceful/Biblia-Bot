import discord, json, sqlite3, re
from discord import app_commands
from typing import List
from collections import deque
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

class PaginatorView(discord.ui.View):
    def __init__(
        self, 
        embeds:List[discord.Embed]
    ) -> None:
        super().__init__(timeout=None)
        self._embeds = embeds
        self._queue = deque(embeds)
        self._initial = embeds[0]
        self._current_page = 1
        self._len = len(embeds)

        if self._len == 1:
            self.previous_page.disabled = True
            self.next_page.disabled = True

    def get_page_number(self) -> str:
        return f"Strona {self._current_page} z {self._len}"

    @discord.ui.button(style=discord.ButtonStyle.secondary, emoji="⬅️")
    async def previous_page(self, interaction: discord.Interaction, _):
        self._queue.rotate(1)
        embed = self._queue[0]
        if self._current_page > 1:
            self._current_page -= 1
        else:
            self._current_page = self._len
        embed.set_footer(text=self.get_page_number())
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(style=discord.ButtonStyle.secondary, emoji="➡️")
    async def next_page(self, interaction: discord.Interaction, _):
        self._queue.rotate(-1)
        if self._current_page < self._len:
            self._current_page += 1
        else:
            self._current_page = 1
        embed = self._queue[0]
        embed.set_footer(text=self.get_page_number())
        await interaction.response.edit_message(embed=embed)

    @property
    def initial(self) -> discord.Embed:
        embed = self._initial
        embed.set_footer(text=self.get_page_number())
        return embed

conn = sqlite3.connect('data/user_settings.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS user_settings
             (user_id INTEGER PRIMARY KEY, default_translation TEXT)''')

# Czcionka italic

def format_verse_text(text):
    return re.sub(r'\[([^\]]+)\]', r'*\1*', text)

# Autouzupełnianie opcji w komendzie /search

async def translation_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> list[app_commands.Choice[str]]:
    with open('resources/translations/bible_translations.txt', 'r') as file:
        bible_translations = [line.strip() for line in file]
    return [
        app_commands.Choice(name=translation, value=translation)
        for translation in bible_translations
        if current.lower() in translation.lower()
    ][:25]

@client.tree.command(name="search", description="Wyszukiwanie fragmentów w Biblii")
@app_commands.describe(text="Wpisz słowo lub frazę", translation="Wybierz przekład Pisma Świętego")
@app_commands.autocomplete(translation=translation_autocomplete)
async def search(interaction: discord.Interaction, text: str, translation: str = None):

    await interaction.response.defer()

    user_id = interaction.user.id
    c.execute("SELECT * FROM user_settings WHERE user_id = ?", (user_id,))
    user_data = c.fetchone()

    if translation:
        translation = translation
    elif user_data:
        translation = user_data[1]
    else:
        embed = discord.Embed(
            title="Ustaw domyślny przekład Pisma Świętego",
            description='Aby móc korzystać z funkcji wyszukiwania fragmentów w Biblii, musisz najpierw ustawić domyślny przekład Pisma Świętego za pomocą komendy `/setversion`. Aby ustawić domyślny przekład Pisma Świętego należy podać jego skrót. Wszystkie skróty przekładów są dostępne w `/versions`',
            color=12370112)
        await interaction.followup.send(embed=embed)
        return
    
    with open('resources/translations/translations.json', 'r', encoding='utf-8') as file:
        translations = json.load(file)

    if translation not in translations:
        error_embed = discord.Embed(
            title="Błąd",
            description=f"Podano błędny skrót przekładu Pisma Świętego. Sprawdź dostępne przekłady w `/versions`",
            color=0xff1d15)
        await interaction.followup.send(embed=error_embed)
        return

    with open('resources/booknames/english_polish.json', 'r', encoding='utf-8') as file:
        polish_booknames = json.load(file)

    try:
        with open(f'resources/bibles/{translation}.json', 'r', encoding='utf-8') as file:
            bible = json.load(file)
    except FileNotFoundError:
        error_embed = discord.Embed(
            title="Błąd",
            description=f"Nie znaleziono wersetu",
            color=0xff1d15)
        await interaction.followup.send(embed=error_embed)
        return

    embeds = []

    try:
        words = text.split()
        verses = []

        for verse in bible:
            if all(word in verse['text'] for word in words):
                for word in words:
                    verse['text'] = verse['text'].replace(word, f'**{word}**')
                italics_font = format_verse_text(verse['text'])
                verses.append(f"**{polish_booknames[verse['book_name']]} {verse['chapter']}:{verse['verse']}** \n{italics_font} \n")
        if not verses:
            raise ValueError(f'Nie znaleziono żadnego wersetu zawierającego słowo lub frazę "**{text}**" w przekładzie `{translations[translation]}`')
        
    except ValueError as err:
        error_embed = discord.Embed(
            title="Błąd wyszukiwania",
            description=str(err),
            color=0xff1d15)
        await interaction.followup.send(embed=error_embed)
        return

    message = ''

    for verse in verses:
        if len(message) + len(verse) < 650:
            message += f"{verse}\n"
        else:
            embed = discord.Embed(
                title=f'Fragmenty z Biblii zawierające słowo lub frazę - *{text}*',
                description=f"{message}**{translations[translation]}**",
                color=12370112
            )
            embeds.append(embed)
            message = f"{verse}\n"

    if message:
        embed = discord.Embed(
            title=f'Fragmenty z Biblii zawierające słowo lub frazę - *{text}*',
            description=f"{message}**{translations[translation]}**",
            color=12370112
        )
        embeds.append(embed)

    view = PaginatorView(embeds)
    await interaction.followup.send(embed=view.initial, view=view)