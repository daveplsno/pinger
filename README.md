pingerspingerspingerspingers

```
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```

```
python manage.py runserver 0.0.0.0:10000
python manage.py createsuperuser --user blender
python manage.py makemigrations
python manage.py migrate
```