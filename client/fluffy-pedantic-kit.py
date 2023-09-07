import requests
import random
import time
from bs4 import BeautifulSoup
import threading

SERVER = "172.20.27.10"  # Sostituisci con il tuo server
PORT = 30000  # Sostituisci con la tua porta
MEAN_INTERVAL = 60  # Sostituisci con la media dell'intervallo di tempo tra una richiesta e l'altra
IMAGES = []  # Inizializza la lista delle immagini

# Funzione per inviare la richiesta HTTP e gestire il timeout
def send_request(image_id):
    url = "http://{}:{}/api/{}".format(SERVER, PORT, image_id)
    start_time = time.time()
    try:
        response = requests.get(url, timeout=120)
    except requests.exceptions.Timeout:
        print(f"Timeout scaduto per l'immagine {image_id}")
    else:
        if response.status_code != 200:
            print("Errore durante la richiesta HTTP")
        else:
            elapsed_time = time.time() - start_time
            print(f"{image_id} ({elapsed_time:.2f} secondi) - {response.content}")


# Funzione per effettuare lo scraping del sito di Imgur e aggiornare la lista delle immagini
def update_images():
    global IMAGES
    url = "https://imgur.com/search?q=cute%20animals"
    response = requests.get(url)
    if response.status_code != 200:
        print("Errore durante la richiesta HTTP")

    soup = BeautifulSoup(response.content, "html.parser")
    images = soup.find_all("img")
    IMAGES = [image['src'].split("/")[-1] for image in images if image['src'].endswith('.jpg') and 'i.imgur.com' in image['src']]

# Inizializza la lista delle immagini
if not IMAGES:
	update_images()

print("Trovate " + str(len(IMAGES)) + " immagini")

while True:
    # Scegli un'immagine a caso dalla lista
    image_id = random.choice(IMAGES)
    
    # Invia la richiesta HTTP in un thread separato
    print("Invio la richiesta con immagine " + image_id)
    t = threading.Thread(target=send_request, args=(image_id,))
    t.start()

    # Calcola il prossimo intervallo di tempo
    next_interval = random.expovariate(1/MEAN_INTERVAL)

    # Attendi per il prossimo intervallo di tempo o per la fine delle richieste in corso
    print(f"Attendo {next_interval:.2f} secondi")
    time.sleep(next_interval)

