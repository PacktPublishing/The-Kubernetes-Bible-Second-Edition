# Installing Your First Kubernetes Cluster

- [Installing Your First Kubernetes Cluster](#installing-your-first-kubernetes-cluster)
  - [Installing minikube](#installing-minikube)
  - [minikube configurations](#minikube-configurations)
  - [Deploying Kubernetes using minikube](#deploying-kubernetes-using-minikube)
  - [Stop/Pause/Delete minikube clusters](#stoppausedelete-minikube-clusters)
  - [Multiple Kubernetes clusters using minikube](#multiple-kubernetes-clusters-using-minikube)
    - [minikube check profiles](#minikube-check-profiles)
  - [Multi-node Kubernetes using minikube](#multi-node-kubernetes-using-minikube)
  - [Installing Kind](#installing-kind)
  - [Creating cluster using kind](#creating-cluster-using-kind)

## Installing minikube

Linux

```shell
$ curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
$ sudo install minikube-linux-amd64 /usr/local/bin/minikube
# Verify minikube command and path
$ which minikube
/usr/local/bin/minikube
```

macOS

```shell
$ curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-
darwin-amd64
$ sudo install minikube-darwin-amd64 /usr/local/bin/minikube
# Verify minikube command and path
$ which minikube
```

Windows

```shell
# Using Windows Package Manager (if installed)
$ winget install minikube
# Using Chocolatey
$ choco install minikube
# Via .exe download and setting the PATH
# 1. Download minikube: https://storage.googleapis.com/minikube/releases/
latest/minikube-installer.exe
# 2. Set PATH
```

## minikube configurations

```shell
$ minikube config set cpus 4
❗  These changes will take effect upon a minikube delete and then a minikube start

$ minikube config set memory 16000
❗  These changes will take effect upon a minikube delete and then a minikube start

$ minikube config set driver podman
❗  These changes will take effect upon a minikube delete and then a minikube start

$ minikube config view driver
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

Selecting correct driver:

```shell
    ▪ Using image gcr.io/k8s-minikube/storage-provisioner:v5
╭───────────────────────────────────────────────────────────────────────────────────────────────────╮
│                                                                                                   │
│    You have selected "virtualbox" driver, but there are better options !                          │
│    For better performance and support consider using a different driver:                          │
│            - kvm2                                                                                 │
│            - qemu2                                                                                │
│                                                                                                   │
│    To turn off this warning run:                                                                  │
│                                                                                                   │
│            $ minikube config set WantVirtualBoxDriverWarning false                                │
│                                                                                                   │
│                                                                                                   │
│    To learn more about on minikube drivers checkout https://minikube.sigs.k8s.io/docs/drivers/    │
│    To see benchmarks checkout https://minikube.sigs.k8s.io/docs/benchmarks/cpuusage/              │
│                                                                                                   │
╰───────────────────────────────────────────────────────────────────────────────────────────────────╯
🔎  Verifying Kubernetes components...
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
$ minikube start --driver=docker --kubernetes-version=1.30.0
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

$ minikube delete
🔥  Deleting "minikube" in docker ...
🔥  Deleting container "minikube" ...
🔥  Removing /home/iamgini/.minikube/machines/minikube ...
💀  Removed all traces of the "minikube" cluster.
```


## Multiple Kubernetes clusters using minikube

```shell
# Start a minikube cluster using Podman as driver.
$ minikube start --profile cluster-docker --driver=podman

$ minikube start --profile cluster-vbox --driver=virtualbox
```

### minikube check profiles

```shell
$ minikube profile list
|----------------|------------|------------|----------------|------|---------|---------|-------|----------------|--------------------|
|    Profile     | VM Driver  |  Runtime   |       IP       | Port | Version | Status  | Nodes | Active Profile | Active Kubecontext |
|----------------|------------|------------|----------------|------|---------|---------|-------|----------------|--------------------|
| cluster-docker | docker     | containerd | 192.168.49.2   | 8443 | v1.30.0 | Running |     1 |                |                    |
| cluster-vbox   | virtualbox | containerd | 192.168.59.145 | 8443 | v1.30.0 | Running |     1 |                | *                  |
|----------------|------------|------------|----------------|------|---------|---------|-------|----------------|--------------------|

# Stop cluster
$ minikube stop --profile cluster-docker

# Remove the cluster
$ minikube delete --profile cluster-podman
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

## Installing Kind

```shell
## Linux:
$ curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.27.1/kind-$(uname)-amd64
$ chmod +x ./kind
$ mv ./kind /usr/local/bin/kind

# macOS:
$ curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.27.1/kind-$(uname)-amd64
$ chmod +x ./kind
$ mv ./kind /usr/local/bin/kind

# Homebrew:
$ brew install kind

# Windows:
$ curl.exe -Llo kind-windows-amd64.exe https

# Chocolatey:
$ choco install kind
```

## Creating cluster using kind

```shell
$ kind create cluster --name test-kind
```

```shell
$ kubectl cluster-info
Kubernetes control plane is running at https://127.0.0.1:42547
CoreDNS is running at https://127.0.0.1:42547/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.

$ kubectl get --raw='/readyz?verbose'
[+]ping ok
[+]log ok
[+]etcd ok
[+]etcd-readiness ok
[+]informer-sync ok
[+]poststarthook/start-apiserver-admission-initializer ok
[+]poststarthook/generic-apiserver-start-informers ok
[+]poststarthook/priority-and-fairness-config-consumer ok
[+]poststarthook/priority-and-fairness-filter ok
[+]poststarthook/storage-object-count-tracker-hook ok
[+]poststarthook/start-apiextensions-informers ok
[+]poststarthook/start-apiextensions-controllers ok
[+]poststarthook/crd-informer-synced ok
[+]poststarthook/start-service-ip-repair-controllers ok
[+]poststarthook/rbac/bootstrap-roles ok
[+]poststarthook/scheduling/bootstrap-system-priority-classes ok
[+]poststarthook/priority-and-fairness-config-producer ok
[+]poststarthook/start-system-namespaces-controller ok
[+]poststarthook/bootstrap-controller ok
[+]poststarthook/start-cluster-authentication-info-controller ok
[+]poststarthook/start-kube-apiserver-identity-lease-controller ok
[+]poststarthook/start-kube-apiserver-identity-lease-garbage-collector ok
[+]poststarthook/start-legacy-token-tracking-controller ok
[+]poststarthook/aggregator-reload-proxy-client-cert ok
[+]poststarthook/start-kube-aggregator-informers ok
[+]poststarthook/apiservice-registration-controller ok
[+]poststarthook/apiservice-status-available-controller ok
[+]poststarthook/apiservice-discovery-controller ok
[+]poststarthook/kube-apiserver-autoregistration ok
[+]autoregister-completion ok
[+]poststarthook/apiservice-openapi-controller ok
[+]poststarthook/apiservice-openapiv3-controller ok
[+]shutdown ok
readyz check passed
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

Mention the Kubernetes version

```shell
# 1.29.0
$ kind create cluster \
  --name my-kind-cluster \
  --config ~/.kube/kind_cluster \
  --image kindest/node:v1.29.0@sha256:eaa1450915475849a73a9227b8f201df25e55e268e5d619312131292e324d570

# 1.29.0
$ kind create cluster \
  --name my-kind-cluster \
  --config ~/.kube/kind_cluster \
  --image kindest/node:v1.29.2@sha256:51a1434a5397193442f0be2a297b488b6c919ce8a3931be0ce822606ea5ca245
```

Refer to [github.com/kubernetes-sigs/kind/releases](https://github.com/kubernetes-sigs/kind/releases) to learn more.
