import requests
import random
import time
import threading
import sys
import csv
import json
import os.path

SCHEDULER = "ROUND ROBIN"
SERVER = "172.20.27.10"
PORT = 30000
MEAN_INTERVAL = 1.0  
INTERVAL_STEP = 0.1
REQUESTS_PER_STEP = 100
NODE_ASSOCIATION = {
    "simulator-757c4599c6-7scnb": "node-b",
    "simulator-757c4599c6-l7md8": "node-c"
}
NODE_DELAY = {
    "node-b": "50",
    "node-c": "5"
}
FILE_PATH = "results.csv"
SEED_FILE = "seeds.txt"

# Funzione per inviare la richiesta HTTP e gestire il timeout
def send_request(writer, index, seed, mean):
    url = "http://{}:{}/".format(SERVER, PORT)
    start_time = time.time()
    try:
        response = requests.get(url, timeout=120)
    except requests.exceptions.Timeout:
        print(f"Timeout scaduto per la richiesta")
    else:
        if response.status_code != 200:
            print("Errore durante la richiesta HTTP")
        else:
            elapsed_time = time.time() - start_time
            writer.writerow([
                SCHEDULER, 
                mean, 
                seed, 
                index, 
                NODE_ASSOCIATION[response.json()["container"]], 
                NODE_DELAY[NODE_ASSOCIATION[response.json()["container"]]], 
                response.json()["time"], 
                elapsed_time
            ])
            #print(f'{index} -> {elapsed_time:.2f}')


file_exists = os.path.isfile(FILE_PATH)
fd = open(FILE_PATH,'a')
writer = csv.writer(fd, delimiter=';')

headers = [
    "scheduling", 
    "lambda_between_requests", 
    "seed", 
    "index", 
    "node", 
    "node_delay (ms)", 
    "sleep_time (s)", 
    "actual_time (s)"
]
if not file_exists:
    writer.writerow(headers)

for mean_interval in range(1, 10, 1):
    mean = mean_interval/10
    print(f'Current mean: {mean}')
    seeds_file = open(SEED_FILE, 'r')

    for line in seeds_file:
        seed = line.rstrip()
        print(f'Current seed: {seed}')
        random.seed(seed)
        threads = []

        for i in range(100):

            # Invia la richiesta HTTP in un thread separato
            t = threading.Thread(target=send_request, args=(writer,i,seed, mean))
            t.start()
            threads.append(t)

            # Calcola il prossimo intervallo di tempo
            next_interval = random.expovariate(1/mean)

            # Attendi per il prossimo intervallo di tempo o per la fine delle richieste in corso
            #print(f"Attendo {next_interval:.2f} secondi")
            time.sleep(next_interval)
        
        for t in threads:
            t.join()

fd.close()
