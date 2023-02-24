clean:
	@rm -f dist/*
	@find . -name '*.pyc' -or -name '*.pyo' -or -name '__pycache__' -type f -delete
	@find . -type d -empty -delete

dist: clean
	@python3 ./setup.py sdist bdist_wheel

init:
	@pip3 install -r requirements.txt

dev:
	@pip3 list --format=freeze > requirements.txt

lint:
	@flake8

set-source:
	@pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple