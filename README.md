# Installation du projet pur_beurre sur PC équipé de linux a partir de github 
Dans un terminal (console pour ligne de commande)
créer un environement virtuel avec la commande :
```shell
python3 -m venv env
```

activer l'environement virtuel avec la commande :

```shell
source env/bin/activate
```

installer git avec la commande : (hors de l`environnement virtuel)

```shell
git init
```

ensuite taper la commande :
```shell
git clone https://github.com/YOUR_USER_NAME/projet_purBeurre.git pour une connexion HTTPS
 ```
ou

```shell
git clone git@github.com:YOUR_USER_NALE/projet_purBeurre.git pour une connexion SSH
```

dans un terminal (hors de l'environnement virtuel) installer le serveur de la base de données POSTGRESQL avec les commandes suivantes :
(commandes dans un environnement "DEBIAN")
```shell
sudo apt update # (pour mettre a jour la liste des dépots de linux)
```
```shell
sudo apt install postgresql
```