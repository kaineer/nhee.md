all: build deploy clean gh

test:
	watch -c "pytest --color=yes --last-failed --no-header"
build:
	build.py
deploy:
	rsync-deploy
clean:
	clean

gh:
	push
