#!/usr/bin/env python3.7

import argparse
import requests
from bs4 import BeautifulSoup, Tag
import json
import os
from dotenv import load_dotenv
import platform
import re
import random
import time as t
from datetime import datetime, time
from statistics import mean




load_dotenv()

# Configura Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Definisci la lista dei modelli attesi per la Jeep (puoi espandere per altre marche)
expected_models = ['cherokee', 'compass', 'wrangler', 'renegade']


parser = argparse.ArgumentParser()
parser.add_argument("--add", dest='name',
                    help="name of new tracking to be added")
parser.add_argument("--url", help="url for your new tracking's search query")
parser.add_argument("--minPrice", help="minimum price for the query")
parser.add_argument("--maxPrice", help="maximum price for the query")
parser.add_argument("--marca", help="car brand to filter (e.g., BMW, Audi)")
parser.add_argument("--modello", help="car model to filter (e.g., A4, 320d)")
parser.add_argument("--alimentazione",
                    help="fuel type (e.g., benzina, diesel)")
parser.add_argument(
    "--cambio", help="gearbox type (e.g., automatico, manuale)")
parser.add_argument("--km_min", help="minimum kilometraggio (e.g., 10000)")
parser.add_argument("--km_max", help="maximum kilometraggio (e.g., 100000)")
parser.add_argument(
    "--regione", help="region or city to filter (e.g., Veneto, Padova)")
parser.add_argument("--inserzionista",
                    help="private or dealer (e.g., privato, concessionario)")
parser.add_argument('--refresh', '-r', dest='refresh',
                    action='store_true', help="refresh search results once")
parser.set_defaults(refresh=False)

args = parser.parse_args()

queries = dict()
dbFile = "searches.tracked"

# Load queries from file

def load_queries():
    global queries
    if not os.path.isfile(dbFile):
        return
    with open(dbFile) as file:
        queries = json.load(file)

# Save queries to file

def save_queries():
    with open(dbFile, 'w') as file:
        file.write(json.dumps(queries))

# Extract model from title


def extract_model_from_title(title, expected_models):
    """ Estrai il modello dal titolo cercando se uno dei modelli attesi è presente """
    title_lower = title.lower()
    for model in expected_models:
        if model.lower() in title_lower:
            return model.lower()
    return None

# Process collected data


# Process collected data
def process_collected_data(all_prices, filters):
    # Raggruppa i prezzi per modello
    prices_by_model = {}
    for entry in all_prices:
        model = entry['model']
        price = entry['price']
        prices_by_model.setdefault(model, []).append(price)

    # Debug per vedere quali modelli sono stati raccolti
    print(f"Modelli raccolti: {list(prices_by_model.keys())}")
    print(f"Prezzi per modello: {prices_by_model}")

    # Calcola il prezzo minimo statistico per il modello desiderato
    target_model = filters.get('modello')

    # Verifica se target_model è None o una stringa vuota
    if not target_model:
        print("Nessun modello specificato per il target.")
        return

    # Converti target_model in lowercase
    target_model = target_model.lower()
    print(f"Modello target: {target_model}")

    if target_model not in prices_by_model:
        print(f"Nessun dato disponibile per il modello {target_model}")
        return

    model_prices = prices_by_model[target_model]
    avg_price = mean(model_prices)
    min_price_stat = min(model_prices)
    max_price_stat = avg_price * 1.2  # Ad esempio, il 120% del prezzo medio

    print(f"Prezzo medio per {target_model}: {avg_price}")
    print(f"Prezzo minimo statistico per {target_model}: {min_price_stat}")

    # Ora filtra gli annunci originali basandosi su questo prezzo
    filter_ads_by_price(min_price_stat, max_price_stat, target_model, filters)

# Filter ads based on calculated price


def filter_ads_by_price(min_price_stat, max_price_stat, target_model, filters):
    # Dobbiamo rifare la richiesta per ottenere gli annunci
    url = args.url
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    product_list_items = soup.find_all('div', class_=re.compile(r'item-card'))

    msg = []
    for product in product_list_items:
        title = product.find('h2').string
        try:
            price = product.find('p', class_=re.compile(r'price')).contents[0]
            price = int(re.sub(r'[^0-9]', '', price))
        except (AttributeError, ValueError):
            continue

        model = extract_model_from_title(title)
        if not model or model.lower() != target_model:
            continue  # Salta se non è il modello desiderato

        if price < min_price_stat or price > max_price_stat:
            continue  # Filtra se il prezzo non è nel range desiderato

        link = product.find('a').get('href')
        location = product.find('span', re.compile(r'town')).string if product.find(
            'span', re.compile(r'town')) else "Unknown location"

        msg.append(
            f"Annuncio trovato: {title} @ {price} - {location} --> {link}\n")
        queries[title] = {'url': link, 'price': price, 'location': location}

    if msg:
        send_telegram_messages(msg)
        print("\n".join(msg))
    else:
        print('Nessun annuncio corrisponde ai criteri filtrati.')

    save_queries()

# Run a query on Subito.it


import random
import time

def run_query(url, name, notify, minPrice, maxPrice, filters):
    print(datetime.now().strftime("%Y-%m-%d, %H:%M:%S") +
          f" Running query (\"{name}\" - {url})...")

    global queries
    all_prices = []
    page_number = 1  # Per gestire la paginazione

    # Definisci gli headers per rendere la richiesta più simile a quella di un browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive"
    }

    while True:
        paginated_url = f"{url}&o={page_number}"
        
        # Esegui la richiesta HTTP con gli headers
        page = requests.get(paginated_url, headers=headers)

        # Crea il soup per analizzare l'HTML della pagina
        soup = BeautifulSoup(page.text, 'html.parser')
        
        # Aggiungi questo blocco per salvare l'HTML in un file per il debug
        with open(f"debug_page_{page_number}.html", "w", encoding="utf-8") as file:
            file.write(soup.prettify())
        
        product_list_items = soup.find_all('div', class_=re.compile(r'item-card'))

        if not product_list_items:
            break  # Nessun altro prodotto, uscire dal ciclo

        for product in product_list_items:
            title = product.find('h2').string
            
            # Debug per verificare se il titolo è stato trovato correttamente
            if title:
                print(f"Titolo trovato: {title}")
            else:
                print("Titolo non trovato per un annuncio")
            try:
                price = product.find('p', class_=re.compile(r'price')).contents[0]
                price = int(re.sub(r'[^0-9]', '', price))
            except (AttributeError, ValueError):
                continue  # Salta se non c'è un prezzo valido

            # Salva il modello e il prezzo
            model = extract_model_from_title(title, expected_models)
            if model:
                all_prices.append({'model': model.lower(), 'price': price})

        # Aggiungi il ritardo casuale tra le richieste
        time.sleep(random.uniform(5, 15))

        page_number += 1  # Passa alla pagina successiva

    # Dopo aver raccolto tutti i dati, procedi con il calcolo
    process_collected_data(all_prices, filters)


# Send Telegram notifications


def send_telegram_messages(messages):
    for message in messages:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        }
        response = requests.post(url, data=data)
        if response.status_code != 200:
            print(
                f"Errore nell'invio del messaggio Telegram: {response.status_code}, {response.text}")


if __name__ == '__main__':
    load_queries()

    if args.refresh:
        filters = {
            'marca': args.marca,
            'modello': args.modello if args.modello is not None else '',  # Evita che 'modello' sia None
            'alimentazione': args.alimentazione,
            'cambio': args.cambio,
            'km_min': args.km_min,
            'km_max': args.km_max,
            'regione': args.regione,
            'inserzionista': args.inserzionista
        }

        # Aggiungi un debug per verificare i filtri creati
        print(f"Filtri: {filters}")

        run_query(args.url, args.name, True, args.minPrice if args.minPrice else "null",
                  args.maxPrice if args.maxPrice else "null", filters)

    save_queries()
