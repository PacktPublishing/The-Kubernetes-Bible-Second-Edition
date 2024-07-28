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
$ kubectl apply -f 01_resource-requests-and-limits/nginx-deployment.yaml
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