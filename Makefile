setup:
	pip install -r test-requirements.txt

test:
	flake8 drfutils --exclude=migrations
	PYTHONPATH=. DJANGO_SETTINGS_MODULE=drfutils.tests.settings django-admin migrate
	PYTHONPATH=. DJANGO_SETTINGS_MODULE=drfutils.tests.settings django-admin test

publish:
	git diff --exit-code
	make test
	git tag $(python setup.py --version)
	git push
	git push --tags
	python setup.py sdist bdist_wheel upload
