usage:
	@echo "make venv"

venv:
	@virtualenv --no-site-package venv
	@source venv/bin/activate && pip install -r requirements.txt
