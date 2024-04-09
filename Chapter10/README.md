# Running Production-Grade Kubernetes Workloads


```shell
$ kubectl get nodes
NAME                 STATUS   ROLES           AGE   VERSION
kind-control-plane   Ready    control-plane   27s   v1.27.3
kind-worker          Ready    <none>          8s    v1.27.3
kind-worker2         Ready    <none>          8s    v1.27.3
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
$ kubectl describe replicaset/nginx-replicaset-example
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
Events:           <none>
```

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