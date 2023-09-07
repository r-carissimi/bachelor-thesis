# Usa un'immagine di Python come base
FROM python:3.9-slim
RUN /bin/sh -c set -eux; apt-get update; apt-get install -y --no-install-recommends stress-ng procps 

# Copia il codice sorgente nella directory /app del container
COPY . /app

# Imposta la directory di lavoro come /app
WORKDIR /app

# Installa le dipendenze del codice sorgente
RUN pip install -r requirements.txt

# Espone la porta 8000 del container
EXPOSE 5000

# Avvia il server quando il container viene avviato
CMD [ "python", "server.py" ]

