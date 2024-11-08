# Suivi du projet


*Texte en italique*
_Texte en italique_
**Texte en gras**
__Texte en gras__
***Texte en italique et en gras***
___Texte en italique et en gras___
~~Ce texte est barré.~~ mais pas celui-là.


##REPARTITION DES TACHES

controle des moteurs : Martin
interface web simplifié : Jeffrey
mini serveur permettant le controle manuel du robot : Joshua
dialogue avec le serveur web de suivi de déplacement : Jeffrey
Reconnaissance des codes ArUco via la caméra, évaluation de la distance : Alice
design du robot : Edouard



## 23/09/2024:
Installation de l’OS sur la Raspberry Pi

Le nom de notre raspberry est “strawberrypi”. Le mot de passe est “pa1LLeB@ie”.


utiliser le github


### Connecter les appareils au routeur

On connecte la raspberry pi en filaire au serveur tp-link.
Pour connecter un ordinateur au routeur sans fil par wifi
	clé de sécurité réseau : 53119193


### Trouver l’adresse IP de notre raspberry

*version 1 :* 
se rendre à l’adresse suivante via un navigateur : http://192.168.0.1/
se connecter en tant qu’administrateur:
mot de passe : Groupe6*
on peut alors voir les adresses IP des différents appareils connectés.
Remarque : le serveur a interdit tous les accès administrateur à cause d’un nombre trop grand de tentatives de connexion. On doit opter pour une autre méthode.

*version 2 :*
pour rechercher toutes les adresses ip des appareils connectés:
	nmap 192.168.0.1/24
le masque /24 indique qu’il faut chercher toutes les adresse IP commençant par 192.168.
Cela nous donne une liste de 4 appareils. On ping chacune en débranchant puis rebranchant notre raspberry pour identifier la bonne adresse IP. On trouve que notre raspberry a l’adresse IP 192.168.0.100

### Se connecter en ssh à la raspberry

	
	ssh strawberrypi@192.168.0.100
	
	
## 27/09/2024:

### TESTS DES CAMERAS (Joshua, Alice)

On a branché la caméra à l'ordinateur par cable USB. On peut voir l'image en tant réél, la caméra fonctionne. On a testé la librairie python open-cv pour récupérer les images de la caméra sous forme de tableau numpy. Problème : sur l'ordinateur, la capture d'une image prend 18 secondes (contre quelques instants pour capturer une image avec la webcam). 

### TESTS DES MOTEURS (Martin)

On a branché l'alimentation des moteurs à la carte de controle et branché la carte de controle à la batterie. 
On a ensuite testé les moteurs avec un script python de base.
Suite à cela, on a dénudé les cables des encodeurs afin d'être capable de brancher ces derniers. Une fois branchés, on a relancé d'autres tests afin de s'assurer de leur bon fonctionnement, tout en profitant de cette occasion pour faire des tests plus poussés sur le fonctionnement des moteurs en essayant de les faire tourner simultanément, à des vitesses différentes, de faire en sorte que l'un des  deux s'arrête pendant que l'autre continue à tourner etc.


### DESIGN DU ROBOT (Edouard)

On a mesuré les différents éléments qui seront sur le chassis et fais un plan au brouillon de leur disposition sur le chassis.


	
	
## 07/10/2024:

### TESTS DETECTION ARUCO (Alice)

J'utilise la librairie cv2 de python pour capturer les images de la caméra et détecter les markers aruco. Il se trouve que si le marker est trop près 
(s'il prend presque tout l'écran), le programme ne le reconnait pas. J'ai ensuite utilisé la librairie pygame pour créer une fenetre
qui affiche en temps réel l'image de la caméra et affiche la distance estimée au marker si un marker est détecté. 

### TESTS DE PAGEWEB RASPBERRY (Jeffrey)

J'ai écrit une pageweb rudimentaire en python avec flask sur la raspberry pour contrôller les moteurs à distance.


### ASSEMBLAGE DU ROBOT (Edouard, Martin)

Decoupage des pièces en bois puis assemblage des différentes parties.
Problème : le support de la caméra est trop haut et les roues trop basses par rapport à la roue libre.


## 21/10/2024:

### AJOUT DU GIT SUR LA RASPBERRY ET CONFIGURATION DE LA PAGEWEB POUR CONTROLLER LA RASPBERY (Jeffrey)

J'ai utilisé un token d'accès gitlab que j'ai mis sur la raspberry pour mettre son code dans le repisitory.
La pageweb est construit en python avec flask afin de pouvoir utilisé les commandes python qui controle les moteurs.
La pageweb est ébergé sur http://137.194.173.61:5000/

### TEST MODULE CAMERA (Alice)

Première version du module caméra dans le dossier caméra.
Problème de version du module opencv, pour se faire, on décide d'utiliser des environnements virtuels (voir ci-dessous)

### CREATION D'ENVIRONNEMENT VIRTUEL PYTHON (Alice, Jeffrey)

création de req.txt, lancer_python.sh et setup.sh qui premettent l'utilisation d'un environnement

### AJUSTEMENT ROBOT (EDOUARD, MARTIN)

Changement du module caméra pour que sa taille soit mieux adaptée, tentative de réparation des roues qui n'étaient pas alignées ce qui entraînait empêchait le robort d'avancer droit.

## 08/11/2024:

### REPARATION ROBOT (MARTIN, EDOUARD)

Suite de la réparation de roue après que les dernières solutions aient échoué lamentablement.
Utilisation de colle forte pour stabiliser les roues qui commencaient à se détacher du support de la raspberrypi.

### AJOUT MODULE CAMERA (Alice, Jeffrey)

On a ajouté sur le git dans le dossier code_raspberry le module pour utiliser la camera et modifier la page web pour pouvoir y faire des tests. Problème : on a push alors que l'ordinateur était dans l'environnement python. On a du supprimer ensuite les fichiers inutiles, ce qui nous a fait perdre du temps. On a ajouté ensuite tout le dossier mon_env dans le .gitignore . 
On voit désormais sur le site web si la caméra est connectée. Problème : le résultat n'est pas le même pour tous les utilisateurs (hypothèse : on cherche à accéder à la caméra trop de fois par seconde).
On essaye aussi de sauvegarder l'image capturée sur la raspberry et d'afficher l'image sur le site web. Problème : on n'arrive pas à afficher des images sur le site (le fichier n'est pas trouvé alors qu'il s'y trouve).






