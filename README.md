# pinger

it pings, it records, it doens't do anything else, eventually it might also graph.

thinken basic steps to get dev env setup is (to be tested lmao):

1) clone repo
2) create .env file in pinger_server (referenced in compose file)
```
MYSQL_DATABASE=nameofdatabase
MYSQL_USER=nameofmysqluser
MYSQL_PASSWORD=passwordformysqluser
MYSQL_ROOT_PASSWORD=passwordformysqlrootuser
```
3) create .env file in pinger_server/data/pinger_server (referenced in settings.py)
``` 
SECRET_KEY=someverylongsecretkeyfordjangoprojectwewlad
DBNAME=nameofdatabase
DBUSER=nameofmysqluser
DBPASS=passwordformysqluser
```
5) navigate back to project root and compose up
```
docker-compose up --build -d
```
3) enter container
```
docker exec -it pinger_server bash
```
5) migrate db
```
python manage.py migrate
```
5) create superuser
```
python manage.py createsuperuser
```
6) log into admin page, generate token for admin
7) create .env file in pinger_client (referenced in compose file)
```
PINGERTOKEN=thetokenfromdjangoadminpage
```
8) probably good idea to take ownership of all the newly created files by root user (thx docker). from the project root run
```
sudo chown -R $USER:$USER .
```

unfortunately the api url for targets and db posts is currently hardcoded in the pinger_client container, so yeah not much can be done here until i change it, i'll eventually pass this as a container env the same as the token so ppl can use their own local server. much work to be done.
