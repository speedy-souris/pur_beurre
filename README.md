# Installation du projet pur_beurre sur PC équipé de linux a partir de github
## I. Créé un environnement de travail pour ce projet
Dans un terminal (console pour ligne de commande)
créer un environnement virtuel avec la commande :
```shell
python3 -m venv env
```

Dans le répertoire de l'environnement virtuel, activer l'environnement virtuel avec la commande :

```shell
source env/bin/activate
```
ou
```shell
. env/bin/activate
```

Installer git avec la commande : (hors de l`environnement virtuel)

```shell
git init
```

Ensuite taper la commande :
```shell
git clone https://github.com/YOUR_USER_NAME/projet_purBeurre.git pour une connexion HTTPS
```
ou
```shell
git clone git@github.com:YOUR_USER_NALE/projet_purBeurre.git pour une connexion SSH
```

Dans un terminal (hors de l'environnement virtuel) installer le serveur de la base de données POSTGRESQL avec les commandes suivantes :
(commandes dans un environnement "DEBIAN")
```shell
sudo apt update # (pour mettre a jour la liste des dépots de linux)
sudo apt install postgresql
```

Démarrer le shell postgresql
```shell
sudo -u postgres psql
```

Dans le terminal postgres# 
créer un utilisateur et une base de données
```shell
CREATE USER nom_utilisateur WITH SUPERUSER CREATEDB PASSWORD 'mot_de_passe';
CREATE DATABASE nom_bd WITH OWNER = nom_utilisateur;
\du # contrôle utilisateur
\l # contrôle base de donnée
\q # quitter le shell postgres
```

dans le terminal Django 
dans l'environnement virtuel 
créer un administrateur pour la base de données
```shell
python manage.py createsuperuser
```
## II. Création de la base donnée de deux manières distincts
### 1. Initialisé chaque commande dans l'ordre
```shell
# 1. Delete old data
python manage.py delete_all_data

# 2. Delete the image_product directory with all old product images
python manage.py delete_image_dir

# 3. Creation of the new product database
python manage.py create_product

# 4. Creation of the new image_product directory with the new images for each product
python manage.py image_product
```
### 2. Initialisé une unique commande
```shell
# 1. Perform all commands in method 1 in order.
python manage.py full_import
```
## III. Déploiement du projet sur Render
### 1. Connexion sur Render
```
Dans le navigateur renseigner l'adresse suivante :
https://dashboard.render.com/login
Pour se connecter utiliser les comptes suivant
Github / Gitlab / Bitbucket / Google
```
### 2. Création du projet
```
Dans Projet
    - Ajouter Postgres (+ New)
        - Donner un nom à l'instance prostgresql
        - Donner un nom à la base de données
        - Donner un nom d'utilisateur
        - Datadog Region = EU
        - Instance Type : Gratuit / Payant
    - Ajouter Web Service (+ New)
        - Ajouter code Source : Git Provider (Projet github)
            - changer la branche (main / dev)
            - Build Command = $ pip install -r requirements.txt
            - start Command = $ gunicorn ton_application.wsgi
            - Type d'instance : Gratuit / Payant
        - Variables d'Environnement
            - SECRET_KEY= génération de clé sur Render
            - Ajout de .env
                - DATABASE_URL=Connexion URL Interne
                - DEBUG=False

```         