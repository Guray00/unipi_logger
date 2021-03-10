# Unipi Logger - README IN COSTRUZIONE

## Cosa è, ma soprattutto perchè
Nelle residenze nel circondario di pisa la connessione fornita crea delle sessioni da circa 8 ore dopo le quali è necessario riconnettersi. Questo script si occupa di avviare l'accesso in automatico.

## Installazione da Linux
- installare python e pip
`sudo apt install python python-pip git chromium-browser`
- navigare nella cartella nella quale si vuole scaricare il programma
`cd desidered/folder/to/clone`
- clonare la repo
`git clone https://github.com/Guray00/unipi_logger`
- installare i requisiti per python
    `pip install -r requirements.txt`
- __se non in possesso di raspberrypi__
    - scoprire la versione installata di chrome
    - recarsi su https://chromedriver.chromium.org/downloads e scaricare quella più adatta per la versione appena trovata. Se non è presente la versione esatta, scaricare una precendente.
    - Estrarre il pacchetto.

### Nota: RaspberryPi 
Se l'installazione viene effettuata su un __RaspberryPi__, sarà necessario installare il pacchetto chromedriver apposito per l'architettura armhf. Questa non è più distribuita da anni, ma fortunatamente i creatori di RaspberryPiOS si occupano di ancora di mantenerla aggiornata.
`sudo apt-get install chromium-chromedriver`

## Utilizzo
Per utilizzare il programma mandare il seguente comando __(senza "<" e ">")__:
`python ./logger.py -u <username> -pw <password>`

### Argomenti
```
    -u:         inserire utente (alice)
    --user:     inserire utente (alice)
    -pw:        inserire password (alice)
    --password: inserire password (alice)
    --log:      inserire il livello di log (tra debug, info, warning, error, critical)
    -l:         posizione per individuare la posizione del chromedriver (necessario per windows)
    --location: posizione per individuare la posizione del chromedriver (necessario per windows)
```

## Automatizzare
- Linux
Aggiungere al chrontab

- Windows
Aggiungere alla routine di sistema

## Logging
Tutti i log del programma si trovano nel file logger.log, nel caso in cui il nome del file cambiasse (per qualche motivo) sarà __nomeprogramma.log__, sempre nella stessa cartella dal quale viene eseguito.