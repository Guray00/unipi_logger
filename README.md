# Unipi Logger - README IN COSTRUZIONE

## Cosa è, ma soprattutto perchè
Nelle residenze nel circondario di pisa la connessione fornita crea delle sessioni da circa 8 ore dopo le quali è necessario riconnettersi. Questo script si occupa di avviare l'accesso in automatico.

## Installer linux

Eseguire il comando seguente e lo script di installazione partirà automaticamente. _Funziona con WSL._
```bash
curl -s https://raw.githubusercontent.com/Guray00/unipi_logger/main/install.sh > /tmp/ul_install.sh && chmod a+x /tmp/ul_install.sh && /tmp/ul_install.sh
```

## Installazione manuale da Linux
- installare python e pip
`sudo apt install python python-pip git chromium-browser`
- navigare nella cartella nella quale si vuole scaricare il programma
`cd desidered/folder/to/clone`
- clonare la repo
`git clone https://github.com/Guray00/unipi_logger`
- installare i requisiti per python
    `pip install -r requirements.txt`. Se stai avendo problemi di compatibilità, utilizza: `pip install -r .\requirements.txt  --use-feature=2020-resolver`
- __se non in possesso di raspberrypi__
    - scoprire la versione installata di chrome con `chromium-browser --product-version`
    - recarsi su https://chromedriver.chromium.org/downloads e scaricare quella più adatta per la versione appena trovata. Se non è presente la versione esatta, scaricare una precendente.
    - Estrarre il pacchetto.


### Nota: RaspberryPi 
Se l'installazione viene effettuata su un __RaspberryPi__, sarà necessario installare il pacchetto chromedriver apposito per l'architettura armhf. Questa non è più distribuita da anni, ma fortunatamente i creatori di RaspberryPiOS si occupano di ancora di mantenerla aggiornata.
`sudo apt-get install chromium-chromedriver`

## Installazione Windows
- ....
- Scoprire la versione adatta aprendo Chrome e andando all'indirizzo "chrome://settings/help"

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
    --force:    forza il tentativo di connessione nonostante siano stati raggiunti i 5 tentativi. 
		Necessario per far ripartire il programma dopo un eventuale cambio di credenziali.
```

## Automatizzare
### Linux
Aggiungere al crontab
```bash 
crontab -e
```
e poi inserire alla fine del documento:
```bash 
*/2 * * * * python ~/.unipi_logger/logger.py -u <USERNAME-HERE>-pw <PASSWORD-HERE> >/dev/null 2>&1
```
Per assicurarsi che le modifiche abbiano effetto, facciamo ripartire il crontab
```bash 
sudo /etc/init.d/cron restart
```
### Windows
Aggiungere alla routine di sistema

## Logging
Tutti i log del programma si trovano nel file logger.log, nel caso in cui il nome del file cambiasse (per qualche motivo) sarà __nomeprogramma.log__, sempre nella stessa cartella dal quale viene eseguito.

## VPN e OpenVPN
Se stai utilizzando una vpn, e se sei in una residenza __devi__ usare una vpn, ricordati di mantenere fuori dalla route gli indirizzi per l'accesso. Per farlo:
```bash
sudo nano /etc/openvpn/server.conf
```

adesso inserire
```
push "route 131.114.101.101 255.255.255.255 net_gateway"
push "route 131.100.1.1 255.255.255.255 net_gateway"
push "route 172.217.21.67 255.255.255.255 net_gateway"
```

assicurati che non vengano violate in qualche configurazione speciale presente nella cartella ccd

## Aggiornare questo script
```git
cd /inside/the/program/folder
git reset --hard
git pull
```