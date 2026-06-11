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
	git add .
	git commit -m "Dump current state"
	git push origin master
