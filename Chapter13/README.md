# DaemonSet – Maintaining Pod Singletons on Nodes


## Create multi-node minikube

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
minikube       Ready    control-plane   3m28s   v1.30.0
minikube-m02   Ready    <none>          2m29s   v1.30.0
minikube-m03   Ready    <none>          91s     v1.30.0
```

## Create multi-master minikube

```shell
$ minikube start \
  --driver=virtualbox \
  --nodes 5 \
  --ha \
  --cni calico \
  --cpus=2 \
  --memory=2g \
  --kubernetes-version=v1.30.0 \
  --container-runtime=containerd


$ kubectl get nodes
NAME           STATUS   ROLES           AGE     VERSION
minikube       Ready    control-plane   6m28s   v1.30.0
minikube-m02   Ready    control-plane   4m36s   v1.30.0
minikube-m03   Ready    control-plane   2m45s   v1.30.0
minikube-m04   Ready    <none>          112s    v1.30.0
minikube-m05   Ready    <none>          62s     v1.30.0
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

```shell
$ kubectl apply -f fluentd-daemonset.yaml
namespace/logging created
daemonset.apps/fluentd-elasticsearch created
```

```shell
$  kubectl describe daemonset fluentd-elasticsearch -n logging
Name:           fluentd-elasticsearch
Selector:       name=fluentd-elasticsearch
Node-Selector:  <none>
Labels:         k8s-app=fluentd-logging
Annotations:    deprecated.daemonset.template.generation: 1
Desired Number of Nodes Scheduled: 3
Current Number of Nodes Scheduled: 3
Number of Nodes Scheduled with Up-to-date Pods: 3
Number of Nodes Scheduled with Available Pods: 3
Number of Nodes Misscheduled: 0
Pods Status:  3 Running / 0 Waiting / 0 Succeeded / 0 Failed
Pod Template:
  Labels:  name=fluentd-elasticsearch
  Containers:
   fluentd-elasticsearch:
    Image:      quay.io/fluentd_elasticsearch/fluentd:v4.7
    Port:       <none>
    Host Port:  <none>
    Limits:
      memory:  200Mi
    Requests:
      cpu:        100m
      memory:     200Mi
    Environment:  <none>
    Mounts:
      /var/log from varlog (rw)
  Volumes:
   varlog:
    Type:          HostPath (bare host directory volume)
    Path:          /var/log
    HostPathType:
Events:
  Type    Reason            Age    From                  Message
  ----    ------            ----   ----                  -------
  Normal  SuccessfulCreate  2m47s  daemonset-controller  Created pod: fluentd-elasticsearch-cs4hm
  Normal  SuccessfulCreate  2m47s  daemonset-controller  Created pod: fluentd-elasticsearch-zk6pt
  Normal  SuccessfulCreate  2m47s  daemonset-controller  Created pod: fluentd-elasticsearch-stfqs
```

```shell
$ kubectl get po -n logging -o wide
NAME                          READY   STATUS    RESTARTS   AGE     IP               NODE           NOMINATED NODE   READINESS GATES
fluentd-elasticsearch-cs4hm   1/1     Running   0          3m48s   10.244.120.68    minikube       <none>           <none>
fluentd-elasticsearch-stfqs   1/1     Running   0          3m48s   10.244.205.194   minikube-m02   <none>           <none>
fluentd-elasticsearch-zk6pt   1/1     Running   0          3m48s   10.244.151.2     minikube-m03   <none>           <none>
```

Check log files mounted inside containers.

```shell
$ kubectl exec -n logging -it fluentd-elasticsearch-cs4hm -- /bin/bash
root@fluentd-elasticsearch-cs4hm:/# ls -l /var/log/
total 20
drwxr-xr-x  3 root root 4096 May 29 10:56 calico
drwxr-xr-x  2 root root 4096 May 29 12:40 containers
drwx------  3 root root 4096 May 29 10:55 crio
drwxr-xr-x  2 root root 4096 May 29 11:53 journal
drwxr-x--- 12 root root 4096 May 29 12:40 pods
root@fluentd-elasticsearch-cs4hm:/#
```

## Modify DaemonSet

```shell
$ kubectl apply -f fluentd-daemonset.yaml
namespace/logging unchanged
daemonset.apps/fluentd-elasticsearch configured

$ kubectl rollout status ds -n logging
Waiting for daemon set "fluentd-elasticsearch" rollout to finish: 2 out of 3 new pods have been updated...
Waiting for daemon set "fluentd-elasticsearch" rollout to finish: 2 out of 3 new pods have been updated...
Waiting for daemon set "fluentd-elasticsearch" rollout to finish: 2 of 3 updated pods are available...
daemon set "fluentd-elasticsearch" successfully rolled out
```

```shell
$ kubectl describe ds -n logging
Name:           fluentd-elasticsearch
Selector:       name=fluentd-elasticsearch
Node-Selector:  <none>
Labels:         k8s-app=fluentd-logging
Annotations:    deprecated.daemonset.template.generation: 2
Desired Number of Nodes Scheduled: 3
Current Number of Nodes Scheduled: 3
Number of Nodes Scheduled with Up-to-date Pods: 3
Number of Nodes Scheduled with Available Pods: 3
Number of Nodes Misscheduled: 0
Pods Status:  3 Running / 0 Waiting / 0 Succeeded / 0 Failed
Pod Template:
  Labels:  name=fluentd-elasticsearch
  Containers:
   fluentd-elasticsearch:
    Image:      quay.io/fluentd_elasticsearch/fluentd:v4.7.5
    Port:       <none>
    Host Port:  <none>
    Limits:
      memory:  200Mi
    Requests:
      cpu:     100m
      memory:  200Mi
    Environment:
      FLUENT_ELASTICSEARCH_HOST:         elasticsearch-logging
      FLUENT_ELASTICSEARCH_PORT:         9200
      FLUENT_ELASTICSEARCH_SSL_VERIFY:   true
      FLUENT_ELASTICSEARCH_SSL_VERSION:  TLSv1_2
    Mounts:
      /var/log from varlog (rw)
  Volumes:
   varlog:
    Type:          HostPath (bare host directory volume)
    Path:          /var/log
    HostPathType:
Events:
  Type    Reason            Age    From                  Message
  ----    ------            ----   ----                  -------
  Normal  SuccessfulDelete  6m7s   daemonset-controller  Deleted pod: fluentd-elasticsearch-cs4hm
  Normal  SuccessfulCreate  6m5s   daemonset-controller  Created pod: fluentd-elasticsearch-62cvj
  Normal  SuccessfulDelete  6m     daemonset-controller  Deleted pod: fluentd-elasticsearch-stfqs
  Normal  SuccessfulCreate  5m58s  daemonset-controller  Created pod: fluentd-elasticsearch-24v2z
  Normal  SuccessfulDelete  5m52s  daemonset-controller  Deleted pod: fluentd-elasticsearch-zk6pt
  Normal  SuccessfulCreate  5m51s  daemonset-controller  Created pod: fluentd-elasticsearch-fxffp
```

## Rollbakck

```shell
$ kubectl rollout undo daemonsetfluentd-elasticsearch -n logging
```

## Delete

```shell
$ kubectl delete ds fluentd-elasticsearch -nlogging
```
