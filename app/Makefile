#!make
.PHONY: all clean controller solver

all: controller-deploy.yml solver-deploy.yml controller solver

%-deploy.yml: %-deploy.yml.tmpl
	envsubst < $< > $@

%-job.yml: %-job.yml.tmpl
	envsubst < $< > $@

controller:
	${MAKE} -C controller

solver:
	${MAKE} -C solver

clean:
	-rm -f controller-deploy.yml solver-deploy.yml
	${MAKE} -C controller clean
	${MAKE} -C solver clean
