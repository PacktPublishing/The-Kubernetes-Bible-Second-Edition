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

Objects no in namespace

```shell
$ kubectl api-resources --namespaced=false
NAME                              SHORTNAMES   APIVERSION                        NAMESPACED   KIND
componentstatuses                 cs           v1                                false        ComponentStatus
namespaces                        ns           v1                                false        Namespace
nodes                             no           v1                                false        Node
persistentvolumes                 pv           v1                                false        PersistentVolume
...<removed for brevity>...
```

```shell
$ kubectl create ns another-ns
namespace/another-ns created
```

```shell
# set alias in ~/.bashrc
alias kubens='kubectl config set-context --current --namespace'

# Use it
$ kubens custom-ns
Context "minikube" modified.
$ kubectl config view --minify --output 'jsonpath={..namespace}'
custom-n

# change to another namespace
$ kubens default
Context "minikube" modified.
$ kubectl config view --minify --output 'jsonpath={..namespace}'
default
```

Enable metics server

```shell
$ minikube addons enable metrics-server
💡  metrics-server is an addon maintained by Kubernetes. For any concerns contact minikube on GitHub.
You can view the list of minikube maintainers at: https://github.com/kubernetes/minikube/blob/master/OWNERS
    ▪ Using image registry.k8s.io/metrics-server/metrics-server:v0.6.4
🌟  The 'metrics-server' addon is enabled

$ kubectl get po -n kube-system | grep metrics
metrics-server-7c66d45ddc-82ngt            1/1     Running   0               113m

$ kubectl top node
NAME       CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%
minikube   181m         1%     806Mi           2%
```

Another minikube cluster

```shell
$ minikube start --profile cluster2-vb --driver=virtualbox
```

Create Pod with requests and limits

```shell
$ kubectl apply -f pod-with-request-and-limit-1.yaml
pod/nginx-with-request-and-limit-1 created

$  kubectl get pod -n custom-ns
NAME                             READY   STATUS    RESTARTS   AGE
nginx-with-request-and-limit-1   0/1     Pending   0          45s
```

```shell
$ kubectl describe po nginx-with-request-and-limit-1 -n custom-ns
Name:             nginx-with-request-and-limit-1
Namespace:        custom-ns
Priority:         0
Service Account:  default
Node:             <none>
Labels:           <none>
Annotations:      <none>
Status:           Pending
IP:
IPs:              <none>
Containers:
  nginx:
    Image:      nginx:latest
    Port:       <none>
    Host Port:  <none>
    Limits:
      cpu:     500m
      memory:  100Gi
    Requests:
      cpu:        100m
      memory:     100Gi
    Environment:  <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-jnr4c (ro)
Conditions:
  Type           Status
  PodScheduled   False
Volumes:
  kube-api-access-jnr4c:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  3607
    ConfigMapName:           kube-root-ca.crt
    ConfigMapOptional:       <nil>
    DownwardAPI:             true
QoS Class:                   Burstable
Node-Selectors:              <none>
Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                             node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:
  Type     Reason            Age   From               Message
  ----     ------            ----  ----               -------
  Warning  FailedScheduling  105s  default-scheduler  0/1 nodes are available: 1 Insufficient memory. preemption: 0/1 nodes are available: 1 No preemption victims found for incoming pod.
```

```shell
$ kubectl create -f pod-with-request-and-limit-2.yaml
pod/nginx-with-request-and-limit-2 created

$ kubectl get po -n custom-ns
NAME                             READY   STATUS    RESTARTS   AGE
nginx-with-request-and-limit-1   0/1     Pending   0          8m24s
nginx-with-request-and-limit-2   1/1     Running   0          20s
```

```shell
$ kubectl create -f resourcequota.yaml
resourcequota/resourcequota created
$ kubectl get quota -n custom-ns
NAME            AGE   REQUEST                                          LIMIT
resourcequota   4s    requests.cpu: 100m/1, requests.memory: 1Gi/1Gi   limits.cpu: 500m/2, limits.memory: 2Gi/2Gi
```

```shell
$ kubectl get po -n custom-ns
NAME                             READY   STATUS    RESTARTS        AGE
nginx-with-request-and-limit-2   1/1     Running   1 (5h41m ago)   7h18m
$ kubectl top pod -n custom-ns
NAME                             CPU(cores)   MEMORY

$ kubectl apply -f pod-with-request-and-limit-3.yaml
Error from server (Forbidden): error when creating "pod-with-request-and-limit-3.yaml": pods "nginx-with-request-and-limit-3" is forbidden: exceeded quota: resourcequota, requested: limits.memory=4Gi,requests.memory=3Gi, used: limits.memory=2Gi,requests.memory=1Gi, limited: limits.memory=2Gi,requests.memory=1Gi
```


```shell
$ kubectl get resourcequotas -n custom-ns
NAME            AGE   REQUEST                                          LIMIT
resourcequota   15m   requests.cpu: 100m/1, requests.memory: 1Gi/1Gi   limits.cpu: 500m/2, limits.memory: 2Gi/2Gi
```

```shell
$ kubectl get limitranges -n custom-ns
NAME            CREATED AT
my-limitrange   2024-03-10T16:13:00Z

$ kubectl delete limitranges my-limitrange -n custom-ns
limitrange "my-limitrange" deleted
```