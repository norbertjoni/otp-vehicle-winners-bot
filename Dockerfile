FROM python:3.9-slim

# Alapcsomagok telepítése
RUN apt-get update && apt-get install -y \
    cron \
    && rm -rf /var/lib/apt/lists/*

# Munka könyvtár létrehozása
WORKDIR /app

# Szolgáltatások és Python csomagok telepítése
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Python script és egyéb fájlok másolása
COPY . .

# Cron job hozzáadása
RUN echo "0 0 17 * * root python /app/bot.py >> /var/log/cron.log 2>&1" >> /etc/crontab

# Cron log fájl létrehozása és jogosultságok beállítása
RUN touch /var/log/cron.log && chmod 666 /var/log/cron.log

# Cron indítása, Python script egyszeri futtatása és naplófájl figyelése
CMD python /app/bot.py && cron && tail -f /var/log/cron.log
