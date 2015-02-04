.PHONY: develop flake8 test coverage

develop:
	pip install -r requirements_dev.txt

flake8:
	flake8 beagle tests

test:
	DJANGO_SETTINGS_MODULE=tests.settings django-admin.py test tests

coverage:
	coverage erase
	DJANGO_SETTINGS_MODULE=tests.settings coverage run --branch --source=beagle `which django-admin.py` test tests
	coverage html
