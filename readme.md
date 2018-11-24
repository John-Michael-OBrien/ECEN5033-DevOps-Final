# Monte Carlo Pi Solver
To run this, you'll need to spawn two services, build a set of images, and then apply 3 deployments.
To do this, use:
```
kubectl apply -f redis-service.yml
kubectl apply -f [controller-service.yml | controller-service-google.yml]
kubectl apply -f redis-deploy.yml
```

Use `controller-service.yml` when deploying to generic Kubernetes clusters. Use `controller-service-google.yml`
if you are deploying to Google's GKE as this will allocate a proper external IP and the necessary load balancer. 

To build the service use:
```
REPO=<Repo Server and Port> BUILDVERSION=<version number> make -B
```

And then finally:
```
kubectl apply -f controller-deploy.yml
kubectl apply -f solver-deploy.yml
```

Thanks to Kubernetes' internal service mapping, no additional configuration is necessary. If using GKE, the only
additional configuration necessary is looking at what IP GKE's load balancer was assigned.

## Allocating a local multi-node cluster
Also included are the necessary items to fully instantiate a 4 node cluster. To accomplish this:
* `vagrant up` on your Vagrant host.
* Grab a cup of coffee.
* Log in to `10.10.77.2` using vagrant's SSH tools.
* Use `sudo su` to switch over to root
* Change into the  `/vagrant` folder
* Execute `./buildcluster` to build the Kubernetes cluster.
* Get another cup of coffee.
* Change into the `/vagrant/dockerreg` folder
* Execute `ansible-playbook -i ../jmcluster/hosts.ini install_registry.yml` to create the local registry and add it to the security exceptions (***DON'T DO THIS IN PRODUCTION!***)

From here, the root user will have all of the necessary settings to control the kubernetes cluster.