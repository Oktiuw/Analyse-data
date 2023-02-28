
## Exécuter l’application pour le développement :

1. Créer un environnement Flask : 
`$ python -m venv env`

2. Création du fichier /app/.env avec les lignes suivante :
```py
# .env
FLASK_APP=app/appdev.py
FLASK_DEBUG=1
```

3. Pour lancer l'environnement :  
```shell
~/Flask $ source env_flask/bin/activate
```

4. Installer les requirements : 
```shell
(env_flask) ~/Flask $ pip install –r requirements.txt
```

5. Pour lancer le server Web de dev Flask :
```
(env_flask) ~/Flask $ flask run
```

## Mettre à jour l'application Web en production :
```shell
~/ $ service apache2 reload
```