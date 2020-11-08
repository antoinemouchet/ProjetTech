# Specs

## Backend - API endpoints

- GET  `/list/<id>`  obtenir la watch list  - Jérémie
- POST `/list/<id>`  modifier la watch list - Jérémie

- POST `/shows/`     créer un show                    - Antoine
- GET  `/shows/`     obtenir tous les shows           - Antoine
- GET  `/shows/<id>` obtenir les détails sur un show  - Antoine

- GET  `/recommendations/<id>` obtenir recommendations pour un utilisateur - Jérémie

- POST `/login/`     connexion                         - Sémy
- POST `/logout/`    déconnexion                       - Sémy

- POST `/users/`     créer un utilisateur              - Sémy
- GET  `/users/`     obtenir tous les utilisateurs     - Sémy

- GET   `/session/<token>` obtenir état d'une session  - Vincent
- PATCH `/session/<token>` modifier état d'une session - Vincent
- POST  `/session/`        créer une session           - Vincent

- GET   `/friends/<id>`    obtenir les amis d'un user  - Vincent
- POST  `/friends/<id>`    définir les amis d'un user  - Vincent

## Frontend

- Connection                                                         - Sémy
- Création de compte                                                 - Sémy 

- Ajouter un show                                                    - Antoine
	- Nom
	- Description
	- Photo
	- Fichier (.mp4, .webm)
- Mes séries (Afficher ma liste et la modifier)                      - Jérémie
	- Un tableau avec logo/nom et lien pour créer une watch party
	- Supprimer série
	- Mettre à vu/en cours
	- Champs pour ajouter une série
- Détail sur série                                                   - Antoine
- Listes d'amis                                                      - Vincent
	- Un tableau avec pseudo et lien pour comparer les listes
	- Supprimer ami
	- Champs pour ajouter un ami
- Comparer deux listes d'utilisateurs                                - Jérémie
- Salon pour visionner vidéo                                         - Vincent
	- Menu d'outils (pause/play/aller à)
	
## Base de données

### Utilisateur

id: autoincrement int
pseudo: text
password: text
ami: foreign key -> Utilisateur.id

### Show

id: autoincrement int
nom: text
description: text
img: text
file: text
tags: text ("violence;adventure")

### Amitié

id: autoincrement int
user_a: foreign key -> Utilisateur.id
user_b: foreign key -> Utilisateur.id

### WatchParty

id: autoincrement string
time: float
state: bool

### WatchPartyParameters

id: foreign key -> WatchParty.id
type: text ("white", "black")

### WatchPartyBlackList

id: autoincrement int
parameters: foreign key -> WatchPartyParameters.id
user: foreign key -> Utilisateur.id

### WatchList

id: autoincrement int
show: foreign key -> Show.id
user: foreign key -> Utilisateur.id
status: text

## Technos

https://kylelogue.github.io/mustard-ui/index.html
