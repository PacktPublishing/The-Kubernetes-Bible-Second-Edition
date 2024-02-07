# Using Multi-Container Pods and Design Patterns 

Creating multi-container Pod

```shell
$ kubectl create -f multi-container-pod.yaml 
pod/multi-container-pod created


$ kubectl get pod 
NAME                  READY   STATUS    RESTARTS   AGE 
multi-container-pod   2/2     Running   0          2m7s 

$ kubectl logs multi-container-pod -c debian-container 
Mon Jan  8 01:33:23 UTC 2024 
debian-container 
Mon Jan  8 01:33:28 UTC 2024 
debian-container 
...<removed for brevity>... 
 
$ kubectl logs multi-container-pod -c nginx-container 
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration 
...<removed for brevity>... 
2024/01/08 01:33:20 [notice] 1#1: start worker process 39 
2024/01/08 01:33:20 [notice] 1#1: start worker process 40 
```
Testing multi-container Pod with invalid image

```shell
$ kubectl apply -f failed-multi-container-pod.yaml  
pod/failed-multi-container-pod created 

$ kubectl get pod  
NAME                         READY   STATUS             RESTARTS   AGE 
failed-multi-container-pod   1/2     ImagePullBackOff   0          93s 
```

Deleting multi-container pods

```shell
$ kubectl delete -f multi-container-pod.yaml 

## Otherwise, if you already know the Pod's name, you can do this as follows: 
$ kubectl delete pods/multi-pod 

## or equivalent 
$ kubectl delete pods multi-pod 

$  kubectl delete pod failed-multi-container-pod --grace-period=0 --force
Warning: Immediate deletion does not wait for confirmation that the running resource has been terminated. The resource may continue to run on the cluster indefinitely.
pod "failed-multi-container-pod" force deleted
```

Accessing Container

```shell
$  kubectl describe pod multi-container-pod 
Name:             multi-container-pod
Namespace:        default
Priority:         0
Service Account:  default
Node:             minikube/192.168.49.2
Start Time:       Tue, 30 Jan 2024 22:47:32 +0800
Labels:           <none>
Annotations:      <none>
Status:           Running
IP:               10.244.0.34
IPs:
  IP:  10.244.0.34
Containers:
  nginx-container:
    Container ID:   docker://d2211148f9932619f667cbecfa471fd8bb1ac813fd52b0f68f18a5b5143063d1
    Image:          nginx:latest
    Image ID:       docker-pullable://nginx@sha256:4c0fdaa8b6341bfdeca5f18f7837462c80cff90527ee35ef185571e1c327beac
    Port:           <none>
    Host Port:      <none>
    State:          Running
      Started:      Tue, 30 Jan 2024 22:47:36 +0800
    Ready:          True
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-lbkc9 (ro)
  debian-container:
    Container ID:  docker://9640c772c1644c4858086ec206a162e656446240b5363d9c2285212f9ee8e312
    Image:         debian
    Image ID:      docker-pullable://debian@sha256:b16cef8cbcb20935c0f052e37fc3d38dc92bfec0bcfb894c328547f81e932d67
    Port:          <none>
    Host Port:     <none>
    Command:
      /bin/sh
    Args:
      -c
      while true; do date;echo debian-container; sleep 5 ; done
    State:          Running
      Started:      Tue, 30 Jan 2024 22:47:39 +0800
    Ready:          True
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-lbkc9 (ro)
Conditions:
  Type                        Status
  PodReadyToStartContainers   True 
  Initialized                 True 
  Ready                       True 
  ContainersReady             True 
  PodScheduled                True 
Volumes:
  kube-api-access-lbkc9:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  3607
    ConfigMapName:           kube-root-ca.crt
    ConfigMapOptional:       <nil>
    DownwardAPI:             true
QoS Class:                   BestEffort
Node-Selectors:              <none>
Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                             node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:
  Type    Reason     Age   From               Message
  ----    ------     ----  ----               -------
  Normal  Scheduled  97s   default-scheduler  Successfully assigned default/multi-container-pod to minikube
  Normal  Pulling    97s   kubelet            Pulling image "nginx:latest"
  Normal  Pulled     94s   kubelet            Successfully pulled image "nginx:latest" in 2.661s (2.661s including waiting)
  Normal  Created    94s   kubelet            Created container nginx-container
  Normal  Started    94s   kubelet            Started container nginx-container
  Normal  Pulling    94s   kubelet            Pulling image "debian"
  Normal  Pulled     92s   kubelet            Successfully pulled image "debian" in 2.599s (2.599s including waiting)
  Normal  Created    91s   kubelet            Created container debian-container
  Normal  Started    91s   kubelet            Started container debian-container
```

```shell
$ kubectl get pod/multi-container-pod -o jsonpath="{.spec.containers[*].name}"
nginx-container debian-container

$ kubectl exec -it multi-container-pod --container nginx-container -- /bin/bash
root@multi-container-pod:/# hostname 
multi-container-pod
root@multi-container-pod:/# 
```

```shell
$  kubectl exec pods/multi-container-pod -c nginx-container -- ls
bin
boot
dev
docker-entrypoint.d
docker-entrypoint.sh
etc
home
lib
lib32
lib64
libx32
media
mnt
opt
proc
root
run
sbin
srv
sys
tmp
usr
var
```

```shell
 $ kubectl create -f nginx-debian-with-custom-command-and-args.yaml 
pod/nginx-debian-with-custom-command-and-args created

$ kubectl get po -w
NAME                                        READY   STATUS              RESTARTS   AGE
nginx-debian-with-custom-command-and-args   0/2     ContainerCreating   0          2s
nginx-debian-with-custom-command-and-args   2/2     Running             0          6s
nginx-debian-with-custom-command-and-args   1/2     NotReady            0          66s
```


```shell
$ kubectl create -f nginx-with-init-container.yaml 
pod/nginx-with-init-container created

$ kubectl get po -w
NAME                        READY   STATUS     RESTARTS   AGE
nginx-with-init-container   0/1     Init:0/1   0          3s
nginx-with-init-container   0/1     Init:0/1   0          4s
nginx-with-init-container   0/1     PodInitializing   0          19s
nginx-with-init-container   1/1     Running           0          22s
```

```shell
$ kubectl logs multi-container-pod 
Defaulted container "nginx-container" out of: nginx-container, debian-container
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
/docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
/docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
/docker-entrypoint.sh: Configuration complete; ready for start up
2024/02/04 16:35:55 [notice] 1#1: using the "epoll" event method
2024/02/04 16:35:55 [notice] 1#1: nginx/1.25.3
2024/02/04 16:35:55 [notice] 1#1: built by gcc 12.2.0 (Debian 12.2.0-14) 
2024/02/04 16:35:55 [notice] 1#1: OS: Linux 6.6.8-200.fc39.x86_64
2024/02/04 16:35:55 [notice] 1#1: getrlimit(RLIMIT_NOFILE): 1048576:1048576
2024/02/04 16:35:55 [notice] 1#1: start worker processes
2024/02/04 16:35:55 [notice] 1#1: start worker process 29
2024/02/04 16:35:55 [notice] 1#1: start worker process 30
2024/02/04 16:35:55 [notice] 1#1: start worker process 31
2024/02/04 16:35:55 [notice] 1#1: start worker process 32
2024/02/04 16:35:55 [notice] 1#1: start worker process 33
2024/02/04 16:35:55 [notice] 1#1: start worker process 34
2024/02/04 16:35:55 [notice] 1#1: start worker process 35
2024/02/04 16:35:55 [notice] 1#1: start worker process 36
2024/02/04 16:35:55 [notice] 1#1: start worker process 37
2024/02/04 16:35:55 [notice] 1#1: start worker process 38
2024/02/04 16:35:55 [notice] 1#1: start worker process 39
2024/02/04 16:35:55 [notice] 1#1: start worker process 40
```

## Volumes

```shell
$ kubectl create -f multi-container-with-emptydir-pod.yaml 
pod/multi-container-with-emptydir-pod created

$ kubectl get po
NAME                                READY   STATUS    RESTARTS   AGE
multi-container-with-emptydir-pod   2/2     Running   0          25s
```

```shell
$  kubectl exec multi-container-with-emptydir-pod -c debian-container -- ls /var
backups
cache
i-am-empty-dir-volume
lib
local
lock
log
mail
opt
run
spool
tmp
```

```shell
$  kubectl exec multi-container-with-emptydir-pod -c debian-container -- bin/sh -c "echo 'hello world' >> /var/i-am-empty-dir-volume/hello-world.txt" 

$ kubectl exec multi-container-with-emptydir-pod -c nginx-container -- cat /var/i-am-empty-dir-volume/hello-world.txt
hello world

$ kubectl exec multi-container-with-emptydir-pod -c debian-container -- cat /var/i-am-empty-dir-volume/hello-world.txt
hello world
```

Hostpath Volume

```shell
$ echo "Hello World" >> /tmp/hello-world.txt 
```