# Running Production-Grade Kubernetes Workloads

```shell
$ kind create cluster --config Chapter03/kind_cluster --image kindest/node:v1.31.0

$ kubectl get nodes
NAME                 STATUS   ROLES           AGE   VERSION
kind-control-plane   Ready    control-plane   60s   v1.31.0
kind-worker          Ready    <none>          47s   v1.31.0
kind-worker2         Ready    <none>          47s   v1.31.0
kind-worker3         Ready    <none>          47s   v1.31.0
```

Create replicationcontroller

```shell
$ kubectl create -f nginx-replicationcontroller.yaml
replicationcontroller/nginx-replicationcontroller-example created

$ kubectl get replicationcontroller/nginx-replicationcontroller-example
NAME                                  DESIRED   CURRENT   READY   AGE
nginx-replicationcontroller-example   3         3         3       3m35s

$ kubectl get po
NAME                                        READY   STATUS    RESTARTS   AGE
nginx-replicationcontroller-example-g8cwg   1/1     Running   0          4m51s
nginx-replicationcontroller-example-ht22x   1/1     Running   0          4m51s
nginx-replicationcontroller-example-nst9z   1/1     Running   0          4m51s

$ kubectl get po -o wide
NAME                                        READY   STATUS    RESTARTS   AGE     IP           NODE           NOMINATED NODE   READINESS GATES
nginx-replicationcontroller-example-g8cwg   1/1     Running   0          2m19s   10.244.2.2   kind-worker2   <none>           <none>
nginx-replicationcontroller-example-ht22x   1/1     Running   0          2m19s   10.244.2.3   kind-worker2   <none>           <none>
nginx-replicationcontroller-example-nst9z   1/1     Running   0          2m19s   10.244.1.2   kind-worker    <none>           <none>
```

Checking replicationcontroller

```shell
$ kubectl delete po nginx-replicationcontroller-example-g8cwg
pod "nginx-replicationcontroller-example-g8cwg" deleted

$  kubectl describe rc/nginx-replicationcontroller-example
Name:         nginx-replicationcontroller-example
Namespace:    default
Selector:     app=nginx,environment=test
Labels:       app=nginx
              environment=test
Annotations:  <none>
Replicas:     3 current / 3 desired
Pods Status:  3 Running / 0 Waiting / 0 Succeeded / 0 Failed
Pod Template:
  Labels:  app=nginx
           environment=test
  Containers:
   nginx:
    Image:        nginx:1.17
    Port:         80/TCP
    Host Port:    0/TCP
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Events:
  Type    Reason            Age    From                    Message
  ----    ------            ----   ----                    -------
  Normal  SuccessfulCreate  8m42s  replication-controller  Created pod: nginx-replicationcontroller-example-nst9z
  Normal  SuccessfulCreate  8m42s  replication-controller  Created pod: nginx-replicationcontroller-example-g8cwg
  Normal  SuccessfulCreate  8m42s  replication-controller  Created pod: nginx-replicationcontroller-example-ht22x
  Normal  SuccessfulCreate  90s    replication-controller  Created pod: nginx-replicationcontroller-example-mrfh5
```


```shell
$ kubectl scale rc/nginx-replicationcontroller-example --replicas=5
```

## ReplicaSet

```shell
$ kubectl create -f ns-rs.yaml
namespace/rs-ns created
```

```shell
$ kubectl apply -f nginx-replicaset-example.yaml
replicaset.apps/nginx-replicaset-example created
```

```shell
$ kubectl describe replicaset/nginx-replicaset-example -n rs-ns
Name:         nginx-replicaset-example
Namespace:    rs-ns
Selector:     app=nginx,environment=test
Labels:       <none>
Annotations:  <none>
Replicas:     4 current / 4 desired
Pods Status:  4 Running / 0 Waiting / 0 Succeeded / 0 Failed
Pod Template:
  Labels:  app=nginx
           environment=test
  Containers:
   nginx:
    Image:         nginx:1.17
    Port:          80/TCP
    Host Port:     0/TCP
    Environment:   <none>
    Mounts:        <none>
  Volumes:         <none>
  Node-Selectors:  <none>
  Tolerations:     <none>
Events:
  Type    Reason            Age   From                   Message
  ----    ------            ----  ----                   -------
  Normal  SuccessfulCreate  84s   replicaset-controller  Created pod: nginx-replicaset-example-cfcfs
  Normal  SuccessfulCreate  84s   replicaset-controller  Created pod: nginx-replicaset-example-6qc9p
  Normal  SuccessfulCreate  84s   replicaset-controller  Created pod: nginx-replicaset-example-kw7cl
  Normal  SuccessfulCreate  84s   replicaset-controller  Created pod: nginx-replicaset-example-r2qfn
```

Delete a Pod

```shell
$ kubectl delete po nginx-replicaset-example-6qc9p -n rs-ns
pod "nginx-replicaset-example-6qc9p" deleted
```

```shell
$ kubectl describe rs/nginx-replicaset-example -n rs-ns

Events:
  Type    Reason            Age   From                   Message
  ----    ------            ----  ----                   -------
  Normal  SuccessfulCreate  9m9s  replicaset-controller  Created pod: nginx-replicaset-example-cfcfs
  Normal  SuccessfulCreate  9m9s  replicaset-controller  Created pod: nginx-replicaset-example-6qc9p
  Normal  SuccessfulCreate  9m9s  replicaset-controller  Created pod: nginx-replicaset-example-kw7cl
  Normal  SuccessfulCreate  9m9s  replicaset-controller  Created pod: nginx-replicaset-example-r2qfn
  Normal  SuccessfulCreate  3m1s  replicaset-controller  Created pod: nginx-replicaset-example-krdrs
```

Test with Bare Pods

```shell
$ kubectl create -f nginx-pod-bare.yaml
pod/nginx-pod-bare-example created

$ kubectl  get pods
NAME                             READY   STATUS        RESTARTS   AGE
nginx-pod-bare-example           0/1     Terminating   0          1s
nginx-replicaset-example-74kq9   1/1     Running       0          23h
nginx-replicaset-example-qfvx6   1/1     Running       0          23h
nginx-replicaset-example-s5cwc   1/1     Running       0          23h

$ kubectl describe rs/nginx-replicaset-example
Name:         nginx-replicaset-example
Namespace:    default
Selector:     app=nginx,environment=test
Labels:       <none>
Annotations:  <none>
Replicas:     3 current / 3 desired
Pods Status:  3 Running / 0 Waiting / 0 Succeeded / 0 Failed
Pod Template:
  Labels:  app=nginx
           environment=test
  Containers:
   nginx:
    Image:        nginx:1.17
    Port:         80/TCP
    Host Port:    0/TCP
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Events:
  Type    Reason            Age                From                   Message
  ----    ------            ----               ----                   -------
  Normal  SuccessfulDelete  56s (x3 over 26m)  replicaset-controller  Deleted pod: nginx-pod-bare-example
```

## HA and FT

```shell
$ kubectl apply -f nginx-service.yaml
service/nginx-service created
```

```shell
$ kubectl port-forward svc/nginx-service 8080:80 -n rs-ns
Forwarding from 127.0.0.1:8080 -> 80
Forwarding from [::1]:8080 -> 80
```

```shell
$ kubectl get po -n rs-ns -o wide
NAME                             READY   STATUS    RESTARTS   AGE   IP           NODE           NOMINATED NODE   READINESS GATES
nginx-replicaset-example-cfcfs   1/1     Running   0          24m   10.244.1.3   kind-worker2   <none>           <none>
nginx-replicaset-example-krdrs   1/1     Running   0          17m   10.244.3.5   kind-worker    <none>           <none>
nginx-replicaset-example-kw7cl   1/1     Running   0          24m   10.244.3.4   kind-worker    <none>           <none>
nginx-replicaset-example-r2qfn   1/1     Running   0          24m   10.244.2.4   kind-worker3   <none>           <none>
```

Remove node

```shell
$ kubectl cordon kind-worker
node/kind-worker cordoned

$ kubectl drain kind-worker --ignore-daemonsets
node/kind-worker already cordoned
Warning: ignoring DaemonSet-managed Pods: kube-system/kindnet-t52g7, kube-system/kube-proxy-m74ln
evicting pod rs-ns/nginx-replicaset-example-kw7cl
evicting pod rs-ns/nginx-replicaset-example-krdrs
pod/nginx-replicaset-example-krdrs evicted
pod/nginx-replicaset-example-kw7cl evicted
node/kind-worker drained

$ kubectl delete node kind-worker
node "kind-worker" deleted
```

```shell
$ kubectl get po -n rs-ns -o wide
NAME                             READY   STATUS    RESTARTS   AGE     IP           NODE           NOMINATED NODE   READINESS GATES
nginx-replicaset-example-8lz9x   1/1     Running   0          2m33s   10.244.1.4   kind-worker2   <none>           <none>
nginx-replicaset-example-cfcfs   1/1     Running   0          30m     10.244.1.3   kind-worker2   <none>           <none>
nginx-replicaset-example-d8rz5   1/1     Running   0          2m33s   10.244.2.5   kind-worker3   <none>           <none>
nginx-replicaset-example-r2qfn   1/1     Running   0          30m     10.244.2.4   kind-worker3   <none>           <none>
```

ReplicaSet with Liveness

```shell
$ kubectl apply -f ./nginx-replicaset-livenessprobe.yaml

$ kubectl get po
NAME                                           READY   STATUS    RESTARTS   AGE
nginx-replicaset-livenessprobe-example-lgvqv   1/1     Running   0          3s
nginx-replicaset-livenessprobe-example-md2s4   1/1     Running   0          3s
nginx-replicaset-livenessprobe-example-n2xxg   1/1     Running   0          3s

$ kubectl exec -it nginx-replicaset-livenessprobe-example-lgvqv -- rm /usr/share/nginx/html/index.html

$ kubectl describe pod/nginx-replicaset-livenessprobe-example-lgvqv
Name:             nginx-replicaset-livenessprobe-example-lgvqv
...<removed for brevitt>...
Events:
  Type     Reason     Age                 From               Message
  ----     ------     ----                ----               -------
  Normal   Scheduled  2m9s                default-scheduler  Successfully assigned default/nginx-replicaset-livenessprobe-example-lgvqv to kind-worker2
  Normal   Pulled     60s (x2 over 2m8s)  kubelet            Container image "nginx:1.17" already present on machine
  Normal   Created    60s (x2 over 2m8s)  kubelet            Created container nginx
  Normal   Started    60s (x2 over 2m8s)  kubelet            Started container nginx
  Warning  Unhealthy  60s (x3 over 64s)   kubelet            Liveness probe failed: HTTP probe failed with statuscode: 403
  Normal   Killing    60s                 kubelet            Container nginx failed liveness probe, will be restarted
```

Delete

```shell
$ kubectl delete rs/nginx-replicaset-livenessprobe-example --cascade=orphan
```