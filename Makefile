install:
	python -m pip install --upgrade pip && pip install -r requirements.txt

build:
	pyinstaller -w -F --add-data "templates:templates" --add-data "static:static" app.py