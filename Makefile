all: build deploy clean

test:
	watch -c "pytest --color=yes --last-failed --no-header"
build:
	build.py
deploy:
	deploy
clean:
	clean

gh:
	git add .
	git commit -m "State at $(date +%Y.%m.%d -- %H:%M)"
	git push origin master
