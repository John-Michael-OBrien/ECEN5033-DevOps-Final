# Monte Carlo Pi Solver
To run this, you'll need to spawn two services, build a set of images, and then apply 3 deployments.

There are two ways you can do it: the easy way, and the hard way, and easy startup tools are provided for both local and Google's GKE system.

## The Easy Way
### Starting things Locally
If you've got minikube running, or have already started a multi-node cluster and have access credentials (see below for how,) then **all
you'll need to do is navigate to the app folder and run `start-local`**. This will prompt you for what repo you want to write to, and what
image version tag you want to use (make sure to pick a unique one or roll-outs won't work) and you'll be off to the races.

### Starting Things on Google
#### Connecting to GKE
If you've already initialized your GKE credentials, you can skip this first part.
* Start by making a GKE cluster called `devops-final`. You can read more about how to do this on [Google's GKE support site](https://cloud.google.com/kubernetes-engine/docs/how-to/creating-a-cluster).
* Next, [make sure you've installed the Google Cloud SDK on your system](https://cloud.google.com/sdk/docs/downloads-apt-get).
* After that, navigate to the app folder and run `init-google`. This will call the three commands required to initialize the Google Cloud Engine on your system. Just follow the prompts to get your credentials setup and get kubectl connected to your cluster.
* Finally, run `start-google` to get the web service up and running.

## The Hard Way
If you want to start everything by hand we'll have to do a few extra steps.

### Starting the Cluster on Google
Since most of the work for Google is getting the cluster setup, this isn't appreciably harder. 

* Start by making a GKE cluster. Again, you can read more about how to do this on [Google's GKE support site](https://cloud.google.com/kubernetes-engine/docs/how-to/creating-a-cluster).
* Next, [make sure you've installed the Google Cloud SDK on your system](https://cloud.google.com/sdk/docs/downloads-apt-get). 
* Moving on, you'll need to initialize the project and project SDK configuration on your system. Run `gcloud init`, and follow the prompts to point the SDK at your GKE project.
* After that, you'll need to configure your docker to handle the Google docker repo. Run `gcloud auth configure-docker`. This will encode the Google endpoints and the associated authorization info into your docker config.
* Next, you'll need to configure your kubectl to talk to the GKE cluster. To do this, you'll need to run `gcloud container clusters get-credentials <cluster name>`. After this point, you can use kubectl just like you would with a local cluster.

### Starting the Web Service
If you're using GKE or are working from a local Minikube or multi-node cluster, the next steps are approximately the same. Start by spinning the DB and web app services, and starting the DB server.

```
kubectl apply -f redis-service.yml
kubectl apply -f [controller-service.yml | controller-service-google.yml]
kubectl apply -f redis-deploy.yml
```

Use `controller-service.yml` when deploying to generic Kubernetes clusters. Use `controller-service-google.yml`
if you are deploying to Google's GKE as this will allocate a proper external IP and the necessary load balancer. 

After that, we need to build the web service and publish it to the repo. To do this run :

```
REPO=<Repo Server and Port> BUILDVERSION=<version number> make -B
```

Once that's done, you just need to deploy our workers and web service. Tell kubectl to get them up and running (or roll-out an update if that's more appropriate.)

```
kubectl apply -f controller-deploy.yml
kubectl apply -f solver-deploy.yml
```

Thanks to Kubernetes' internal service mapping, no additional configuration is necessary. If you're using GKE, the only
additional configuration necessary is looking at what IP GKE's load balancer was assigned.

## Allocating a Local Multi-Node Cluster
Also included are the necessary items to fully instantiate a 4 node cluster. To accomplish this:
* `vagrant up` on your Vagrant host.
* Grab a cup of coffee.
* Log in to `10.10.77.2` using vagrant's SSH tools.
* Use `sudo su` to switch over to root
* Change into the  `/vagrant` folder
* Execute `./buildcluster` to build the Kubernetes cluster.
* Get another cup of coffee.
* Change into the `/vagrant/dockerreg` folder
* (Optional) Execute `ansible-playbook -i ../jmcluster/hosts.ini install_registry.yml` to create the local registry and add it to the security exceptions (***DON'T DO THIS IN PRODUCTION!***)

From here, the root user will have all of the necessary settings to control the kubernetes cluster.