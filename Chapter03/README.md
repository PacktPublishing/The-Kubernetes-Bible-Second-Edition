# Installing Your First Kubernetes Cluster

## minikube configurations

```shell
$ minikube config set cpus 4
❗  These changes will take effect upon a minikube delete and then a minikube start

$ minikube config set memory 16000
❗  These changes will take effect upon a minikube delete and then a minikube start

$  minikube config set driver podman
❗  These changes will take effect upon a minikube delete and then a minikube start

$  minikube config view driver
- driver: podman
- rootless: false
```

## Deploying Kubernetes using minikube

On your workstation where you have installed minikube and VirtualBox, execute the following command.

```shell
$ minikube start --driver=virtualbox --memory=8000m --cpus=2
```

If you are using an old version of minikube but you want to install different version of Kubernetes version, then you can mention the specific version as follows.

```shell
$ minikube start --driver=virtualbox --memory=8000m --cpus=2 --kubernetes-version=1.29.0
```

```shell
$  minikube status
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured
```

Using container

```shell
$ minikube start --driver=docker --kubernetes-version=1.29.0
```

Check nodes

```shell
$ kubectl get nodes
NAME       STATUS   ROLES           AGE     VERSION
minikube   Ready    control-plane   3m52s   v1.29.0
```

```shell
$ kubectl get componentstatuses
Warning: v1 ComponentStatus is deprecated in v1.19+
NAME                 STATUS    MESSAGE   ERROR
controller-manager   Healthy   ok
scheduler            Healthy   ok
etcd-0               Healthy   ok
```

## Stop/Pause/Delete minikube clusters

```shell
$  minikube stop
✋  Stopping node "minikube"  ...
🛑  1 node stopped.

$ minikube status
minikube
type: Control Plane
host: Stopped
kubelet: Stopped
apiserver: Stopped
kubeconfig: Stopped

```


## Multiple Kubernetes clusters using minikube

```shell
# Start a minikube cluster using Podman as driver.
$ minikube start --profile cluster2-podman --driver=podman

# Stop cluster
$ minikube stop --profile cluster2-podman

# Remove the cluster
$ minikube delete --profile cluster2-podman
```

## Multi-node Kubernetes using minikube

```shell
$ minikube start --driver=podman --nodes=3

$ kubectl get nodes
NAME           STATUS   ROLES           AGE   VERSION
minikube       Ready    control-plane   77s   v1.28.3
minikube-m02   Ready    <none>          58s   v1.28.3
minikube-m03   Ready    <none>          44s   v1.28.3
```

## Creating cluster using king

```shell
$ kind create cluster --name test-kind
```

Config file creating multi-node cluster - eg: `~/.kube/kind_cluster`

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
- role: worker
- role: worker
- role: worker
```

Create cluster

```shell
$ kind create cluster --config ~/.kube/kind_cluster
```

Start with Podman instead of Docker

```shell
$ KIND_EXPERIMENTAL_PROVIDER=podman kind create cluster --config ~/.kube/kind_cluster
```