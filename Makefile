PWD=$(shell pwd)

all: build deploy clean gh

test:
	watch -c "pytest --color=yes --last-failed --no-header"
build:
	@PYTHONPATH=$(PWD)/bin build.py
deploy:
	@rsync-deploy
clean:
	@clean
gh:
	@push
