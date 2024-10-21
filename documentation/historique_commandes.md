# Se connecter à la Raspberry
Les commands éxécutés pour configurer et se connecter à la raspberrypi

```bash
yay -S rpi-imager #installation de rpi-imager pour flaché l'OS sur la clef usb
sudo rpi-imager

nmcli device wifi connect TP-Link_A1A8 # Connection au router
nmap 192.168.0.0/24 -sV -p 22 # Pour trouver les IP des cartes (le port 22 est utilisé pour ssh)

ping 192.168.0.114 # On lançait un ping et on débranchait notre carte pour vérifié que l'addresse IP correspond bien à la notre
ssh 192.168.0.114 

scp tp-2021.pem strawberrypi@192.168.0.114:~/
``` 

Puis, étant connecté sur la raspberrypi on a éxécuté les commandes suivantes:

```bash
sudo mv tp-2021.pem /root/
ip address # pour avoir l'address MAC de la carte et obtenir no

sudo nmtui
```

Après avoir débranché la carte du routeur, on s'y connect grâce à:
```bash
ssh strawberrypi@robotpi-61.enst.fr
```

# Mettre la Raspberry à l'heure

```bash
sudo vi /etc/systemd/timesyncd.conf
# ajout de NTP=ntp.enst.fr

sudo systemctl enable systemd-timesynced.service
sudo systemctl restart systemd-timesynced.service

timedatectl list-timezones 
timedatectl set-timezone Europe/Paris
```

# Mettre en route les moteurs 

Quand connecté à la raspberry en ssh:
```bash
sudo apt install i2c-tools
i2cdetect -y 1
#Si i2cdetect ne fonctionne pas et ne renvoie pas l'adresse i2c: il faut activer i2c dans la config interface de la raspberrypi:
sudo raspi-config
interface options
I2C
enable

#installation de smbus
sudo apt install python3-smbus

#résolution de bug
#Lors du lancement du code de test, le code essayait d'accéder au port i2c-8, qui nétait pas un port que nous possédions sur notre raspberry pi. Les ports à notre disposition étaient les ports 1, 20 et 21, après deux test rapide en changeant le port 8 pour les ports 20 et 21 qui ont tous les deux résultés en des erreurs, nous avons essayé de changer le port 8 pour le port 1, ce qui a fonctionné car le moteur tournait lorsqu'on le lui demandait.

#Extraction des fichiers de test dans la raspberry, puis lancement des fichiers tests

scp dc-motor-hat-tpt.tar.gz strawberrypi@robotpi-61.enst.fr
python3 check-wiring.py
```

# Page web pour contrôller les moteurs 
On utilise une page web python utilisant flask pour interagire avec la raspberry sans avoir besoin de se connecter en ssh
La page web est hosté sur http://137.194.173.61:5000/
Les commandes exécuté pour la mettre en place sont 
```bash
sudo apt install flask 

# Puis on a crée webpage.py et templates/page.html dans dc-motor-hat-tpt (pour avoir acces a controller.py) 
# Pour lancer la pageweb:

python webpage.py 
```

On utilise des bouttons avec des methodes post pour activer les moteurs de la raspberry

# Mise de la carte raspberry sur le gitlab

Sur gitlab dans `setting > access token` on a crée un token d'authentication pour la raspbery  
Puis on a crée un `.gitconfig` pour la raspberry
```gitconfig
[remote "origin"]
  url = https://oauth2:[le token d'authentication]@gitlab.telecom-paris.fr/proj103/2425/gr6/team1.git
[user]
        email = Raspberry\n@project_7776_bot_6d5a4dffd92789fc507b95a2ecbf920
        name = Raspberry
```
L'address email à été trouvé dans la liste des membres du gitlab

On a ensuit fait 
```bash
git clone git@gitlab.enst.fr:proj103/2425/gr6/team1.git

git config --global user.email "Raspberry@project_7776_bot_6d5a4dffd92789fc507b95a2ecbf920"
git config --global user.name "Raspberry"

git add code_raspberry/*

git commit -m "Ajout du code de la raspberry"
git push
```

# Automatisation de demarage de la page web et git pull

On utilise un script bash qui est lancé par un service systemd au démarage de la raspberry pour faire un `git pull` et lancer la pageweb

Le code bash en question s'appelle `raspberry_start_up.sh` et contient
```bash
#!/bin/bash

cd /home/strawberrypi/team1/code_raspberry/
git pull
python webpage.py
```
Le fichier service est `/etc/systemd/system/start_up_pull_webpage.service` et contient 
```service
[Unit]
Description=Git pull and start webpage
After=network.target

[Service]
ExecStart=/bin/bash /home/strawberrypi/team1/raspberry_start_up.sh
Restart=always

[Install]
WantedBy=multi-user.target
```

Les commandes éxécutés pour configurer pour configurer le service sont:
```bash
chmod +x raspberry_start_up.sh
sudo systemctl daemon-reload
sudo systemctl enable start_up_pull_webpage.service
sudo systemctl start start_up_pull_webpage.service
```




