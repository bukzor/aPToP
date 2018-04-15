
bin/venv-update:
	curl -o $@ https://raw.githubusercontent.com/Yelp/venv-update/v3.0.0/venv_update.py
	chmod 755 $@

venv: requirements.txt bin/venv-update
	./bin/venv-update venv= --prompt '(aPToP)' -ppython3 venv


