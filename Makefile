test:
	watch -c "pytest --color=yes --last-failed --no-header"
build:
	build.py
