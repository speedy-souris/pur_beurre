# Moteur de recherche de substituts alimentaires via OpenFoodFacts
## Description
```
Application permettant de trouver des produits de substitution 
plus sains en se basant sur le Nutri-Score. 
Le projet interagit avec l'API publique d'OpenFoodFacts
 pour extraire et comparer les données nutritionnelles.
```
## Périmètre du test :
```
Pour les besoins de la démonstration et des tests de performance, 
le projet se limite actuellement à un jeu de données de 1 000 produits, 
segmentés en 10 catégories majeures:
'pâtes alimentaires de céréales', 'boissons', 'mélanges de légumes frais',
'fruits secs', 'poissons', 'biscottes', 'pâtisseries', 'fromages',
'charcuteries', 'confitures'

```
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
## IV. Parcours Utilisateur
### 1. Connexion en ligne 
```
Dans le navigateur renseigner l'adresse suivante
https://nom_du_projet.onrender.com

Chaque page se compose des parties suivantes :
    - Bandeau de Navigation Superieur de Gauche à Droite
        - Icône De retour à l'Accueil => lien page d'accueil
        - Barre de recherche (Produit Recherché)
        - Icône de Profil Connecté / Déconnecté => lien page profil
        - Icône des produits Favoris (Carotte) => lien page des produits favoris
        - Icône de Déconnexion => deconnexion et lien retour page d'accueil
    - Partie Centrale differe sur chaque page
    - Pied de page (footer)
        - Bouton des Mentions Légales => lien page mentions légales
        - Bouton pour Formulaire de contact => lien page de contact
```
### 2. la page d'Accueil
```
- Formulaire de recherche (Peoduit Recherchés)    
````
### 3. la page Produit Trouvés
```
- Affichage du produit recherché 
- Affichage des produits de substitutions sur 3 colonnes et sur 2 lignes Par page
```
### 4. la page Produits favoris
```
- Affichage des produits Favoris sur 3 colonnes et sur 2 lignes Par page
```
### 5. la page détail produit
```
Chaque photo des produits sert de lien pour cette page
- Informations Nutritionnells du produit pour 100 gr
- lien page produit OpenFoodFact    
```