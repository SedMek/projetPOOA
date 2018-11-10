# Le projet hébégé:

Il est possible d'utiliser la version hébergée en ligne : http://projet-pooa-v0.herokuapp.com

Une fois sur notre site, vous pouvez soit créer un compte utilisateur ou utilisez les coordonnées du compte 
ci-dessous que nous avons créé pour les démonstrations et accéder directement.
* email: py17pooa@gmail.com 
* password: pooapy17

Vous pouvez utiliser la même adresse et le même mot de passe pour accéder au compte gmail si vous voulez essayer la fonctionnalité du mot de passe oublié. 

------------------------------------------------------------------------------------------------------------
# Le projet en local:

**Pour faire tourner le projet en local:

1) Utiliser Python 3.5 ou plus

2) Installer les bibliothèques dans requirements.txt du dossier du projet : pip install -r chemin/vers/requirements.txt

3) Télécharger Mongodb : https://docs.mongodb.com/manual/installation/ (Pour windows vaut mieux télécharger l'exécutable MSI et pas le ZIP)

4) Lancer l'application mongod dans le dossier (pas mongo ou mongos). Ce lancement est nécessaire pour soumettre les données du login et lancer le site, sinon une page de login statique sera affichée et rien ne se passe.

5) Lancer le script vues.py dans le dossier du projet, il permet de créer le serveur du site en localhost

6) Aller dans un navigateur web (on recommande Mozilla Firefox avec navigation privée (ctrl + shift +P)) 

7) Accéder à http://127.0.0.1:5000

8) Assurez-vous que vous avez lancez le service mongod (point 4) sinon tout ce que vous aurez est la page de login sans pouvoir créer un compte et se connecter

9) Créez un compte et accédez au site 

------------------------------------------------------------------------------------------------------------

# Fonctionnalités:
En utilisant notre site, vous pouvez:
1) sign-in / login: 
- créer un compte personnel en utilisant un email et un mot de passe
- vous connecter avec un compte déjà créé
- vous déconnecter
- recevoir par email un nouveau mot de passe si vous avez oublié le votre.
2) home:
- chercher des séries
- rajouter une série à votre liste de séries favorites
- retirer une série de votre liste de séries favorites
- voir les information globale d'une série favorie
- voir les informations de chaque saison des séries favorites
- supprimer toutes vos séries favorites
- voir la durée totale des séries favorites
3) Notifications:
- recevoir des notifications sur le site dès qu'un nouvel épisode d'une série favorie est sorti (Pour des raisons de démonstration, nous avons mis du code en dur pour afficher des exemples de notification)
- recevoi par email une notification dès qu'un nouvel épisode d'une série favorie est sorti
4) Settings:
- modifier votre mot de passe
- gérer les notifications que vous voulez recevoir

------------------------------------------------------------------------------------------------------------
Bonne navigation :)
------------------------------------------------------------------------------------------------------------
