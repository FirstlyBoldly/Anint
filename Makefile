.PHONY: init upgrade test flake8 mypy black publish distclean

init:
	python -m pip install -r requirements.txt

upgrade:
	python -m pip install --upgrade anint

test:
	python -m pytest $(flags) tests

flake8:
	python -m flake8 src

mypy:
	python -m mypy src

black:
	python -m black src

publish:
	python -m pip install --upgrade twine
	python -m twine upload dist/*
	rm -fr dist src/anint.egg-info

distclean:
	rm -fr dist src/anint.egg-info
