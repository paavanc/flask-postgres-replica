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

##Enable workload identity on SA account

This allows us to access google secret manager via a service account

gcloud iam service-accounts create $CLUSTER_NAME-sm --project $SECRETS_MANAGER_PROJECT_ID
gcloud iam service-accounts add-iam-policy-binding \
  --role roles/iam.workloadIdentityUser \
  --member "serviceAccount:$PROJECT_ID.svc.id.goog[$NAMESPACE/gsm-sa]" \
  $CLUSTER_NAME-sm@$SECRETS_MANAGER_PROJECT_ID.iam.gserviceaccount.com \
  --project $SECRETS_MANAGER_PROJECT_ID
gcloud projects add-iam-policy-binding $SECRETS_MANAGER_PROJECT_ID \
  --role roles/secretmanager.secretAccessor \
  --member "serviceAccount:$CLUSTER_NAME-sm@$SECRETS_MANAGER_PROJECT_ID.iam.gserviceaccount.com" \
  --project $SECRETS_MANAGER_PROJECT_ID