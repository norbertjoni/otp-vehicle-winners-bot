import os
import requests
from bs4 import BeautifulSoup
import fitz  # PyMuPDF
from dotenv import load_dotenv
import discord
import shutil

# Betöltjük a .env fájl tartalmát
load_dotenv()

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))

intents = discord.Intents.default()
client = discord.Client(intents=intents)

# Megadott számok az .env fájlból
my_numbers = os.getenv('MY_NUMBERS').split(',')

def get_web_winners():
    url = "https://www.otpbank.hu/portal/hu/Megtakaritas/ForintBetetek/Gepkocsinyeremeny"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to load page")
    print("Page loaded successfully.")

    soup = BeautifulSoup(response.text, 'html.parser')
    winners = {}
    list_container = soup.find('section', {'id': 'mtxt_sorsolasi__container'})
    if list_container:
        for item in list_container.find_all('li', class_='sf-listitem'):
            number, *prize = item.text.split()
            winners[number] = ' '.join(prize)
    return winners

def download_pdf(download_folder):
    url = "https://www.otpbank.hu/portal/hu/Megtakaritas/ForintBetetek/Gepkocsinyeremeny"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to load PDF list page")
    soup = BeautifulSoup(response.text, 'html.parser')
    pdf_link = ""
    for link in soup.find_all('a', href=True):
        if 'GK_At_nem_vett_jegyzek' in link['href']:
            pdf_link = "https://www.otpbank.hu" + link['href']
            break
    if not pdf_link:
        raise Exception("No PDF link found on the page")

    os.makedirs(download_folder, exist_ok=True)
    response = requests.get(pdf_link)
    if response.status_code != 200:
        raise Exception("Failed to download PDF")

    pdf_filename = os.path.join(download_folder, "GK_At_nem_vett_jegyzek.pdf")
    with open(pdf_filename, 'wb') as f:
        f.write(response.content)
    return pdf_filename

def extract_numbers_from_pdf(file_path):
    document = fitz.open(file_path)
    numbers = []
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text = page.get_text("text")
        lines = text.split('\n')
        for line in lines:
            digits = ''.join(filter(str.isdigit, line))
            for i in range(0, len(digits), 9):
                number = digits[i:i+9]
                if len(number) == 9:
                    numbers.append(number)
    return numbers

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        # Ellenőrizzük a nyerőszámokat a weboldalon
        web_winners = get_web_winners()
        found_winners_web = {num: web_winners[num] for num in my_numbers if num in web_winners}

        # Ellenőrizzük a PDF-ből a számokat a már meglévő PDF fájlból
        download_folder = "/tmp"
        pdf_path = download_pdf(download_folder)
        pdf_numbers = extract_numbers_from_pdf(pdf_path)
        found_winners_pdf = [num for num in my_numbers if num in pdf_numbers]

        # Eredmény összegzése
        if found_winners_web or found_winners_pdf:
            message = "Gratulálunk, nyertél! Nyerő számaid és nyereményeid:\n"
            for num, prize in found_winners_web.items():
                message += f"{num}: {prize}\n"
            if found_winners_pdf:
                for num in found_winners_pdf:
                    message += f"{num}: PDF-ból kikért szám ami nyert\n"
        else:
            message = f"Lefutott az ellenőrzés, nem nyertél. Saját részvényszámaid:\n" + "\n".join(my_numbers) + "\nEllenőrizd a részleteket itt: https://www.otpbank.hu/portal/hu/Megtakaritas/ForintBetetek/Gepkocsinyeremeny"
        
        await channel.send(message)
        
        # Töröljük a letöltött PDF fájlt és mappát
        os.remove(pdf_path)
        shutil.rmtree(download_folder)
    else:
        print("Channel not found")
    await client.close()

if __name__ == "__main__":
    client.run(TOKEN)
