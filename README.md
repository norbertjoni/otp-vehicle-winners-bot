# OTP Winners Bot

Ez a projekt egy Discord bot, amely ellenőrzi az OTP Gépkocsinyeremény betétszámla nyerőszámait, és értesítést küld a Discord csatornára, ha a megadott számok nyertek.

## Telepítés és futtatás

### Előfeltételek

- Docker és Docker Compose telepítve a rendszereden.
- Egy Discord bot token és egy Discord csatorna ID.

### Lépések

1. **Repository klónozása:**

   ```sh
   git clone <repository_url>
   cd <repository_directory>

2. **Hozz létre egy .env fájlt a projekt gyökérkönyvtárában a következő tartalommal:**

   ```sh
   DISCORD_BOT_TOKEN=your_discord_bot_token
   DISCORD_CHANNEL_ID=your_discord_channel_id
   MY_NUMBERS=your_numbers_comma_separated

3. **Docker image építése és futtatása:**
   
   ```sh
    docker-compose up --build


###Megjegyzés:
A konténer futtatása közben a bot először azonnal elindul, és ellenőrzi a nyerőszámokat. A letöltött PDF fájlokat a downloads mappában tárolja ideiglenesen, majd törli azokat az ellenőrzés után.