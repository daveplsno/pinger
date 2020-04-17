# collector.py

this needs a token before it'll work

i am the token master

once you have a token, pass token to container thru env var

suggest to pass from .env file like:

```
PINGERTOKEN=dfds,mfjnkjewjfoi342jroioifje98fjewoifejioufjew98fh98w4eru4398ru984j
```

and compose like:

```
version: "3"
services:

  pinger:
    restart: unless-stopped
    image: daveplsno/pinger:0.1
    container_name: pinger
    environment:
      PINGERTOKEN: ${PINGERTOKEN}

```

results get stored in my db

i am the db master

eventually when a front end exists things will be nicer n i will let u 

- create your own user
- get your own token
- setup your own targets, 
- actually view your results on a dashboard