# o'zgaruvchilar
ENV_DIR=env
PYTHON=$(ENV_DIR)/bin/python
PIP=$(ENV_DIR)/bin/pip
MANAGE=$(PYTHON) manage.py
HOST=localhost
PORT=8000


# .env file yaratish
envfile:
	cp .env.example .env

# virtualmuhitni yaratish va unga requirements/base.txt kutubxonalarni yuklab active qilish
activate:
	virtualenv $(ENV_DIR)
	$(PIP) install -r requirements/base.txt

# migratsiya amalini bajarish
migrate:
	$(MANAGE) makemigrations
	$(MANAGE) migrate

# static filelarni bitta joyga jamlash
collectstatic:
	$(MANAGE) collectstatic --noinput

# projectni ishga tushirish
runserver:
	$(MANAGE) runserver $(HOST):$(PORT)

# yangi superuser yaratish
createuser:
	$(MANAGE) createsuperuser