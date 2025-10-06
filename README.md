# Installation du projet pur_beurre sur PC équipé de linux a partir de github
## I. Créé un environnement de travail pour ce projet
Dans un terminal (console pour ligne de commande)
créer un environement virtuel avec la commande :
```shell
python3 -m venv env
```

Dans le répertoire de l'environnement virtuel, activer l'environement virtuel avec la commande :

```shell
source env/bin/activate
```
ou
```shell
. env/bin/activate
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
sudo apt install postgresql
```

demarrer le shell postgresql
```shell
sudo -u postgres psql
```

dans le terminal postgres# 
creer un utilisateur et une base de données
```shell
CREATE USER nom_utilisateur WITH SUPERUSER CREATEDB PASSWORD 'mot_de_passe';
CREATE DATABASE nom_bd WITH OWNER = nom_utilisateur;
\du # controle utilisateur
\l # controle base de donnée
\q # quitter le shell postgres
```

dans le terminal Django 
dans l'environement virtuel 
creer un administrateur pour la base de données
```shell
python manage.py createsuperuser
```
## II. Création de la base donnée de deux manières distincts
### 1. Initialisé chaque commande dans l'ordre
```shell
# 1. Effacer les anciennes données
python manage.py delete_all_data

# 2. Effacer le repertoire image_product avec toutes les anciennes images produits
python manage.py delete_image_dir

# 3. Creation de la nouvelle base de données de produits
python manage.py create_product

# 4. Creation du nouveau répertoire image_product avec les nouvelles images de chaque produit
python manage.py image_product
```
### 2. Initialisé une unique commande
```shell
# 1. Réalise toutes les commandes de la méthode 1 dans l'ordre
python manage.py full_import
```
