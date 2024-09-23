#								 Suivi du projet


*Texte en italique*
_Texte en italique_
**Texte en gras**
__Texte en gras__
***Texte en italique et en gras***
___Texte en italique et en gras___
~~Ce texte est barré.~~ mais pas celui-là.

## 23/09/2024:
Installation de l’OS sur la Raspberry Pi

e nom **de** notre raspberry est “strawberry”. Le mot de passe est “raspberry”.


utiliser le github


### Connecter les appareils au routeur

raspbery pi connecté en filiaire au serveur tp-link
pour connecter un ordinateur au routeur sans fil : 
se connecter par wifi au routeur:
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
Cela nous donne une liste de 4 appareils. On ping chacune en débranchant puis rebranchant notre raspberry pour identifier la bonne adresse IP. On trouve que notre raspberry a l’adresse IP 192.168.0.114

### Se connecter en ssh à la raspberry

