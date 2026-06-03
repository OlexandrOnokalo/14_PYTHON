# Create Project
```
python --version
```

## Сeate venv - віртуальне середоще для вашого проекту і пакетів
```
py -m venv .venv
python -m venv .venv
python3 -m venv .venv
```

# Activate venv
```
.venv\Scripts\activate.bat
```
# оновлення pip
```
python.exe -m pip install --upgrade pip
```
# установка джанго
```
py -m pip install Django

py

>>>import django
>>>print(django.get_version())
>>>quit()

python -m django --version
mrdir silpo
```
# створюємо проект в папці сільпо
```

django-admin startproject mysite silpo 
cd silpo
```
# запуск сервака
```
py manage.py runserver 9581 
```
# ставим бібліотеку постгрес в наш венв
```
pip install psycopg2-binary
py manage.py migrate
```
## Перегляд списку бібліотек їх збереження та клонування проекту
```
pip freeze
pip freeze > requirements.txt
```
## Додаю superuser
```
python manage.py createsuperuser
py manage.py createsuperuser
admin
123456
py manage.py runserver 9581
```

## Working users Custom Django
```
py manage.py startapp users
pip install Pillow 
py manage.py makemigrations users
py manage.py migrate
```
