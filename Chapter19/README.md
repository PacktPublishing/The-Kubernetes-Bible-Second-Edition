# Advanced Techniques for Scheduling Pods


```shell
$ minikube start \
  --driver=virtualbox \
  --nodes 3 \
  --cni calico \
  --cpus=2 \
  --memory=2g \
  --kubernetes-version=v1.30.0 \
  --container-runtime=containerd

$ kubectl get nodes
NAME           STATUS   ROLES           AGE     VERSION
minikube       Ready    control-plane   3m34s   v1.30.0
minikube-m02   Ready    <none>          2m34s   v1.30.0
minikube-m03   Ready    <none>          87s     v1.30.0
```

## Nodename

```shell
$ kubectl apply -f 01_nodename/nginx-deployment.yaml
deployment.apps/nginx-app created

$ kubectl get pods --namespace default --output=custom-columns="NAME:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName"
NAME                         STATUS    NODE
nginx-app-7b547cfd87-4g9qx   Running   minikube
nginx-app-7b547cfd87-m76l2   Running   minikube-m02
nginx-app-7b547cfd87-mjf78   Running   minikube-m03
nginx-app-7b547cfd87-vvrgk   Running   minikube-m02
nginx-app-7b547cfd87-w7jcw   Running   minikube-m03

$ kubectl delete -f 01_nodename/nginx-deployment.yaml
deployment.apps "nginx-app" deleted

$ kubectl get pods --namespace default --output=custom-columns="NAME:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName"
NAME                         STATUS    NODE
nginx-app-85b577894f-8tqj7   Running   minikube-m02
nginx-app-85b577894f-9c6hd   Running   minikube-m02
nginx-app-85b577894f-fldxx   Running   minikube-m02
nginx-app-85b577894f-jrnjc   Running   minikube-m02
nginx-app-85b577894f-vs7c5   Running   minikube-m02

```