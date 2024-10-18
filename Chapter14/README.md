# Working with Helm Charts and Operator

- [Working with Helm Charts and Operator](#working-with-helm-charts-and-operator)
  - [Install Helm](#install-helm)
    - [Install Chart](#install-chart)
    - [Install WordPress](#install-wordpress)
    - [Additional deployments](#additional-deployments)
      - [Kubernetes Dashboard](#kubernetes-dashboard)
  - [Operators](#operators)
    - [Install Prometheus operator](#install-prometheus-operator)
    - [Install and check Grafana operator](#install-and-check-grafana-operator)
    - [Check CRD](#check-crd)
    - [Create Prometheus and Grafana instance](#create-prometheus-and-grafana-instance)

## Install Helm

```shell
$ sudo dnf repolist | grep fedora
fedora                                         Fedora 39 - x86_64

$ sudo dnf install helm

$ helm version
version.BuildInfo{Version:"v3.11", GitCommit:"", GitTreeState:"", GoVersion:"go1.21rc3"}
```

```shell
choco install kubernetes-helm
```

```shell
$ wget https://get.helm.sh/helm-v3.15.1-linux-amd64.tar.gz

$ tar -zxvf helm-v3.15.1-linux-amd64.tar.gz
linux-amd64/
linux-amd64/README.md
linux-amd64/LICENSE
linux-amd64/helm

$ sudo mv linux-amd64/helm /usr/local/bin/helm
$ helm version
version.BuildInfo{Version:"v3.15.1", GitCommit:"e211f2aa62992bd72586b395de50979e31231829", GitTreeState:"clean", GoVersion:"go1.22.3"}
```

### Install Chart

```shell
$ helm repo add stable https://charts.helm.sh/stable
"stable" has been added to your repositories

$ helm search repo stable|grep -i deprecated|head
stable/acs-engine-autoscaler            2.2.2           2.1.1                   DEPRECATED Scales worker nodes within agent pools
stable/aerospike                        0.3.5           v4.5.0.5                DEPRECATED A Helm chart for Aerospike in Kubern...
stable/airflow                          7.13.3          1.10.12                 DEPRECATED - ple


$ helm search hub|head
URL                                                     CHART VERSION                                           APP VERSION                                             DESCRIPTION
https://artifacthub.io/packages/helm/mya/12factor       24.1.2                                                                                                          Easily deploy any application that conforms to ...
https://artifacthub.io/packages/helm/gabibbo97/...      0.1.0                                                   fedora-32                                               389 Directory Server

$ helm search hub wordpress
URL                                                     CHART VERSION   APP VERSION            DESCRIPTION
https://artifacthub.io/packages/helm/kube-wordp...      0.1.0           1.1                    this is my wordpress package
https://artifacthub.io/packages/helm/wordpress-...      1.0.2           1.0.0                  A Helm chart for deploying Wordpress+Mariadb st...
https://artifacthub.io/packages/helm/bitnami-ak...      15.2.13         6.1.0                  WordPress is the world's most popular blogging ...
```

### Install WordPress

```shell
$ helm repo add bitnami https://charts.bitnami.com/bitnami
"bitnami" has been added to your repositories
```

```shell
$ kubectl create ns wordpress
namespace/wordpress created
```

```shell
$ helm install wp-demo bitnami/wordpress -n wordpress --values wp-values.yaml
NAME: wp-demo
LAST DEPLOYED: Tue Jun  4 21:27:49 2024
NAMESPACE: wordpress
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
CHART NAME: wordpress
CHART VERSION: 22.4.2
APP VERSION: 6.5.3

** Please be patient while the chart is being deployed **

Your WordPress site can be accessed through the following DNS name from within your cluster:

    wp-demo-wordpress.wordpress.svc.cluster.local (port 80)

To access your WordPress site from outside the cluster follow the steps below:

1. Get the WordPress URL by running these commands:

   export NODE_PORT=$(kubectl get --namespace wordpress -o jsonpath="{.spec.ports[0].nodePort}" services wp-demo-wordpress)
   export NODE_IP=$(kubectl get nodes --namespace wordpress -o jsonpath="{.items[0].status.addresses[0].address}")
   echo "WordPress URL: http://$NODE_IP:$NODE_PORT/"
   echo "WordPress Admin URL: http://$NODE_IP:$NODE_PORT/admin"

2. Open a browser and access WordPress using the obtained URL.

3. Login with the following credentials below to see your blog:

  echo Username: wpadmin
  echo Password: $(kubectl get secret --namespace wordpress wp-demo-wordpress -o jsonpath="{.data.wordpress-password}" | base64 -d)

WARNING: There are "resources" sections in the chart not set. Using "resourcesPreset" is not recommended for production. For production installations, please set the following values according to your workload needs:
  - resources
+info https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
```

Specific version

```shell
$ helm install my-wordpress bitnami/wordpress --version 22.4.2
```

```shell
$ kubectl get po -n wordpress
NAME                                 READY   STATUS    RESTARTS        AGE
wp-demo-mariadb-0                    1/1     Running   9 (5m57s ago)   31m
wp-demo-wordpress-5d98c44785-9xd6h   1/1     Running   0               31m
``

```shell
$ kubectl get statefulsets.apps -n wordpress
NAME              READY   AGE
wp-demo-mariadb   1/1     99s
```

```shell
$ kubectl get svc -n wordpress
NAME                TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
wp-demo-mariadb     ClusterIP   10.100.118.79   <none>        3306/TCP                     2m39s
wp-demo-wordpress   NodePort    10.100.149.20   <none>        80:30509/TCP,443:32447/TCP   2m39s
```

```shell
$ minikube service --url wp-demo-wordpress -n wordpress
http://192.168.59.150:30509
http://192.168.59.150:32447
```

Retrieve password

```shell
$ kubectl get secret --namespace wordpress wp-demo-wordpress -o jsonpath="{.data.wordp
ress-password}" | base64 --decode
wppassword
```

```shell
$ helm list -n wordpress
NAME    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART              APP VERSION
wp-demo wordpress       1               2024-06-04 22:20:32.556683096 +0800 +08 deployed        wordpress-22.4.2   6.5.3
```

Uninstall release

```shell
$ helm uninstall wp-demo -n wordpress
release "wp-demo" uninstalled
```

### Additional deployments

#### Kubernetes Dashboard

```shell
$ helm repo add kubernetes-dashboard https://kubernetes.github.io/dashboard/
"kubernetes-dashboard" has been added to your repositories

$ helm upgrade --install kubernetes-dashboard kubernetes-dashboard/kubernetes-dashboard --create-namespace --namespace kubernetes-dashboard
Release "kubernetes-dashboard" does not exist. Installing it now.
NAME: kubernetes-dashboard
LAST DEPLOYED: Wed Jun  5 00:30:37 2024
NAMESPACE: kubernetes-dashboard
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
*************************************************************************************************
*** PLEASE BE PATIENT: Kubernetes Dashboard may need a few minutes to get up and become ready ***
*************************************************************************************************

Congratulations! You have just installed Kubernetes Dashboard in your cluster.

To access Dashboard run:
  kubectl -n kubernetes-dashboard port-forward svc/kubernetes-dashboard-kong-proxy 8443:443

NOTE: In case port-forward command does not work, make sure that kong service name is correct.
      Check the services in Kubernetes Dashboard namespace using:
        kubectl -n kubernetes-dashboard get svc

Dashboard will be available at:
  https://localhost:8443
```


```shell
$ kubectl get po -n kubernetes-dashboard
NAME                                                    READY   STATUS    RESTARTS   AGE
kubernetes-dashboard-api-68fc77fc9f-zbvcw               1/1     Running   0          52s
kubernetes-dashboard-auth-567d8754b8-5wn5n              1/1     Running   0          52s
kubernetes-dashboard-kong-7696bb8c88-2rsxl              1/1     Running   0          52s
kubernetes-dashboard-metrics-scraper-5485b64c47-hzkdn   1/1     Running   0          52s
kubernetes-dashboard-web-84f8d6fff4-rstdl               1/1     Running   0          52s

$ kubectl expose deployment kubernetes-dashboard-web --type=NodePort --port 8000 --name k8s-dashboard -n kubernetes-dashboard
service/k8s-dashboard exposed

$ minikube service --url k8s-dashboard -n kubernetes-dashboard
http://192.168.59.150:30556
```

Setup login

```shell
$ kubectl apply -f dashboard-sa.yaml
serviceaccount/admin-user created

$ kubectl apply -f dashboard-rbac.yml
clusterrolebinding.rbac.authorization.k8s.io/admin-user created

$ kubectl -n kubernetes-dashboard create token admin-user
eyJhbGciOiJSUzI1NiIsImtpZCI6ImFYREhzS25YOE1ydkJ3QnV5el9QWFhhNUJVdjEyNnBJbXNXeWxrMXpJMXMifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwiXSwiZXhwIjoxNzE3NTE4NTIwLCJpYXQiOjE3MTc1MTQ5MjAsImlzcyI6Imh0dHBzOi8va3ViZXJuZXRlcy5kZWZhdWx0LnN2Yy5jbHVzdGVyLmxvY2FsIiwianRpIjoiMTExNGQ3MDYtNjRhYi00NGI5LWI5ZGEtNDllZGFmMTRhZTllIiwia3ViZXJuZXRlcy5pbyI6eyJuYW1lc3BhY2UiOiJrdWJlcm5ldGVzLWRhc2hib2FyZCIsInNlcnZpY2VhY2NvdW50Ijp7Im5hbWUiOiJhZG1pbi11c2VyIiwidWlkIjoiZWQ1NjNkMjktNTg3OC00YmZiLThkMjUtMTE4ZjM2YjZjZTFiIn19LCJuYmYiOjE3MTc1MTQ5MjAsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlcm5ldGVzLWRhc2hib2FyZDphZG1pbi11c2VyIn0.Y-4_LymKHU2HzspJUdt55aYtxVAG8BSoEaDi6e7V5q7K-R2rEbpDQd9Jc0VIGkzmQL72skrGmvVw1HGLJLxYeFSUycljQgbava6d0o-PZk8ca6_C2L3yOfNqPSiJY98tG_ggCB4Q4uKYBoeKQueZkB21Bev8qrJwUletHMDNO88QofodBfwNdK0QyO8wLrtEvGnybfYufB3hLjevnNbxeYgnS7l-7J3EeBdd_NRH1h9hvAwvEJJeIfvoykA_OkrmhkJu5HQWBeV1f7Rmab9UMjlodTdLvpLh0tHj9gCQq6lZrSTulBDP3TNquBZ3TVaa8o_Al3oSrOH6kdHjxiNSZg
```

```shell
$ kubectl -n kubernetes-dashboard port-forward svc/kubernetes-dashboard-kong-proxy 8443:443
Forwarding from 127.0.0.1:8443 -> 8443
Forwarding from [::1]:8443 -> 8443

kubectl -n dashboard get secret $(kubectl -n dashboard get sa/admin-user -o jsonpath="{.secrets[0].name}") -o go-template="{{.data.token | base64decode}}"
```

## Operators

```shell
$ curl -sL https://github.com/operator-framework/operator-lifecycle-manager/releases/download/v0.28.0/install.sh | bash -s v0.28.0
customresourcedefinition.apiextensions.k8s.io/catalogsources.operators.coreos.com created
customresourcedefinition.apiextensions.k8s.io/clusterserviceversions.operators.coreos.com created
customresourcedefinition.apiextensions.k8s.io/installplans.operators.coreos.com created
customresourcedefinition.apiextensions.k8s.io/olmconfigs.operators.coreos.com created
customresourcedefinition.apiextensions.k8s.io/operatorconditions.operators.coreos.com created
customresourcedefinition.apiextensions.k8s.io/operatorgroups.operators.coreos.com created
customresourcedefinition.apiextensions.k8s.io/operators.operators.coreos.com created
customresourcedefinition.apiextensions.k8s.io/subscriptions.operators.coreos.com created
customresourcedefinition.apiextensions.k8s.io/catalogsources.operators.coreos.com condition met
customresourcedefinition.apiextensions.k8s.io/clusterserviceversions.operators.coreos.com condition met
customresourcedefinition.apiextensions.k8s.io/installplans.operators.coreos.com condition met
customresourcedefinition.apiextensions.k8s.io/olmconfigs.operators.coreos.com condition met
customresourcedefinition.apiextensions.k8s.io/operatorconditions.operators.coreos.com condition met
customresourcedefinition.apiextensions.k8s.io/operatorgroups.operators.coreos.com condition met
customresourcedefinition.apiextensions.k8s.io/operators.operators.coreos.com condition met
customresourcedefinition.apiextensions.k8s.io/subscriptions.operators.coreos.com condition met
namespace/olm created
namespace/operators created
serviceaccount/olm-operator-serviceaccount created
clusterrole.rbac.authorization.k8s.io/system:controller:operator-lifecycle-manager created
clusterrolebinding.rbac.authorization.k8s.io/olm-operator-binding-olm created
olmconfig.operators.coreos.com/cluster created
deployment.apps/olm-operator created
deployment.apps/catalog-operator created
clusterrole.rbac.authorization.k8s.io/aggregate-olm-edit created
clusterrole.rbac.authorization.k8s.io/aggregate-olm-view created
operatorgroup.operators.coreos.com/global-operators created
operatorgroup.operators.coreos.com/olm-operators created
clusterserviceversion.operators.coreos.com/packageserver created
catalogsource.operators.coreos.com/operatorhubio-catalog created
Waiting for deployment "olm-operator" rollout to finish: 0 of 1 updated replicas are available...
deployment "olm-operator" successfully rolled out
Waiting for deployment "catalog-operator" rollout to finish: 0 of 1 updated replicas are available...
deployment "catalog-operator" successfully rolled out
Package server phase: Installing
Package server phase: Succeeded
deployment "packageserver" successfully rolled out
```

```shell
$ kubectl get pods -n olm
NAME                               READY   STATUS    RESTARTS   AGE
catalog-operator-9f6dc8c87-rt569   1/1     Running   0          36s
olm-operator-6bccddc987-nrlkm      1/1     Running   0          36s
operatorhubio-catalog-6l8pw        0/1     Running   0          21s
packageserver-6df47456b9-8fdt7     1/1     Running   0          24s
packageserver-6df47456b9-lrvzp     1/1     Running   0          24s
```

```shell
$ kubectl get csv -n olm
NAME            DISPLAY          VERSION   REPLACES   PHASE
packageserver   Package Server   0.28.0               Succeeded
```
### Install Prometheus operator

Check prometheus

```shell
$ kubectl get packagemanifests | grep prometheus
ack-prometheusservice-controller           Community Operators   12m
prometheus                                 Community Operators   12m
prometheus-exporter-operator               Community Operators   12m
```

Install and check prometheus operator

```shell
$ kubectl create -f https://operatorhub.io/install/prometheus.yaml
subscription.operators.coreos.com/my-prometheus created

$ kubectl get csv -n operators
NAME                         DISPLAY               VERSION   REPLACES                     PHASE
prometheusoperator.v0.70.0   Prometheus Operator   0.70.0    prometheusoperator.v0.65.1   Succeeded

$ kubectl get pods -n operators
NAME                                   READY   STATUS    RESTARTS   AGE
prometheus-operator-84f9b76686-twvbq   1/1     Running   0          10m
```

### Install and check Grafana operator

```shell
$ kubectl create -f https://operatorhub.io/install/grafana-operator.yaml
subscription.operators.coreos.com/my-grafana-operator created
```

### Check CRD

```shell
$ kubectl get crd
NAME                                                  CREATED AT
alertmanagerconfigs.monitoring.coreos.com             2024-10-18T09:14:03Z
alertmanagers.monitoring.coreos.com                   2024-10-18T09:14:04Z
catalogsources.operators.coreos.com                   2024-10-18T09:10:00Z
clusterserviceversions.operators.coreos.com           2024-10-18T09:10:00Z
grafanaalertrulegroups.grafana.integreatly.org        2024-10-18T09:25:19Z
grafanacontactpoints.grafana.integreatly.org          2024-10-18T09:25:19Z
grafanadashboards.grafana.integreatly.org             2024-10-18T09:25:20Z
grafanadatasources.grafana.integreatly.org            2024-10-18T09:25:20Z
grafanafolders.grafana.integreatly.org                2024-10-18T09:25:19Z
grafananotificationpolicies.grafana.integreatly.org   2024-10-18T09:25:20Z
grafanas.grafana.integreatly.org                      2024-10-18T09:25:19Z
installplans.operators.coreos.com                     2024-10-18T09:10:00Z
olmconfigs.operators.coreos.com                       2024-10-18T09:10:00Z
operatorconditions.operators.coreos.com               2024-10-18T09:10:00Z
operatorgroups.operators.coreos.com                   2024-10-18T09:10:00Z
operators.operators.coreos.com                        2024-10-18T09:10:00Z
podmonitors.monitoring.coreos.com                     2024-10-18T09:14:03Z
probes.monitoring.coreos.com                          2024-10-18T09:14:03Z
prometheusagents.monitoring.coreos.com                2024-10-18T09:14:04Z
prometheuses.monitoring.coreos.com                    2024-10-18T09:14:04Z
prometheusrules.monitoring.coreos.com                 2024-10-18T09:14:03Z
scrapeconfigs.monitoring.coreos.com                   2024-10-18T09:14:03Z
servicemonitors.monitoring.coreos.com                 2024-10-18T09:14:03Z
subscriptions.operators.coreos.com                    2024-10-18T09:10:00Z
thanosrulers.monitoring.coreos.com                    2024-10-18T09:14:03Z
```

### Create Prometheus and Grafana instance

```shell
$ kubectl apply -f monitoring-ns.yaml
namespace/monitoring created
```

Create Service Account

```shell
$ kubectl apply -f monitoring-sa.yaml
serviceaccount/prometheus created
role.rbac.authorization.k8s.io/prometheus-role created
rolebinding.rbac.authorization.k8s.io/prometheus-rolebinding created
```

Create Prometheus instance

```shell
$ kubectl apply -f prometheus-instance.yaml
prometheus.monitoring.coreos.com/example-prometheus created
```

Install Grafana instance

```shell
$ kubectl apply -f grafana-instnace.yaml
grafana.grafana.integreatly.org/grafana-a created
```

```shell
$  kubectl get pod,svc,sts -n monitoring
NAME                                       READY   STATUS    RESTARTS   AGE
pod/grafana-a-deployment-69f8999f8-82zbv   1/1     Running   0          17m
pod/node-exporter-n7tlb                    1/1     Running   0          93s
pod/prometheus-example-prometheus-0        2/2     Running   0          20m
pod/prometheus-example-prometheus-1        2/2     Running   0          20m

NAME                          TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
service/grafana-a-service     ClusterIP   10.107.212.241   <none>        3000/TCP   17m
service/prometheus-operated   ClusterIP   None             <none>        9090/TCP   20m

NAME                                             READY   AGE
statefulset.apps/prometheus-example-prometheus   2/2     20m
```

Create Node Exporter daemonset

```shell
$ kubectl apply -f node-exporter-daemonset.yaml
daemonset.apps/node-exporter created
```

Create Node Exporter svc

```shell
$ kubectl apply -f node-exporter-svc.yaml
service/node-exporter created
```

Create ServiceMonitor

```shell
$ kubectl apply -f servicemonitor-instance.yaml
servicemonitor.monitoring.coreos.com/node-exporter created
```

Verify Prometheus

```shell
$ kubectl port-forward -n monitoring svc/prometheus-operated 9091:9090
Forwarding from 127.0.0.1:9091 -> 9090
Forwarding from [::1]:9091 -> 9090
```

```shell
$ kubectl port-forward -n monitoring service/grafana-a-service 3000:3000
Forwarding from 127.0.0.1:3000 -> 3000
Forwarding from [::1]:3000 -> 3000
```
