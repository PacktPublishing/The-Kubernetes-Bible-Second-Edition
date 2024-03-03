# Managing Namespaces in Kubernetes

```shell
$ kubectl get namespaces
NAME              STATUS   AGE
default           Active   8d
kube-node-lease   Active   8d
kube-public       Active   8d
kube-system       Active   8d
```

```shell
$ kubectl describe namespaces default
Name:         default
Labels:       kubernetes.io/metadata.name=default
Annotations:  <none>
Status:       Active

No resource quota.

No LimitRange resource.
```

```shell
$ kubectl get namespaces default -o yaml > default-ns.yaml
```

```shell
$ kubectl create ns custom-ns
namespace/custom-ns created

$ kubectl get ns custom-ns
NAME        STATUS   AGE
custom-ns   Active   21s
```

```shell
$ kubectl create -f custom-ns-2.yaml
namespace/custom-ns-2 created
```

Delete namespace

```shell
$ kubectl delete namespaces custom-ns
namespace "custom-ns" deleted

$ kubectl delete -f custom-ns-2.yaml
namespace "custom-ns-2" deleted
```

Using namespace

```shell
$ kubectl create ns custom-ns
namespace/custom-ns created

$ kubectl run nginx --image nginx:latest -n custom-ns
pod/nginx created

$ kubectl create configmap configmap-custom-ns --from-literal=Lorem=Ipsum -n custom-ns
configmap/configmap-custom-ns created

$ kubectl create -f pod-in-namespace.yaml
pod/nginx2 created
```
Listing resources inside a specific namespace

```shell
$ kubectl get pods -n custom-ns
NAME     READY   STATUS    RESTARTS   AGE
nginx    1/1     Running   0          9m23s
nginx2   1/1     Running   0          94s

$ kubectl get pods
No resources found in default namespace.

$ kubectl get cm
NAME               DATA   AGE
kube-root-ca.crt   1      9d

$ kubectl get cm -n custom-ns
NAME                  DATA   AGE
configmap-custom-ns   1      70m
kube-root-ca.crt      1      76m
```

```shell
$ kubectl config set-context --current --namespace=custom-ns
Context "minikube" modified.

$ kubectl config view --minify --output 'jsonpath={..namespace}'
custom-ns

$ kubectl get po
NAME     READY   STATUS    RESTARTS   AGE
nginx    1/1     Running   0          79m
nginx2   1/1     Running   0          71m

$ kubectl config set-context --current --namespace=default
Context "minikube" modified.
```
