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

### AJUSTEMENT ROBOT (Edouard, Martin)

Changement du module caméra pour que sa taille soit mieux adaptée, tentative de réparation des roues qui n'étaient pas alignées ce qui entraînait empêchait le robort d'avancer droit.

## 08/11/2024:

### REPARATION ROBOT (Martin, Edouard)

Suite de la réparation de roue après que les dernières solutions aient échoué lamentablement. Utilisation de colle forte pour stabiliser les roues qui commencaient à se détacher du support de la raspberrypi.
### AJOUT MODULE CAMERA (Alice, Jeffrey)

On a ajouté sur le git dans le dossier code_raspberry le module pour utiliser la camera et modifier la page web pour pouvoir y faire des tests. Problème : on a push alors que l'ordinateur était dans l'environnement python. On a du supprimer ensuite les fichiers inutiles, ce qui nous a fait perdre du temps. On a ajouté ensuite tout le dossier mon_env dans le .gitignore . 
On voit désormais sur le site web si la caméra est connectée. Problème : le résultat n'est pas le même pour tous les utilisateurs (hypothèse : on cherche à accéder à la caméra trop de fois par seconde).
On essaye aussi de sauvegarder l'image capturée sur la raspberry et d'afficher l'image sur le site web. Problème : on n'arrive pas à afficher des images sur le site (le fichier n'est pas trouvé alors qu'il s'y trouve).

### CALIBRAGE CAMERA (Joshua)

Ecriture d'un code python permettant d'obtenir les coordonnées, l'inclinaison et la distance à la caméra d'un QR code observé par cette dernière. J'observe à la fin de la séance que j'ai besoin de trouver la matrice intrinsèque de la caméra afin de continuer à coder.


## 14/11/2024: 

### DEBUGGAGE DU SITE (Alice, Jeffrey)

Tentative de faire apparaitre le flux caméra sur le site web. Les images prises par la caméra peuvent être récupérés sans souci, mais il y a une certaine latence entre deux images (de plusieurs dizaines de seconde) empêchant d'avoir un flux fluide.

### CALIBRAGE DES ROUES / PROGRAMME MOTEUR (Edouard, Martin)

Les deux roues du robot ne tournent pas à la même vitesse et ne commence ni ne termine de tourner en même temps. Le but de la séance est premièrement de proposer un ratio de vitesse entre les deux roues permettant d'atteindre une marche rectiligne. Une fois que cela est fait, je pourrais vérifier les résultats donnés par les encodeurs après une ligne droite pour regarder comment calibrer les moteurs pour qu'il commence et finisse de tourner en même temps. Ajout de quatre boutons permettant d'avancer, reculer ou tourner à gauche et à droite. Le robot a l'air d'avancer droit, mais recule en tournant un peu. Edouard a ajouté le dépôt git sur son PC afin d'arrêter de devoir coder avec le PC de Martin.

### CALIBRAGE DE LA CAMERA (Joshua)

Prise de différentes photos avec la caméra afin de trouver la matrice intrinsèque de la caméra, ce qui permettra ensuite de la calibrer. Des résultats sont trouvés mais aucun n'est vraiment concluant (test surtout effectués pour l'évaluation de la distance du QR code à la aruco).

### TEST DU SERVEUR DE SUIVI (Martin)

Envoi d'une requête simple au serveur, qui m'a tout simplement répondu OK


## 19/11/2024 (Matin)

### ENVOI DES REQUETES AU SERVEUR DE SUIVI (Martin, Jeffrey)

Utilisation du module python `requests` pour envoyer des requetes au serveur de suivi (debugage par envoi de requete à requestcatcher.com)

### DETERMINATION DE LA POSITION DU ROBOT A PARTIR DES MARQUEURS (Alice) 

Creation d'une fonction qui prend en argument une liste de liste de markers detectés et qui 
renvoie la position estimée du robot ainsi que l'erreur en cm.
On utilise une méthode de triangulation en prenant pour distance à chaque marker repère 
détecté la moyenne de toutes les distances mesurées.


### OBTENTION DES DONNÉES DE LECTURE DU ACURO VU PAR LA RASPBERRY (Joshua, Jeffrey) 

Résolution de conflit de modules python et implementation du code

### MISE A JOURS DU FIRMWARE DE LA RASPBERRY (Martin, Jeffrey)


### RETOUCHANGE DE LA PAGE WEB (Jeffrey)




## 19/11/2024 (Après-midi)

### ASSERVISEMENT DES MOTEURS POUR AJUSTER LE POSITIONNEMENT (Martin, Jeffrey, Edouard)
Asservisement en ligne droite (Martin, Jeffrey): detection du décalage de tick des moteurs et adaptation en conséquence 

Asservisement par rotation (pouvoir tourner le robot d'un certain angle) (Edouard et Martin)

### DETERMINATION DE LA POSITION DU ROBOT A PARTIR DES DONNÉE DES MARQUEURS (Alice)

creation du module position_from_arucos qui contient notamment get_position_from_markers qui permet de 
trouver la position du robot par triangulation en connaissant la distance aux repères du terrain (grace à la caméra).
La fonction get_orientation permet quant à elle d'avoir l'orientation du robot à partir des reperes visibles sur une image
prise depuis une position donnée. (non testée sur le terrain)

### FONCTIONS POUR COMMUNIQUER AVEC LE SERVEUR DE SUIVI (Jeffrey)

Creation de fonction dans webpage permettant d'envoyer la position du robot sur le serveur de suivi.
Remarque : le serveur de suivi n'a pas la meme origine que nous dans le repère du terrain, ce qui nous oblige
à faire une petite conversion.

### DEPLACEMENT AUTOMATIQUE SELON X ET Y (Edouard)

fonction aller_vers_case du fichier main.py : le robot se rend à la position demandé en se déplaçant uniquement
selon les axes (Ox) et (Oy)


## 20/11/2024 (Matin)

### GESTION DE LA POSITION DU ROBOT LORS DES DEPLACEMENTS AUTOMATIQUES (Alice)

Creation de la classe Position_robot qui garde en mémoire la position et l'orientation actuelle
du robot. La position et l'orientation sont modifiées par les fonctions avance_cm et rota_deg de
moteur.py. On peut également modifier la position grâce à des boutons sur la page web.

### ALGORITHME DE GUIDAGE VERS LES DRAPEAU (Joshua)

Si on detecte un drapeau grace à la caméra, le robot calcule sa position grâce à l'image, se rend
sur la case adjacente la plus proche, puis tourne autour du drapeau jusqu'à trouver l'id.

### GUIDAGE VERS UNE CASE DEPUIS PAGE WEB (Jeffrey)

Boutons sur le site web pour initialiser la position du robot (avec la case où il se trouve).
Boutons sur le site web pour se rendre sur une autre case.

### RECONSTRUCTION DU TERRAIN EN 0A128 (Alice, Martin)

On retrace sur le sol la grille du terrain et on positionne les reperes sur des pieds de chaises
aux quatre coins. Cela permet à tout le groupe 6 de faire ses tests sans avoir à aller loin.
(Un autre terrain avait déjà été dessiné par nos soin en 1A318 avant qu'on soit délocalisés)


## 20/11/2024 (Après-midi)

### PILOTAGE MANUEL DU ROBOT AVEC LES TOUCHES DU CLAVIER (Edouard)

Jusqu'ici, on pouvait diriger de manière approximative le robot via des boutons sur le site.
Désormais, le pilotage du robot est beaucoup plus aisé et précis.

### TESTS RECHERCHE DRAPEAU (Joshua, Edouard)

Test de l'algorithme pour chercher les drapeaux.

### PRISE EN COMPTE DU DECALAGE DE LA CAMERA PAR RAPPORT AU CENTRE LORS DE LA TRIANGULATION (Alice)

Amelioration de la triangulation.

### TOUR SUR LUI MEME AVEC ARRETS (Martin)

Creation d'un fonction permettant au robot de tourner de petits angles plusieurs fois
en minimisant les erreurs d'approximation (s'assure que le robot a bien fait un tour complet
à la fin).

### REPERAGE GRACE AUX REPERES EN TOURNANT SUR SOI-MEME (Jeffrey, Alice)

(utilise la fonction précédente)
Creation d'une fonction ordonnant au robot de faire un tour sur lui meme et de prendre
des photos autour de lui pour ensuite proceder à la triangulation.

### TESTS ET DEBOGAGE DU REPERAGE GRACE AUX REPERES (Martin, Jeffrey)

Tests de la fonction précédante avec le robot sur le terrain.

### CREATION D'UN PETIT DRAPEAU ROUGE A ACCROCHER SUR LE ROBOT (Alice)

Il est écrit notre groupe et notre équpie (6.1) sur notre robot de sorte qu'on puisse le reconnaitre.

## 10/12/2024

### STRATÉGISATION AVEC LES AUTRES GROUPES (Tout le monde)

### DÉBUGAGE DES PROBLÈMES RENCONTRÉES PENDENT L'ÉVALUATION INTERMÉDAIRE (Jeffrey)

Correction de la requête qui indique la capture d'un drapeau et netoyage du code.

### CREATION D'UN CONTROLLEUR DU SERVEUR DE SUIVI (Jeffrey)

Écriture d'un script python permettant d'énvoier tout types de requetes accepté par le serveur de suivi à la main.


## 12/12/2024

### PRESENTATION STRATEGIE DE GROUPE (Alice)

Présentation orale avec d'autres membres d'autres équipes.

### NETTOYAGE CODE, FICHIERS, DOCUMENTATION DES FICHIERS (Alice)

Suppression des fichiers inutiles, création du fichier ARCHITECTURE_CODE.md qui répertorie tous les fichiers pythons.

## 14/01/2025

### TRAVAIL SUR STRATÉGIE DE GROUPE (Alice, Jeffrey)

Normalisation des moyen de communiquer les données parmis les robots.
Échange sur le fonctionnement du serveur commun de communication établit par Lothaire.

### DÉBUT D'IMPLEMENTATION DU CODE DE COMMUNICATION AVEC LE SERVEUR COMMUN (Jeffrey)

Écriture du prototype du code qui communique avec les autres robots

### DESIGN DU ROBOT / MODÉLISATION 3D (Edouard)

Choix du design (Seamoth de subnautica) et création de plans / début de la conception du modèle 3D

## 21/02/2025

### FINALISATION DU CODE POUR COMMUNIQUER AVEC LE SERVEUR COMMUN (Jeffrey)

Travail avec Lothaire pour tester la communication entre robot.

### DESIGN DE LA PAGE WEB (Alice)

Ajout d'un fichier CSS à la page web de la raspberry.

### PERFECTION DU CONTRÔLE DES MOTEURS / AMÉLIORATION DES FONCTIONS MOTEURS (Martin)



## 29/01/2025

### FABRICATION DE LA DECORATION DU ROBOT (Martin, Alice)

abandon de la coque 3D par manque de temps. Choix d'une décoration en papier
sur le thème du fond marin.

### CREATION FLYER ROBOT (Martin, Jeffrey)

Il roule droit.

## 30/01/2025


### AJOUT DE DECORATIONs (Alice)

coloriage des revetement en papier, decoupage des algues, collage des algues.

### PEINTURE DES DECORATIONS (Joshua, Edouard, Alice)

Peinture en rouge des algues autour de la camera.

### DEBUG ASSERVISSEMENT MOTEUR (Martin, Jeffrey)

Debug du nouveau code qui retient les ticks de retard (erreur dans le déplacement) d'un déplacement à l'autre.
Le robot accumulait des erreurs en tournant. Le problème a été résolu en autorisant 
les vitesses très basses pour corriger les erreurs.

### CODE POUR ALLER A UNE POSITION (Edouard, Alice)

Nouvelle fonction qui autorise les deplacements ou la distance
selon l'axe x ou y est faible : dans ce cas, le robot avance uniquement
dans une direction en deviant legerement pour parcourir aussi
la distance selon l'autre axe.

### REPERAGE GRACE AUX MARKERS (Jeffrey)

Le robot peut desormais se reperer grâce à un seul marker.

### TESTS STRATEGIE DE GROUPE (Jeffrey, Martin, Alice)

