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

## Node Labels

```shell
$ kubectl describe nodes minikube
Name:               minikube
Roles:              control-plane
Labels:             beta.kubernetes.io/arch=amd64
                    beta.kubernetes.io/os=linux
                    kubernetes.io/arch=amd64
                    kubernetes.io/hostname=minikube
                    kubernetes.io/os=linux
                    minikube.k8s.io/commit=5883c09216182566a63dff4c326a6fc9ed2982ff
                    minikube.k8s.io/name=minikube
                    minikube.k8s.io/primary=true
                    minikube.k8s.io/updated_at=2024_07_21T16_40_25_0700
                    minikube.k8s.io/version=v1.33.1
                    node-role.kubernetes.io/control-plane=
                    node.kubernetes.io/exclude-from-external-load-balancers=
```

```shell
$ kubectl label nodes minikube-m02 node-type=superfast
node/minikube-m02 labeled
$ kubectl label nodes minikube-m03 node-type=superfast
node/minikube-m03 labeled

$ oc get nodes --show-labels |grep superfast
minikube-m02   Ready    <none>          80m   v1.30.0   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=minikube-m02,kubernetes.io/os=linux,minikube.k8s.io/commit=5883c09216182566a63dff4c326a6fc9ed2982ff,minikube.k8s.io/name=minikube,minikube.k8s.io/primary=false,minikube.k8s.io/updated_at=2024_07_21T16_41_14_0700,minikube.k8s.io/version=v1.33.1,node-type=superfast
minikube-m03   Ready    <none>          79m   v1.30.0   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=minikube-m03,kubernetes.io/os=linux,minikube.k8s.io/commit=5883c09216182566a63dff4c326a6fc9ed2982ff,minikube.k8s.io/name=minikube,minikube.k8s.io/primary=false,minikube.k8s.io/updated_at=2024_07_21T16_42_25_0700,minikube.k8s.io/version=v1.33.1,node-type=superfast
```

```shell
$ kubectl apply -f 02_nodeselector/nginx-deployment.yaml

$ kubectl get pods --namespace default --output=custom-columns="NAME:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName"
NAME                        STATUS    NODE
nginx-app-6c5b8b758-2dcsc   Running   minikube-m02
nginx-app-6c5b8b758-48c5t   Running   minikube-m03
nginx-app-6c5b8b758-pfmvg   Running   minikube-m03
nginx-app-6c5b8b758-v6rhj   Running   minikube-m02
nginx-app-6c5b8b758-zqvqm   Running   minikube-m02
```

```shell
$ kubectl apply -f 02_nodeselector/nginx-deployment-slow.yaml
deployment.apps/nginx-app configured

$ kubectl get pods --namespace default --output=custom-columns="NAME:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName"
NAME                        STATUS    NODE
nginx-app-6c5b8b758-48c5t   Running   minikube-m03
nginx-app-6c5b8b758-pfmvg   Running   minikube-m03
nginx-app-6c5b8b758-v6rhj   Running   minikube-m02
nginx-app-6c5b8b758-zqvqm   Running   minikube-m02
nginx-app-9cc8544f4-7dwcd   Pending   <none>
nginx-app-9cc8544f4-cz947   Pending   <none>
nginx-app-9cc8544f4-lfqqj   Pending   <none>
```

## Node affinity

```shell
$ kubectl label nodes --overwrite minikube node-type=slow
node/minikube labeled

$ kubectl label nodes --overwrite minikube-m02 node-type=fast
node/minikube-m02 labeled

$ kubectl label nodes --overwrite minikube-m03 node-type=superfast
node/minikube-m03 not labeled
# Note that this label was already present with this value
```

```shell
$ kubectl apply -f 03_affinity/nginx-deployment.yaml
deployment.apps/nginx-app configured

$ kubectl get pods --namespace default --output=custom-columns="NAME:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName"
NAME                         STATUS    NODE
nginx-app-7766c596cc-4d4sl   Running   minikube-m02
nginx-app-7766c596cc-4h6k6   Running   minikube-m03
nginx-app-7766c596cc-ksld5   Running   minikube-m03
nginx-app-7766c596cc-nw9hx   Running   minikube-m02
nginx-app-7766c596cc-tmwhm   Running   minikube-m03
```

```shell
$ kubectl label nodes --overwrite minikube node-type=slow
node/minikube not labeled
# Note that this label was already present with this value

$ kubectl label nodes --overwrite minikube-m02 node-type=extremelyslow
node/minikube-m02 labeled

$ kubectl label nodes --overwrite minikube-m03 node-type=extremelyslow
node/minikube-m03 labeled
```

```shell
$ kubectl rollout restart deployment nginx-app
deployment.apps/nginx-app restarted
```

```shell
$ kubectl get pods --namespace default --output=custom-columns="NAME:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName"
NAME                         STATUS    NODE
nginx-app-7d8c65464c-5d9cc   Running   minikube
nginx-app-7d8c65464c-b97g8   Running   minikube
nginx-app-7d8c65464c-cqwh5   Running   minikube
nginx-app-7d8c65464c-kh8bm   Running   minikube
nginx-app-7d8c65464c-xhpss   Running   minikube
```

## Taints and Tolerations


```shell
$ kubectl taint node minikube machine-check-exception=memory:NoExecute
node/minikube tainted

$ kubectl taint node minikube machine-check-exception=memory:NoExecute-
node/minikube untainted

$ kubectl taint node minikube machine-check-exception:NoExecute-
````

```shell
$ kubectl taint node minikube machine-check-exception=memory:NoExecute
node/minikube tainted

$ kubectl get pods --namespace default --output=custom-columns="NAME:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName"
NAME                         STATUS    NODE
nginx-app-7d8c65464c-5j69n   Pending   <none>
nginx-app-7d8c65464c-c8j58   Pending   <none>
nginx-app-7d8c65464c-cnczc   Pending   <none>
nginx-app-7d8c65464c-drpdh   Pending   <none>
nginx-app-7d8c65464c-xss9b   Pending   <none>
```


```shell
$ kubectl apply -f 04_taints/nginx-deployment.yaml
deployment.apps/nginx-app configured

$ kubectl get pods --namespace default --output=custom-columns="NAME:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName"
NAME                         STATUS    NODE
nginx-app-84d755f746-4zkjd   Running   minikube
nginx-app-84d755f746-58qmh   Running   minikube-m02
nginx-app-84d755f746-5h5vk   Running   minikube-m03
nginx-app-84d755f746-psmgf   Running   minikube-m02
nginx-app-84d755f746-zkbc6   Running   minikube-m03
```

```shell
$ kubectl taint node minikube machine-check-exception=memory:NoSchedule
node/minikube tainted

$ kubectl get pods --namespace default --output=custom-columns="NAME:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName"
NAME                         STATUS    NODE
nginx-app-84d755f746-58qmh   Running   minikube-m02
nginx-app-84d755f746-5h5vk   Running   minikube-m03
nginx-app-84d755f746-psmgf   Running   minikube-m02
nginx-app-84d755f746-sm2cm   Running   minikube-m03
nginx-app-84d755f746-zkbc6   Running   minikube-m03
```

```shell
$ kubectl taint node minikube machine-check-exception-
node/minikube untainted

$ kubectl rollout restart deployment nginx-app
deployment.apps/nginx-app restarted

$ kubectl get pods --namespace default --output=custom-columns="NAME:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName"
NAME                         STATUS    NODE
nginx-app-5bdd957558-fj7bk   Running   minikube-m02
nginx-app-5bdd957558-mrddn   Running   minikube-m03
nginx-app-5bdd957558-mz2pz   Running   minikube-m02
nginx-app-5bdd957558-pftz5   Running   minikube-m03
nginx-app-5bdd957558-vm6k9   Running   minikube
```

```shell
$ kubectl taint node minikube machine-check-exception=memory:NoSchedule
node/minikube tainted
$ kubectl taint node minikube machine-check-exception=memory:NoExecute
node/minikube tainted

$ kubectl get pods --namespace default --output=custom-columns="NAME:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName"
NAME                         STATUS    NODE
nginx-app-5bdd957558-7n42p   Running   minikube-m03
nginx-app-5bdd957558-fj7bk   Running   minikube-m02
nginx-app-5bdd957558-mrddn   Running   minikube-m03
nginx-app-5bdd957558-mz2pz   Running   minikube-m02
nginx-app-5bdd957558-pftz5   Running   minikube-m03
```