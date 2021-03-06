# flask-postgres-replica
Sample Flask App Simulating Postgres Replication

## Infra Directories/Files
* k8-setup -> Kustomization files for flask app
* terraform-> Terraform files
* cloudbuild.yaml-> CI file
* config.py -> Main configuration
* wsgi.py -> app startup file
* Dockerfile -> important information about how the app is packaged
* app/routes.py -> key routes used for testing replication
* postgres/data/iso-3166.sql -> country test data
* postgres/data/todo.sql -> todo schema


## Installation
Make sure you have python3 installed.  
* pip3 -r requirements.txt

## Running the App
* gunicorn -c gunicorn.config.py wsgi:app
* runs on port 5000


## Key Routes

* todo sample structure: {"task":"do the dishes"}
* GET /todo/<id> - get todo in write database
* GET /todo   - get all todos in write database
* GET /todo_replica/<id>   - get todo in read database
* GET /todo_replica   - get all todos in read database
* POST /todo - create todo in write database, will get copied to read database
* GET /   - get todo form

App uses basic AUTH on all /todo (including / ) endpoints.

* ex: curl --location --request GET 'http://localhost:5000/todo' -- header 'Authorization: Basic base64string=='

* GET /status - health check endpoint

## Key ENV Variables - must be set for app to work

* POSTGRES_MAIN_HOST - write postgres host
* POSTGRES_REPLICATION_HOST - read postgres host
* POSTGRES_MAIN_PASSWORD - postgres database password
* BASIC_AUTH_USERNAME - basic auth username
* BASIC_AUTH_PASSWORD - basic auth password

## Overview

We are using terraform to spin up our VPC, subnets, service accounts and k8 cluster.
A gcp bucket keeps track of the state and we rely on terraform's free UI service, to keep
track of previous runs.

We are also using argocd to spin up our flask app within our k8 cluster.
Argocd is using Kustomization files to apply the changes.

Cloudbuild handles running the CI portion of the app by building the flask app's
docker image and storing it in gcr.

Helm is used to create our Postgres Stateful replica set.

The k8 cluster is running in a private subnet and can hit the internet via our
nat gateway.

## TradeOffs

We initially tried using google secret manager and injecting secrets in memory
at run time.  However, the doit binary installed in the docker image, which does the translation,  assumes our service only runs via pid one.  This approach won't work because we use a gunicorn server to run our flask app. Gunicorn spins up our flask app on multiple pids.  

It came down to a tradeoff between dynamic passwords and the stability of the app.

We used load balancers instead of an ingresses controller because we don't have a domain registered for this app and can't use a domain header to parse traffic.

Finally, no memory or cpu limits are specified for the flask app, because our cluster uses small VMs and we want the pod to be scheduled.
## DoIt Binary for Translating passwords stored in Google Secrets Manager

A binary used to translate google secrets in memory at run time.

One would specify the secret path as an environment variable and that path
would get translated to its actual value during runtime.

* ex: MY_DB_PASSWORD=gcp:secretmanager:projects/$PROJECT_ID/secrets/mydbpassword

* https://github.com/doitintl/secrets-init


## ArgoCD
Our k8 deployment tool.

* https://argoproj.github.io/argo-cd/getting_started/


## Make new flask app image
git push origin main:deploy-production --force

## Postgres Replicas Stateful Set using Bitnami Helm

* https://engineering.bitnami.com/articles/create-a-production-ready-postgresql-cluster-bitnami-kubernetes-and-helm.html

### Commands:
* helm repo add bitnami https://charts.bitnami.com/bitnami

* helm install  bitnami/postgresql -f values-production.yaml --set postgresqlPassword=<> --set replication.password=<> --generate-name -n psql

* kubectl patch svc psql-svc -n psql -p '{"spec": {"type": "LoadBalancer"}}' ->(exposes the services)

## Add GCR SA Account as a Secret

In hindsight we should have given the nodes in the noodpool more GCP access.  

* kubectl create secret docker-registry gcr-json-key \
(out) --docker-server=eu.gcr.io \
(out) --docker-username=_json_key \
(out) --docker-password="$(cat ~/json-key-file.json)" \
(out) --docker-email=any@valid.email

## Sources for terraform and flask app
* https://github.com/gruntwork-io/terraform-google-network/blob/master/modules/vpc-network/main.tf
* https://github.com/gruntwork-io/terraform-google-gke/tree/master/modules/gke-cluster
* https://github.com/ytimocin/flask-postgres-server
* https://www.geeksforgeeks.org/todo-list-app-using-flask-python/
