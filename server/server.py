from flask import Flask
import random
import time
import subprocess
import threading
import multiprocessing
import os
import socket
from threading import Lock
import signal

app = Flask(__name__)

# tempo medio di risposta in secondi
tempo_medio = os.getenv('FLUFFY_AVG_TIME', 0.1)

# percentuale di CPU da occupare in caso di richieste in fase di elaborazione
percentuale_cpu = os.getenv('FLUFFY_CPU_PERCENT', 80)

index = 0
index_lock = Lock()
pids = dict()

@app.route('/')
def api():
    global index
    with index_lock:
        this_index = index
        index = index + 1

    # genera un tempo di attesa casuale
    tempo_attesa = random.expovariate(1/tempo_medio)
    
    # avvia il thread per occupare la CPU
    tmp = subprocess.Popen(["stress-ng", "--cpu", str(multiprocessing.cpu_count()), "--cpu-load", str(percentuale_cpu)])
    pids[this_index] = tmp.pid
    print(f'Facendo partire il processo con PID {pids[this_index]}')

    # metti in pausa il processo per il tempo di attesa casuale
    time.sleep(tempo_attesa)

    # ferma lo stress-ng
    print(f'Fermando il processo con PID {pids[this_index]}')
    os.kill(pids[this_index], signal.SIGTERM)

    dict_response = dict()
    dict_response["index"] = this_index
    dict_response["time"] = '{:.2f}'.format(tempo_attesa)
    dict_response["container"] = socket.getfqdn()
    return dict_response
    
if __name__ == '__main__':
    print(f"Cores: {multiprocessing.cpu_count()}")
    print(f"Avg time: {tempo_medio}")
    print(f"Percent CPU: {percentuale_cpu}")
    app.run(host='0.0.0.0', port=5000)

