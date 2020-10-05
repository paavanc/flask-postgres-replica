# flask-postgres-replica
Sample Flask App Simulating Postgres Replication


#ArgoCD
Our k8 deployment tool

https://argoproj.github.io/argo-cd/getting_started/


#Make new images
git push origin main:deploy-production --force

#Postgres Replicas Stateful Set using Bitnami Helm

helm repo add bitnami https://charts.bitnami.com/bitnami

https://engineering.bitnami.com/articles/create-a-production-ready-postgresql-cluster-bitnami-kubernetes-and-helm.html

helm install  bitnami/postgresql -f values-production.yaml --set postgresqlPassword=<> --set replication.password=<> --generate-name -n psql

kubectl patch svc psql-svc -n psql -p '{"spec": {"type": "LoadBalancer"}}'
