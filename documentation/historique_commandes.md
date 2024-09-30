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

```