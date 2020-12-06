# Weebinator

Ce repository contient le code source de l'application web développée dans le cadre du cours de Technologies Web. Ce projet a donc pour objectif de tester nos capacités et notre utilisation des technologies, en préférant celles vues dans le cadre du cours sans en exclure d'autre (Flask, Jinja2, JavaScript, HTML, CSS, Ajax, normes REST API).

## Objectif et principe 

Qui n’a jamais voulu partager ses séries, films et animés préférés avec ses amis ? Weebinator répond à ce problème d’une manière simple et pratique. Modifier votre watch list en ligne en puisant dans la base de données d’œuvres enregistrées. De plus, des fonctionnalités pour comparer sa watch list avec ses amis sont présentes, permettant ainsi de découvrir en quelques secondes ce qu’il vous reste à voir pour être à jour. Une fois que vous êtes à jour ? Continuez à avancer ENSEMBLE ! Grâce à la fonctionnalité watch party, visionnez ensemble des films. L’état de lecture et le temps actuel sont synchronisés sur toutes les machines. Rien de plus facile en cette période de vide social, ajoutez votre épisode au format mp4 ou webm sur la plateforme, ajoutez-le à votre watch list et créer une watch party. Vous recevez un code unique à partager avec vos amis. Et c’est parti !

## Informations légales

Ce projet a été développé dans le but de **tester nos capacités**. 

S'il venait à être déployé, il est important de noter que nous déclinons toute responsabilité pour le contenu mis en ligne.

## **Requirements**
* python 3.7 ([get it here](https://www.python.org/downloads/))
* pip
* miniconda (*or anaconda*) ([download available here](https://docs.conda.io/en/latest/miniconda.html))

## **Setup**
1. Clone the repository
2. Open a shell/command prompt
3. Use the following commands in the directory

```
conda env create -f environment.yml
```
```
pip install -r requirements.txt
```

### Note
Those commands set up an isolated environment and download the required packages for the application so that it does not mess up with other existing versions of python and packages.

## **Launch**
If you have done everything right, you should be ready to launch the app.

Just a few more commands to type in the shell in the same directory as the main.py file.

First, you have to activate the conda environment you just created
```
conda activate [environmentName]
```

### Warning
This may vary depending on your OS.

### Windows
#### **Powershell**
```ps
$env:FLASK_APP=./main.py 
flask run
```
#### **Command prompt**
```cmd
set FLASK_APP=main.py
flask run
```

### UNIX
```bash
export FLASK_APP=main.py
flask run
```


## **How to use ?**
See the application on ```localhost:5000```

### _Create a new account_
* Press Register and fill in the boxes
* Press Submit
  
### _Log In_
* Enter your username and password
* Press Submit

### _Manage your friends_
* Click on "Friends" in the navigation bar.

### _Add a show_
* Click on "Shows List" in the navigation bar
* Press the "New" button in the top right corner
* Fill in the form
* Press Submit

### _See detail of a show_
* Press the "Details" button next to the corresponding show.

### _Add a show to your watchlist_
* Click on "Watch List" in the navigation bar
* Enter the name of the show to add in the text box at the bottom.
* Press "Add Show"

### _Get recommendations_
* Click on "Recommendations" in the navigation bar.

### _Compare your watch list with a friend_
* Click on "Compare Lists" in the navigation bar
* Enter the pseudo of the friend with whom you want to compare

### _Create a watch party_
* Add the show to your watch list.
* Click on its name in your watch list.

### _Join a watch party_
* Click on "Watch Party" in the navigation bar.
* Enter the tag which is after the watch in the URL of the watch party.