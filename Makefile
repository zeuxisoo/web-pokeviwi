.PHONY: venv

usage:
	@echo "make venv"

venv:
	@virtualenv --no-site-package venv
	@source venv/bin/activate && pip install -r requirements.txt

	@npm install

server:
	@source venv/bin/activate && python manager.py runserver

dev-assets:
	@npm run dev
