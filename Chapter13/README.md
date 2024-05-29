# DaemonSet – Maintaining Pod Singletons on Nodes


## Create multi-node minikube

```shell
$ minikube start \
  --driver=virtualbox \
  --nodes 3 \
  --cni calico \
  --cpus=2 \
  --memory=2g \
  --kubernetes-version=v1.30.0

$ kubectl get nodes
NAME           STATUS   ROLES           AGE     VERSION
minikube       Ready    control-plane   3m28s   v1.30.0
minikube-m02   Ready    <none>          2m29s   v1.30.0
minikube-m03   Ready    <none>          91s     v1.30.0
```

```shell
$ kubectl get daemonsets -A
NAMESPACE     NAME          DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR            AGE
kube-system   calico-node   3         3         3       3            3           kubernetes.io/os=linux   63m
kube-system   kube-proxy    3         3         3       3            3           kubernetes.io/os=linux   63m
```

Check Pods

```shell
$ kubectl get po -n kube-system -o wide|grep calico
calico-kube-controllers-ddf655445-jx26x   1/1     Running   0          68m   10.244.120.65    minikube       <none>           <none>
calico-node-fkjxb                         1/1     Running   0          68m   192.168.59.126   minikube       <none>           <none>
calico-node-nrzpb                         1/1     Running   0          66m   192.168.59.128   minikube-m03   <none>           <none>
calico-node-sg66x                         1/1     Running   0          67m   192.168.59.127   minikube-m02   <none>           <none>
```

## Create DaemonSet
