# Working with Helm Charts and Operator

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

## Install Chart

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

## Install WordPress

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

## Additional deployments

### Kubernetes Dashboard

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
$ helm repo update
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "kubernetes-dashboard" chart repository
...Successfully got an update from the "stable" chart repository
...Successfully got an update from the "bitnami" chart repository
Update Complete. ⎈Happy Helming!⎈
```

```shell
$ helm install prometheus bitnami/kube-prometheus --create-namespace --namespace monitoring
NAME: prometheus
LAST DEPLOYED: Thu Jun  6 14:45:28 2024
NAMESPACE: monitoring
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
CHART NAME: kube-prometheus
CHART VERSION: 9.3.0
APP VERSION: 0.74.0

** Please be patient while the chart is being deployed **

Watch the Prometheus Operator Deployment status using the command:

    kubectl get deploy -w --namespace monitoring -l app.kubernetes.io/name=kube-prometheus-operator,app.kubernetes.io/instance=prometheus

Watch the Prometheus StatefulSet status using the command:

    kubectl get sts -w --namespace monitoring -l app.kubernetes.io/name=kube-prometheus-prometheus,app.kubernetes.io/instance=prometheus

Prometheus can be accessed via port "9090" on the following DNS name from within your cluster:

    prometheus-kube-prometheus-prometheus.monitoring.svc.cluster.local

To access Prometheus from outside the cluster execute the following commands:

    echo "Prometheus URL: http://127.0.0.1:9090/"
    kubectl port-forward --namespace monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090

Watch the Alertmanager StatefulSet status using the command:

    kubectl get sts -w --namespace monitoring -l app.kubernetes.io/name=kube-prometheus-alertmanager,app.kubernetes.io/instance=prometheus

Alertmanager can be accessed via port "9093" on the following DNS name from within your cluster:

    prometheus-kube-prometheus-alertmanager.monitoring.svc.cluster.local

To access Alertmanager from outside the cluster execute the following commands:

    echo "Alertmanager URL: http://127.0.0.1:9093/"
    kubectl port-forward --namespace monitoring svc/prometheus-kube-prometheus-alertmanager 9093:9093

WARNING: There are "resources" sections in the chart not set. Using "resourcesPreset" is not recommended for production. For production installations, please set the following values according to your workload needs:
  - alertmanager.resources
  - blackboxExporter.resources
  - operator.resources
  - prometheus.resources
  - prometheus.thanos.resources
+info https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/

```

```shell
$  kubectl get pod,svc,sts -n monitoring
NAME                                                              READY   STATUS    RESTARTS   AGE
pod/alertmanager-prometheus-kube-prometheus-alertmanager-0        2/2     Running   0          8m10s
pod/prometheus-kube-prometheus-blackbox-exporter-984564d5-z264l   1/1     Running   0          9m8s
pod/prometheus-kube-prometheus-operator-6ccb785575-xbkdp          1/1     Running   0          9m8s
pod/prometheus-kube-state-metrics-9d66f5498-dftlx                 1/1     Running   0          9m8s
pod/prometheus-node-exporter-vcfsz                                1/1     Running   0          9m8s
pod/prometheus-prometheus-kube-prometheus-prometheus-0            2/2     Running   0          8m10s

NAME                                                   TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                      AGE
service/alertmanager-operated                          ClusterIP   None             <none>        9093/TCP,9094/TCP,9094/UDP   8m10s
service/prometheus-kube-prometheus-alertmanager        ClusterIP   10.106.0.252     <none>        9093/TCP                     9m8s
service/prometheus-kube-prometheus-blackbox-exporter   ClusterIP   10.97.130.28     <none>        19115/TCP                    9m8s
service/prometheus-kube-prometheus-operator            ClusterIP   10.99.39.207     <none>        8080/TCP                     9m8s
service/prometheus-kube-prometheus-prometheus          ClusterIP   10.96.218.94     <none>        9090/TCP                     9m8s
service/prometheus-kube-state-metrics                  ClusterIP   10.106.101.139   <none>        8080/TCP                     9m8s
service/prometheus-node-exporter                       ClusterIP   10.104.57.79     <none>        9100/TCP                     9m8s
service/prometheus-operated                            ClusterIP   None             <none>        9090/TCP                     8m10s

NAME                                                                    READY   AGE
statefulset.apps/alertmanager-prometheus-kube-prometheus-alertmanager   1/1     8m10s
statefulset.apps/prometheus-prometheus-kube-prometheus-prometheus       1/1     8m10s
```

Install Grafana

```shell
$ helm install grafana bitnami/grafana-operator -n monitoring --values grafana-values.yaml
NAME: grafana
LAST DEPLOYED: Thu Jun  6 15:15:11 2024
NAMESPACE: monitoring
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
CHART NAME: grafana-operator
CHART VERSION: 4.4.3
APP VERSION: 5.9.2

** Please be patient while the chart is being deployed **

Watch the Grafana Operator Deployment status using the command:

    kubectl get deploy -w --namespace monitoring -l app.kubernetes.io/name=grafana-operator,app.kubernetes.io/instance=grafana


WARNING: There are "resources" sections in the chart not set. Using "resourcesPreset" is not recommended for production. For production installations, please set the following values according to your workload needs:
  - grafana.resources
  - operator.resources
+info https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
```

```shell
$ kubectl get po -n monitoring |grep grafana
grafana-grafana-operator-787b5cfcf-p9sf9                       0/1     Running   1 (8s ago)   2m24s
grafana-grafana-operator-grafana-deployment-6fd9bd9485-9xt4n   1/1     Running   0            2m8s
```

CRD

```shell
$ kubectl get crd
NAME                                             CREATED AT
alertmanagerconfigs.monitoring.coreos.com        2024-06-06T06:45:27Z
alertmanagers.monitoring.coreos.com              2024-06-06T06:45:27Z
grafanaalertrulegroups.grafana.integreatly.org   2024-06-06T07:15:09Z
grafanadashboards.grafana.integreatly.org        2024-06-06T07:15:09Z
grafanadatasources.grafana.integreatly.org       2024-06-06T07:15:09Z
grafanafolders.grafana.integreatly.org           2024-06-06T07:15:09Z
grafanas.grafana.integreatly.org                 2024-06-06T07:15:09Z
podmonitors.monitoring.coreos.com                2024-06-06T06:45:27Z
probes.monitoring.coreos.com                     2024-06-06T06:45:27Z
prometheusagents.monitoring.coreos.com           2024-06-06T06:45:28Z
prometheuses.monitoring.coreos.com               2024-06-06T06:45:28Z
prometheusrules.monitoring.coreos.com            2024-06-06T06:45:28Z
scrapeconfigs.monitoring.coreos.com              2024-06-06T06:45:28Z
servicemonitors.monitoring.coreos.com            2024-06-06T06:45:28Z
thanosrulers.monitoring.coreos.com               2024-06-06T06:45:28Z
```

Get services

```shell
$ kubectl get svc -n monitoring
NAME                                           TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                      AGE
alertmanager-operated                          ClusterIP   None             <none>        9093/TCP,9094/TCP,9094/UDP   73m
grafana-grafana-operator-grafana-service       NodePort    10.100.76.214    <none>        3000:30298/TCP               30m
prometheus-kube-prometheus-alertmanager        ClusterIP   10.106.0.252     <none>        9093/TCP                     74m
prometheus-kube-prometheus-blackbox-exporter   ClusterIP   10.97.130.28     <none>        19115/TCP                    74m
prometheus-kube-prometheus-operator            ClusterIP   10.99.39.207     <none>        8080/TCP                     74m
prometheus-kube-prometheus-prometheus          ClusterIP   10.96.218.94     <none>        9090/TCP                     74m
prometheus-kube-state-metrics                  ClusterIP   10.106.101.139   <none>        8080/TCP                     74m
prometheus-node-exporter                       ClusterIP   10.104.57.79     <none>        9100/TCP                     74m
prometheus-operated                            ClusterIP   None             <none>        9090/TCP                     73m
```

```shell
$ minikube service --url grafana-grafana-operator-grafana-service -n monitoring
http://192.168.59.153:30298
```

Get Grafana login password

```shell
$ kubectl get secrets grafana-grafana-operator-grafana-admin-credentials -n monitoring -o jsonpath="{.data.GF_SECURITY_ADMIN_PASSWORD}" | base64 --decode
ZQrnOovzxq0ckw==
```


```shell
$ curl -L https://github.com/operator-framework/operator-lifecycle-manager/releases/download/v0.28.0/install.sh -o install.sh
$ chmod +x install.sh
$ ./install.sh v0.28.0


$ kubectl get csv -A
NAMESPACE   NAME            DISPLAY          VERSION   REPLACES   PHASE
olm         packageserver   Package Server   0.28.0               Succeeded

$ kubectl get packagemanifest -n olm
NAME                                       CATALOG               AGE
lightbend-console-operator                 Community Operators   2m28s
ack-dynamodb-controller                    Community Operators   2m28s
ack-memorydb-controller                    Community Operators   2m28s
...
```

```
$ kubectl patch svc prometheus-k8s -n monitoring --type merge -p '{"spec":{"type": "NodePort"}}'
service/prometheus-k8s patched
```