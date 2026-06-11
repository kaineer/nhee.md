all: build deploy clean gh

test:
	watch -c "pytest --color=yes --last-failed --no-header"
build:
	build.py
deploy:
	deploy
clean:
	clean

gh:
	push
