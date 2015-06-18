.DEFAULT_GOAL := tests

clean:
	git clean -Xdf
	rm -rf build/ dist/

setup:
	pip install -e .
	pip install -r requirements-dev.txt

tests:
	py.test

build-docs: docs/*.rst
	make -C docs/ html

serve-docs:
	killall "python -m SimpleHTTPServer" || true
	cd docs/_build; python -m SimpleHTTPServer&
	cd ../..
	open http://localhost:8000/html/