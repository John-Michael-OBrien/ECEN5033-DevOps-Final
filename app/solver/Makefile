REPO ?= 10.10.77.2:5000
BUILDVERSION ?= 1.0

.PHONY: push container clean

all: container push

container: Dockerfile app.py requirements.txt
	docker build --network=host -t ${REPO}/pi-solver:${BUILDVERSION} -t ${REPO}/pi-solver:latest .

push:
	docker push ${REPO}/pi-solver:${BUILDVERSION}
	docker push ${REPO}/pi-solver:latest

clean:
	-docker rmi ${REPO}/pi-solver
