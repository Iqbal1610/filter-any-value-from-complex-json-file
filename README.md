# filter-any-value-from-complex-json-file
In this repository we will create a FastApi endpoint to parse json file and search any key-value pair from that json by passing parameterised value to API endpoint. After that we will deploy this application on local kubernetes cluster(minikube or docker-desktop) with nginx-ingress controller proxy to make it accessible form outside of the kubernetes host with rate-limit features to check/prevent DDOS attack.

## Step by step process

### Pre-requisite
- Install Docker-desktop or Minikube 
- Install Python and FastApi
- Kubectl,helm,helmfile

### Backend Api development using FastApi
In the **app** directory, the fastapi project resources are available. There is only one API is configured here for dynamic parameterized key-value pair search in any complex json file. We can pass any json file and search any key-value by using the API endpoints.

The application is Dockerized via **Dockerfile** and exposed on port **8080**

We need to build docker image by this Dockerfile via below command

```
docker build --no-cache -t test-image-build:v1 ./app
```
Now we have the docker image in our local machine which will be used during the application deployment via helm-chart.

### Create helm-chart for API application deployment
In this section we created a helm-chart name **demo-app**, where you will find 3 kubernetes resources 
- **deployment.yaml**: manifest file for deploy the API application with docker-image **test-image-build:v1** which is build in previous step.
- **service.yaml**: The application is exposed in the cluster by this service manifest via **NodePort** as this service will be accessible from other host via nginx-ingress.
- **ingress.yaml** : This ingress resource is needed to access the API service from the out-side of kubernetes host. We are using nginx-ingress controller as a proxy to expose the service to out-side of the host.Here we configure **request-per-second** features to make the rate-limit functionality test for the API endpoint for preventing DDOS.

### Nginx-controller deployment 
We will use bitnami helm-chart to deploy nginx-ingress-controller as proxy infront of the kubernetes-cluster.

We can deploy this chart by below command
```
kubectl config set-context docker-desktop 
helm install nginx-ingress-release oci://registry-1.docker.io/bitnamicharts/nginx-ingress-controller
```
Check nginx deployment via kubectl 

```
kubectl get all | grep "nginx"
```

### Application deployment on Docker-desktop/minikube

Now we have all things(docker image,helm-chart,proxy) are ready for final application deployment.

We will deploy our helm-chart via helmfile by below command

```
kubectl config set-context docker-desktop
cd deployment
helmfile sync
```
Check application deployment via kubectl 

```
kubectl get ingress,all -n test-app
```
You will see all resources are deployed as expected and the endpoint will be accessible via **http://localhost/uploadfile/** this url by providing json file path with searching parameter.

### Test the API with jsonfile and search parameter

We have created a **run.sh** script to call the API via curl command and pass json file and search key as parameter.

We can export our file path and search key via 
```
export FILE_PATH=./devops_interview_terraform_state.json
export SEARCH_PARAMETER=source_security_group_id

./run.sh
```
Now you will see all key-value matched with **source_security_group_id** inside the given json file.

You will see only 10 search results and another 10 result will give 503 error from the run.sh script. It's happened due to the **request-per-second** [rate-limit](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/#rate-limiting) is setup on the ingress.yaml as 2. It will be multiplied by default brust  limit value 5, So number of allowed request per second for the localhost is 10. Thats why we see only 10 search result and others request give 503.
