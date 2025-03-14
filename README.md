# Biblia Bot - bot w trakcie rozbudowy

## O bocie: 

**Biblia** to bot, który daje możliwość czytania Pisma Świętego w różnych językach, co pozwala na dokładne porównywanie tekstów oryginalnych z ich tłumaczeniami. Bot zawiera przekłady Pisma Świętego w języku **polskim, angielskim, niemieckim, łacińskim, greckim i hebrajskim**

## Instalacja pakietów:

* Wpisz w terminalu następujące komendy:

``` python
pip install discord.py
```

``` python
pip install asyncio
```

``` python
pip install pysqlite3
```

``` python
pip install python-dotenv
```

``` python
pip install beautifulsoup4
```

``` python
pip install requests
```

## Utwórz plik .env z taką strukturą:

``` python
TOKEN='tu wklej token bota'
```
## Wklej swój link z zaproszeniem:

Link z zaproszeniem należy utworzyć w **Discord Developer Portal**
1. Wejdź w aplikację bota
2. Kliknij w zakładkę **OAuth2**
3. W **SCOPES** zaznacz `bot` i `applications.commands`
4. W **BOT PERMISSIONS** zaznacz następujące uprawnienia:
* View Channels
* Send Messages
* Send Messages in Threads
* Use Slash Commands
* Manage Messages
* Embed Links

``` python
self.add_item(discord.ui.Button(label="Dodaj bota", url="twój_link_z_zaproszeniem"))
```

## Baza danych

W folderze `data` zostanie utworzona baza danych w pliku `user_settings.db` gdy pierwszy użytkownik ustawi domyślny przekład Pisma Świętego

## Uruchomienie bota:

* Wpisz w terminalu następującą komendę:

``` python
python main.py
```
