# Autoscaling Kubernetes Pods and Nodes

```shell
$ kubectl describe node minikube-m03
Name:               minikube-m03
Roles:              <none>
Labels:             beta.kubernetes.io/arch=amd64
                    beta.kubernetes.io/os=linux
                    kubernetes.io/arch=amd64
                    kubernetes.io/hostname=minikube-m03
                    kubernetes.io/os=linux
                    minikube.k8s.io/commit=5883c09216182566a63dff4c326a6fc9ed2982ff
                    minikube.k8s.io/name=minikube
                    minikube.k8s.io/primary=false
                    minikube.k8s.io/updated_at=2024_07_28T15_31_34_0700
                    minikube.k8s.io/version=v1.33.1
Annotations:        kubeadm.alpha.kubernetes.io/cri-socket: unix:///run/containerd/containerd.sock
                    node.alpha.kubernetes.io/ttl: 0
                    projectcalico.org/IPv4Address: 192.168.59.172/24
                    projectcalico.org/IPv4IPIPTunnelAddr: 10.244.151.18
                    volumes.kubernetes.io/controller-managed-attach-detach: true
CreationTimestamp:  Sun, 28 Jul 2024 15:31:36 +0800
Taints:             <none>
Unschedulable:      false
Lease:
  HolderIdentity:  minikube-m03
  AcquireTime:     <unset>
  RenewTime:       Sun, 28 Jul 2024 16:32:03 +0800
Conditions:
  Type                 Status  LastHeartbeatTime                 LastTransitionTime                Reason                       Message
  ----                 ------  -----------------                 ------------------                ------                       -------
  NetworkUnavailable   False   Sun, 28 Jul 2024 15:31:39 +0800   Sun, 28 Jul 2024 15:31:39 +0800   CalicoIsUp                   Calico is running on this node
  MemoryPressure       False   Sun, 28 Jul 2024 16:31:35 +0800   Sun, 28 Jul 2024 15:31:34 +0800   KubeletHasSufficientMemory   kubelet has sufficient memory available
  DiskPressure         False   Sun, 28 Jul 2024 16:31:35 +0800   Sun, 28 Jul 2024 15:31:34 +0800   KubeletHasNoDiskPressure     kubelet has no disk pressure
  PIDPressure          False   Sun, 28 Jul 2024 16:31:35 +0800   Sun, 28 Jul 2024 15:31:34 +0800   KubeletHasSufficientPID      kubelet has sufficient PID available
  Ready                True    Sun, 28 Jul 2024 16:31:35 +0800   Sun, 28 Jul 2024 15:31:37 +0800   KubeletReady                 kubelet is posting ready status
Addresses:
  InternalIP:  192.168.59.172
  Hostname:    minikube-m03
Capacity:
  cpu:                2
  ephemeral-storage:  17734596Ki
  hugepages-2Mi:      0
  memory:             2015788Ki
  pods:               110
Allocatable:
  cpu:                2
  ephemeral-storage:  17734596Ki
  hugepages-2Mi:      0
  memory:             2015788Ki
  pods:               110
System Info:
  Machine ID:                 b69112ce60bc44cbad0ebc952e33c188
  System UUID:                f5c6e926-02b5-5948-91ad-f93fec57765e
  Boot ID:                    1c139d10-c7ad-46fc-8fc4-c3f9b4f50d17
  Kernel Version:             5.10.207
  OS Image:                   Buildroot 2023.02.9
  Operating System:           linux
  Architecture:               amd64
  Container Runtime Version:  containerd://1.7.15
  Kubelet Version:            v1.30.0
  Kube-Proxy Version:         v1.30.0
PodCIDR:                      10.244.2.0/24
PodCIDRs:                     10.244.2.0/24
Non-terminated Pods:          (5 in total)
  Namespace                   Name                                         CPU Requests  CPU Limits  Memory Requests  Memory Limits  Age
  ---------                   ----                                         ------------  ----------  ---------------  -------------  ---
  default                     nginx-deployment-example-6d444cfd96-f5tnq    100m (5%)     200m (10%)  50Mi (2%)        60Mi (3%)      23s
  default                     nginx-deployment-example-6d444cfd96-k6j9d    100m (5%)     200m (10%)  50Mi (2%)        60Mi (3%)      23s
  default                     nginx-deployment-example-6d444cfd96-mqxxp    100m (5%)     200m (10%)  50Mi (2%)        60Mi (3%)      23s
  kube-system                 calico-node-92bdc                            250m (12%)    0 (0%)      0 (0%)           0 (0%)         6d23h
  kube-system                 kube-proxy-5cd4x                             0 (0%)        0 (0%)      0 (0%)           0 (0%)         6d23h
Allocated resources:
  (Total limits may be over 100 percent, i.e., overcommitted.)
  Resource           Requests    Limits
  --------           --------    ------
  cpu                550m (27%)  600m (30%)
  memory             150Mi (7%)  180Mi (9%)
  ephemeral-storage  0 (0%)      0 (0%)
  hugepages-2Mi      0 (0%)      0 (0%)
Events:              <none>
```

Update the request and limits.

```yaml
          resources:
            limits:
              cpu: 2000m
              memory: 60Mi
            requests:
              cpu: 2000m
              memory: 50Mi
```

```shell
$ kubectl apply -f resource-limit/nginx-deployment.yaml
deployment.apps/nginx-deployment-example configured
```

```shell
$ kubectl get pod
NAME                                        READY   STATUS    RESTARTS   AGE
nginx-deployment-example-59b669d85f-cdptx   1/1     Running   0          52s
nginx-deployment-example-59b669d85f-hdzdf   1/1     Running   0          54s
nginx-deployment-example-59b669d85f-ktn59   1/1     Running   0          54s
nginx-deployment-example-59b669d85f-vdn87   1/1     Running   0          52s
nginx-deployment-example-69bd6d55b4-n2mzq   0/1     Pending   0          3s
nginx-deployment-example-69bd6d55b4-qb62p   0/1     Pending   0          3s
nginx-deployment-example-69bd6d55b4-w7xng   0/1     Pending   0          3s
```

```shell
$ kubectl describe pod nginx-deployment-example-69bd6d55b4-n2mzq
...
Events:
  Type     Reason            Age                  From               Message
  ----     ------            ----                 ----               -------
  Warning  FailedScheduling  23m (x21 over 121m)  default-scheduler  0/3 nodes are available: 1 node(s) had untolerated taint {machine-check-exception: memory}, 2 Insufficient cpu. preemption: 0/3 nodes are available: 1 Preemption is not helpful for scheduling, 2 No preemption victims found for incoming pod.
```

## VerticalPodAutoscaler (VPA)


```shell
$ minikube start --feature-gates=InPlacePodVerticalScaling=true
```

```shell
  - command:
    - kube-apiserver
   ...<removed for brevity>...
    - --feature-gates=InPlacePodVerticalScaling=true
```

```shell
$ kubectl get pods -n kube-system | grep vpa
vpa-admission-controller-5b64b4f4c4-vsn9j   1/1     Running   0             5m34s
vpa-recommender-54c76554b5-m7wnk            1/1     Running   0             5m34s
vpa-updater-7d5f6fbf9b-rkwlb                1/1     Running   0             5m34s
```

```shell
$ minikube addons enable metrics-server
```

```shell
$ kubectl apply -f vpa/vpa-demo-ns.yaml
namespace/vpa-demo created

$ kubectl apply -f vpa/hamster-deployment.yaml
deployment.apps/hamster created
```

```shell
$ kubectl get po -n vpa-demo
NAME                      READY   STATUS    RESTARTS   AGE
hamster-7fb7dbff7-hmzt5   1/1     Running   0          8s
hamster-7fb7dbff7-lbk9f   1/1     Running   0          8s
hamster-7fb7dbff7-ql6gd   1/1     Running   0          8s
hamster-7fb7dbff7-qmxd8   1/1     Running   0          8s
hamster-7fb7dbff7-qtrpp   1/1     Running   0          8s

$ kubectl top pod -n vpa-demo
NAME                      CPU(cores)   MEMORY(bytes)
hamster-7fb7dbff7-hmzt5   457m         0Mi
hamster-7fb7dbff7-lbk9f   489m         0Mi
hamster-7fb7dbff7-ql6gd   459m         0Mi
hamster-7fb7dbff7-qmxd8   453m         0Mi
hamster-7fb7dbff7-qtrpp   451m         0Mi
```

```shell
$ kubectl apply -f vpa/hamster-vpa.yaml
verticalpodautoscaler.autoscaling.k8s.io/hamster-vpa created
```

```shell
$ kubectl describe vpa hamster-vpa -n vpa-demo
Name:         hamster-vpa
Namespace:    vpa-demo
...
Status:
  Conditions:
    Last Transition Time:  2024-08-11T09:20:44Z
    Status:                True
    Type:                  RecommendationProvided
  Recommendation:
    Container Recommendations:
      Container Name:  hamster
      Lower Bound:
        Cpu:     461m
        Memory:  262144k
      Target:
        Cpu:     587m
        Memory:  262144k
      Uncapped Target:
        Cpu:     587m
        Memory:  262144k
      Upper Bound:
        Cpu:     1
        Memory:  500Mi
Events:          <none>
```

Update mode

```yaml
# vpa/hamster-vpa.yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: hamster-vpa
  namespace: vpa-demo
spec:
...
  updatePolicy:
    updateMode: Auto
...


```shell
$ kubectl apply -f vpa/hamster-vpa.yaml
verticalpodautoscaler.autoscaling.k8s.io/hamster-vpa configured
```

```shell
$ kubectl get po -n vpa-demo -w
NAME                      READY   STATUS              RESTARTS   AGE
hamster-7fb7dbff7-24p89   0/1     ContainerCreating   0          2s
hamster-7fb7dbff7-6nz8f   0/1     ContainerCreating   0          2s
hamster-7fb7dbff7-hmzt5   1/1     Running             0          20m
hamster-7fb7dbff7-lbk9f   1/1     Running             0          20m
hamster-7fb7dbff7-ql6gd   1/1     Terminating         0          20m
hamster-7fb7dbff7-qmxd8   1/1     Terminating         0          20m
hamster-7fb7dbff7-qtrpp   1/1     Running             0          20m
hamster-7fb7dbff7-24p89   1/1     Running             0          2s
hamster-7fb7dbff7-6nz8f   1/1     Running             0          2s
```

```shell
$ kubectl describe pod hamster-7fb7dbff7-24p89 -n vpa-demo
...
Annotations:      ...<removed for brevity>...
                  vpaObservedContainers: hamster
                  vpaUpdates: Pod resources updated by hamster-vpa: container 0: memory request, cpu request
...
Containers:
  hamster:
    ...
    Requests:
      cpu:        587m
      memory:     262144k
...<removed for brevity>...
```

## HPA

```shell
$ kubectl apply -f hpa/hpa-demo-ns.yaml
namespace/hpa-demo created

$ kubectl apply -f hpa/todo-deployment.yaml
deployment.apps/todo-app created

$ kubectl get po -n hpa-demo
NAME                        READY   STATUS    RESTARTS   AGE
todo-app-5cfb496d77-l6r69   1/1     Running   0          8s

$ kubectl apply -f hpa/todo-service.yaml
service/todo-app created

$ kubectl get svc -n hpa-demo
NAME       TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
todo-app   ClusterIP   10.96.171.71   <none>        8081/TCP   15s

$ kubectl port-forward svc/todo-app -n hpa-demo 8081:8081
Forwarding from 127.0.0.1:8081 -> 3000
Forwarding from [::1]:8081 -> 3000

```

### Auto scale

**Get load test tool**

You can use any available load testing/benchmarking tools but we are using a simple tool called **hey** in this workshop.

- Download the hey package for your operating system.
- Set executable permission and copy the file to a executable path (eg: ln -s ~/Downloads/hey_linux_amd64 ~/.local/bin/)

Check [**hey**](https://github.com/rakyll/hey) repo for more details.


```shell
$ kubectl apply -f hpa/todo-hpa.yaml
horizontalpodautoscaler.autoscaling/todo-hpa created

$ kubectl get hpa -n hpa-demo
NAME       REFERENCE             TARGETS              MINPODS   MAXPODS   REPLICAS   AGE
todo-hpa   Deployment/todo-app   cpu: <unknown>/80%   1         5         0          6s


$ kubectl port-forward svc/todo-app -n hpa-demo 8081:8081
Forwarding from 127.0.0.1:8081 -> 3000
Forwarding from [::1]:8081 -> 3000

$ hey -z 4m -c 25 http://localhost:8081

$ kubectl get po -n hpa-demo
NAME                        READY   STATUS    RESTARTS   AGE
todo-app-5cfb496d77-5kc27   1/1     Running   0          2m9s
todo-app-5cfb496d77-l6r69   1/1     Running   0          11m
todo-app-5cfb496d77-pb7tx   1/1     Running   0          2m9s
```

```shell
$ watch 'kubectl get po -n hpa-demo;kubectl top pods -n hpa-demo'
Every 2.0s: kubectl get po -n hpa-demo;kubectl top pods -n hpa-demo

NAME                        READY   STATUS    RESTARTS   AGE
todo-app-5cfb496d77-5kc27   1/1     Running   0          76s
todo-app-5cfb496d77-l6r69   1/1     Running   0          10m
todo-app-5cfb496d77-pb7tx   1/1     Running   0          76s
NAME                        CPU(cores)   MEMORY(bytes)
todo-app-5cfb496d77-5kc27   10m          14Mi
todo-app-5cfb496d77-l6r69   100m         48Mi
todo-app-5cfb496d77-pb7tx   7m           14Mi
```

```shell
$ kubectl describe deployments.apps todo-app -n hpa-demo
Name:                   todo-app
...<removed for brevity>...
Replicas:               3 desired | 3 updated | 3 total | 3 available | 0 unavailable
StrategyType:           RollingUpdate
...<removed for brevity>...
Events:
  Type    Reason             Age   From                   Message
  ----    ------             ----  ----                   -------
  Normal  ScalingReplicaSet  16m   deployment-controller  Scaled up replica set todo-app-749854577d to 1
  Normal  ScalingReplicaSet  13m   deployment-controller  Scaled up replica set todo-app-5cfb496d77 to 1
  Normal  ScalingReplicaSet  13m   deployment-controller  Scaled down replica set todo-app-749854577d to 0 from 1
  Normal  ScalingReplicaSet  4m9s  deployment-controller  Scaled up replica set todo-app-5cfb496d77 to 3 from 1
```

```shell
$ kubectl delete namespaces hpa-demo
namespace "hpa-demo" deleted
```

## Cluster Autoscaling

### GKE


Preparations

```shell
$ gcloud config set compute/region us-central1-a
```

```shell
$ gcloud container clusters create k8sforbeginners --num-nodes=2 --zone=us-central1-a --enable-autoscaling --min-nodes=2 --max-nodes=10

$ gcloud container clusters create k8sbible \
  --enable-autoscaling \
  --num-nodes 2 \
  --min-nodes 2 \
  --max-nodes 10 \
  --region=us-central1-a
...<removed for brevity>...
Creating cluster k8sbible in us-central1-a... Cluster is being health-checked (master is healthy)...done.
Created [https://container.googleapis.com/v1/projects/k8sbible-project/zones/us-central1-a/clusters/k8sbible].
To inspect the contents of your cluster, go to: https://console.cloud.google.com/kubernetes/workload_/gcloud/us-central1-a/k8sbible?project=k8sbible-project
kubeconfig entry generated for k8sbible.
NAME      LOCATION       MASTER_VERSION      MASTER_IP      MACHINE_TYPE  NODE_VERSION        NUM_NODES  STATUS
k8sbible  us-central1-a  1.29.7-gke.1008000  <removed>      e2-medium     1.29.7-gke.1008000  3          RUNNING
```
Verify

```shell
$ gcloud container node-pools describe default-pool --cluster=k8sdemo |grep autoscaling -A 1
autoscaling:
  enabled: true
```
### AKS

```shell
$ az aks create --resource-group k8sforbeginners-rg \
  --name k8sforbeginners-aks \
  --node-count 1 \
  --enable-cluster-autoscaler \
  --min-count 1 \
  --max-count 3 \
  --vm-set-type VirtualMachineScaleSets \
  --load-balancer-sku standard \
  --generate-ssh-keys
```

### Implement CA

```shell
$ kubectl get nodes -o custom-columns=NAME:.metadata.name,CPU_ALLOCATABLE:.status.allocatable.cpu,MEMORY_ALLOCATABLE:.status.allocatable.memory
NAME                                     CPU_ALLOCATABLE   MEMORY_ALLOCATABLE
gke-k8sdemo-default-pool-1bf4f185-6422   940m              2873304Ki
gke-k8sdemo-default-pool-1bf4f185-csv0   940m              2873312Ki
```


```shell
$ kubectl apply -f ca/
namespace/ca-demo created
role.rbac.authorization.k8s.io/deployment-reader created
deployment.apps/elastic-hamster created
horizontalpodautoscaler.autoscaling/elastic-hamster-hpa created
serviceaccount/elastic-hamster created
rolebinding.rbac.authorization.k8s.io/read-deployments created
```

```shell
$ kubectl top pod -n ca-demo
NAME                              CPU(cores)   MEMORY(bytes)
elastic-hamster-87d4db7fd-59lcd   1292m        65Mi
elastic-hamster-87d4db7fd-9kzhp   1272m        67Mi
elastic-hamster-87d4db7fd-cwzs7   1280m        67Mi
elastic-hamster-87d4db7fd-fvlm7   1262m        66Mi
elastic-hamster-87d4db7fd-g5xvx   1302m        66Mi
elastic-hamster-87d4db7fd-kf7kx   1310m        66Mi
elastic-hamster-87d4db7fd-sbnzc   1262m        67Mi
elastic-hamster-87d4db7fd-twb86   1300m        67Mi
```

```shell
$  kubectl top nodes
NAME                                     CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%
gke-k8sdemo-default-pool-1bf4f185-6422   196m         20%    1220Mi          43%
gke-k8sdemo-default-pool-1bf4f185-csv0   199m         21%    1139Mi          40%
gke-k8sdemo-default-pool-1bf4f185-fcsd   751m         79%    935Mi           33%
gke-k8sdemo-default-pool-1bf4f185-frq6   731m         77%    879Mi           31%
gke-k8sdemo-default-pool-1bf4f185-h8hw   742m         78%    846Mi           30%
gke-k8sdemo-default-pool-1bf4f185-j99r   733m         77%    923Mi           32%
gke-k8sdemo-default-pool-1bf4f185-k6xq   741m         78%    986Mi           35%
gke-k8sdemo-default-pool-1bf4f185-vq55   732m         77%    940Mi           33%
gke-k8sdemo-default-pool-1bf4f185-wh66   732m         77%    819Mi           29%
gke-k8sdemo-default-pool-1bf4f185-xdpr   742m         78%    921Mi           32%
```

Scale down

```shell
$ kubectl patch hpa elastic-hamster-hpa -n ca-demo -p '{"spec": {"maxReplicas": 2}}'
horizontalpodautoscaler.autoscaling/elastic-hamster-hpa patched
```

```shell
$ kubectl get pod -n ca-demo
NAME                              READY   STATUS    RESTARTS   AGE
elastic-hamster-87d4db7fd-2qghf   1/1     Running   0          20m
elastic-hamster-87d4db7fd-mdvpx   1/1     Running   0          19m

$ kubectl get nodes
NAME                                     STATUS   ROLES    AGE    VERSION
gke-k8sdemo-default-pool-1bf4f185-6422   Ready    <none>   145m   v1.29.7-gke.1008000
gke-k8sdemo-default-pool-1bf4f185-csv0   Ready    <none>   145m   v1.29.7-gke.1008000
```