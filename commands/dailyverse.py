# import discord, json, sqlite3, requests, re
# from discord.ext import commands
# from bs4 import BeautifulSoup

# intents = discord.Intents.default()
# intents.message_content = True
# client = commands.Bot(command_prefix='!', intents=intents)

# conn = sqlite3.connect('data/user_settings.db')
# c = conn.cursor()

# c.execute('''CREATE TABLE IF NOT EXISTS user_settings
#              (user_id INTEGER PRIMARY KEY, default_translation TEXT)''')

# # Czcionka italic

# def format_verse_text(text):
#     return re.sub(r'\[([^\]]+)\]', r'*\1*', text)

# # Alternatywne nazwy ksiąg

# def get_canonical_book_name(book, books):
#     for canonical_name, aliases in books.items():
#         if book in aliases:
#             return canonical_name
#     return book

# @client.tree.command(name="dailyverse", description="Wyświetla werset dnia z Biblii") 
# async def dailyverse(interaction: discord.Interaction): 
#     await interaction.response.defer()

#     user_id = interaction.user.id
#     c.execute("SELECT * FROM user_settings WHERE user_id = ?", (user_id,))
#     user_data = c.fetchone()

#     if not user_data:
#         embed = discord.Embed(
#             title="Ustaw domyślny przekład Pisma Świętego",
#             description='Aby móc korzystać z funkcji wyszukiwania fragmentów w Biblii, musisz najpierw ustawić domyślny przekład Pisma Świętego za pomocą komendy `/setversion`. Aby ustawić domyślny przekład Pisma Świętego należy podać jego skrót. Wszystkie skróty przekładów są dostępne w `/versions`',
#             color=12370112)
#         await interaction.followup.send(embed=embed, ephemeral=True)
#         return

#     translation = user_data[1]

#     try:
#         with open(f'resources/bibles/{translation}.json', 'r', encoding='utf-8') as file:
#             bible = json.load(file)

#         with open('resources/booknames/english_polish.json', 'r', encoding='utf-8') as file:
#             english_to_polish_books = json.load(file)

#         with open('resources/translations/translations.json', 'r', encoding='utf-8') as file:
#             translations = json.load(file)

#         with open('resources/booknames/books.json', 'r', encoding='utf-8') as file:
#             books = json.load(file)

#         # Pobieranie wersetu dnia ze strony
#         response = requests.get("https://www.verseoftheday.com/")
#         soup = BeautifulSoup(response.text, 'html.parser')
#         reference_div = soup.find("div", class_="reference")
#         link = reference_div.find("a", href=True)
#         verse_reference = link.text.strip()  # np. "John 3:16"

#         # Parsowanie nazwy księgi, rozdziału i wersetu
#         book, chapter_verse = verse_reference.rsplit(" ", 1)
#         chapter, verses = chapter_verse.split(":")
#         chapter = int(chapter)
        
#         verse_range = verses.split("-")
#         start_verse = int(verse_range[0])
#         end_verse = int(verse_range[1]) if len(verse_range) > 1 else start_verse

#         # Tłumaczy nazwę księgi na język polski
#         book_name_polish = english_to_polish_books.get(book, book)

#         # Inne nazwy ksiąg
#         canonical_book_name = get_canonical_book_name(book, books)

#         # Szuka tekstu w pliku JSON
#         text = []
#         for verse in bible:
#             if verse['book_name'] == canonical_book_name and verse['chapter'] == chapter and start_verse <= verse['verse'] <= end_verse:
#                 text.append(f"**({verse['verse']})** {format_verse_text(verse['text'])}")

#         if start_verse == end_verse:
#             title = f"{book_name_polish} {chapter}:{start_verse}"
#         else:
#             title = f"{book_name_polish} {chapter}:{start_verse}-{end_verse}"

#         embed = discord.Embed(
#             title=title,
#             description=" ".join(text),
#             color=12370112
#         )

#         embed.set_footer(text=translations[translation])

#         await interaction.followup.send(embed=embed)

#     except ValueError:
#         error_embed = discord.Embed(
#             title="Błąd",
#             description="Wystąpił błąd podczas przetwarzania danych",
#             color=0xff1d15
#         )
#         await interaction.followup.send(embed=error_embed, ephemeral=True)

tu będą wprowadzane zmiany
