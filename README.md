# OTP Winners Bot

Ez a projekt egy Discord bot, amely ellenőrzi az OTP Gépkocsinyeremény betétszámla nyerőszámait, és értesítést küld a Discord csatornára, ha a megadott számok nyertek.

## Telepítés és futtatás

### Előfeltételek

- Python 3.6 vagy újabb verzió telepítve a rendszereden.
- Egy Discord bot token és egy Discord csatorna ID.

### Lépések

1. **Repository klónozása:**

   ```
   git clone https://github.com/norbertjoni/otp-vehicle-winners-bot.git
   cd otp-vehicle-winners-bot
2. **Környezet beállítása:**

    Hozz létre egy szelvenyek.txt fájlt a projekt gyökérkönyvtárában a következő tartalommal:
    ```
    DISCORD_BOT_TOKEN=your_discord_bot_token
    DISCORD_CHANNEL_ID=your_discord_channel_id
    SZELVENYSZAMOK=your_numbers_comma_separated
3. **Szükséges csomagok telepítése:**

    ```
    pip install -r requirements.txt
4. **Bot futtatása:**

    ```
    python bot.py
5. **Crontab beállítása (opcionális)**
    Ha szeretnéd, hogy a bot rendszeresen fusson, beállíthatod a crontab-ban. Például, hogy minden hónap 17-én fusson:

    Nyisd meg a crontab fájlt szerkesztésre:
    crontab -e
    ```
    0 0 17 * * /usr/bin/python3 /path/to/your/project/bot.py