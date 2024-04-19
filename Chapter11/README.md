# Deploying Stateless Applications

## Create Deployment

Create Skeleton

```shell
$ kubectl create deployment my-deployment --replicas=1 --image=my-image:latest --dry-run=client --port=80 -o yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: my-deployment
  name: my-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-deployment
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: my-deployment
    spec:
      containers:
      - image: my-image:latest
        name: my-image
        ports:
        - containerPort: 80
        resources: {}
```

```shell
$ kubectl apply -f ./nginx-deployment.yaml

$ kubectl rollout status deployment nginx-deployment-example
Waiting for deployment "nginx-deployment-example" rollout to finish: 0 of 3 updated replicas are available...
deployment "nginx-deployment-example" successfully rolled out

$ kubectl get deploy nginx-deployment-example
NAME                       READY   UP-TO-DATE   AVAILABLE   AGE
nginx-deployment-example   3/3     3            3           80s

$ kubectl get rs
NAME                                  DESIRED   CURRENT   READY   AGE
nginx-deployment-example-5b8dc6b8cd   3         3         3       2m17s

$ kubectl get pods
NAME                                        READY   STATUS    RESTARTS   AGE
nginx-deployment-example-5b8dc6b8cd-lj2bz   1/1     Running   0          3m30s
nginx-deployment-example-5b8dc6b8cd-nxkbj   1/1     Running   0          3m30s
nginx-deployment-example-5b8dc6b8cd-shzmd   1/1     Running   0          3m30s
```

## Create Service

```shell
$ kubectl apply -f nginx-service.yaml
service/nginx-service-example created

$ kubectl describe service nginx-service-example
Name:                     nginx-service-example
Namespace:                default
Labels:                   <none>
Annotations:              <none>
Selector:                 app=nginx,environment=test
Type:                     LoadBalancer
IP Family Policy:         SingleStack
IP Families:              IPv4
IP:                       10.96.231.126
IPs:                      10.96.231.126
Port:                     <unset>  80/TCP
TargetPort:               80/TCP
NodePort:                 <unset>  32563/TCP
Endpoints:                10.244.1.2:80,10.244.2.2:80,10.244.2.3:80
Session Affinity:         None
External Traffic Policy:  Cluster
Events:                   <none>
```

```shell
$ kubectl apply -f ../Chapter07/k8sutils.yaml
pod/k8sutils created

$ kubectl exec -it k8sutils -- curl nginx-service-example.default.svc.cluster.local |grep Welcome -A2
<title>Welcome to nginx!</title>
<style>
    body {
--
  <h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>
```

## Expose the Deployment

```shell
$ kubectl expose deployment --type=LoadBalancer nginx-deployment-example
service/nginx-deployment-example exposed
```

```shell
$ kubectl describe svc nginx-service-example
Name:                     nginx-service-example
Namespace:                default
Labels:                   <none>
Annotations:              <none>
Selector:                 app=nginx,environment=test
Type:                     LoadBalancer
IP Family Policy:         SingleStack
IP Families:              IPv4
IP:                       10.96.231.126
IPs:                      10.96.231.126
Port:                     <unset>  80/TCP
TargetPort:               80/TCP
NodePort:                 <unset>  32563/TCP
Endpoints:                10.244.1.6:80,10.244.1.7:80,10.244.2.6:80
Session Affinity:         None
External Traffic Policy:  Cluster
Events:                   <none>


$ kubectl describe svc nginx-service-example |grep Endpoint
Endpoints:                10.244.1.6:80,10.244.2.6:80
```

```shell
$  kubectl describe pod nginx-deployment-readiness-69dd4cfdd9-4pkwr
Name:             nginx-deployment-readiness-69dd4cfdd9-4pkwr
Namespace:        default
Priority:         0
Service Account:  default
Node:             my-kind-cluster-worker2/172.18.0.2
Start Time:       Tue, 16 Apr 2024 22:19:25 +0800
Labels:           app=nginx
                  environment=test
                  pod-template-hash=69dd4cfdd9
Annotations:      <none>
Status:           Running
IP:               10.244.1.7
IPs:
  IP:           10.244.1.7
Controlled By:  ReplicaSet/nginx-deployment-readiness-69dd4cfdd9
Containers:
  nginx:
    Container ID:  containerd://bde1066155d85ccaa75e39a64fab92f52b920e3b52c319cde71ca6a8b86c4a2e
    Image:         nginx:1.25.4
    Image ID:      docker.io/library/nginx@sha256:9ff236ed47fe39cf1f0acf349d0e5137f8b8a6fd0b46e5117a401010e56222e1
    Port:          80/TCP
    Host Port:     0/TCP
    Command:
      /bin/sh
      -c
      touch /usr/share/nginx/html/ready
      echo "You have been served by Pod with IP address: $(hostname -i)" > /usr/share/nginx/html/index.html
      nginx -g "daemon off;"

    State:          Running
      Started:      Tue, 16 Apr 2024 22:20:27 +0800
    Ready:          False
    Restart Count:  0
    Readiness:      http-get http://:80/ready delay=5s timeout=10s period=2s #success=1 #failure=2
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-2wl8m (ro)
Conditions:
  Type                        Status
  PodReadyToStartContainers   True
  Initialized                 True
  Ready                       False
  ContainersReady             False
  PodScheduled                True
Volumes:
  kube-api-access-2wl8m:
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
  Type     Reason     Age                  From               Message
  ----     ------     ----                 ----               -------
  Normal   Scheduled  22m                  default-scheduler  Successfully assigned default/nginx-deployment-readiness-69dd4cfdd9-4pkwr to my-kind-cluster-worker2
  Normal   Pulling    22m                  kubelet            Pulling image "nginx:1.25.4"
  Normal   Pulled     21m                  kubelet            Successfully pulled image "nginx:1.25.4" in 8.496s (1m0.478s including waiting)
  Normal   Created    21m                  kubelet            Created container nginx
  Normal   Started    21m                  kubelet            Started container nginx
  Warning  Unhealthy  72s (x25 over 118s)  kubelet            Readiness probe failed: HTTP probe failed with statuscode: 404
```

```shell
$ kubectl exec -it nginx-deployment-readiness-69dd4cfdd9-7n2kz -- rm /usr/share/nginx/html/ready

$ kubectl exec -it nginx-deployment-readiness-69dd4cfdd9-t7rp2 -- rm /usr/share/nginx/html/ready

$ kubectl get po -w
NAME                                          READY   STATUS    RESTARTS   AGE
k8sutils                                      1/1     Running   0          166m
nginx-deployment-readiness-69dd4cfdd9-4pkwr   0/1     Running   0          25m
nginx-deployment-readiness-69dd4cfdd9-7n2kz   0/1     Running   0          25m
nginx-deployment-readiness-69dd4cfdd9-t7rp2   0/1     Running   0          25m

$ kubectl exec -it k8sutils -- curl nginx-service-example.default.svc.cluster.local
curl: (7) Failed to connect to nginx-service-example.default.svc.cluster.local port 80 after 5 ms: Couldn't connect to server
command terminated with exit code 7
```

```shell
$ kubectl exec -it nginx-deployment-readiness-69dd4cfdd9-4pkwr -- touch /usr/share/nginx/html/ready
```

## Scaling

```shell
$ kubectl describe deployments.apps nginx-deployment-readiness
Name:                   nginx-deployment-readiness
...<removed fro brevity>...
Events:
  Type    Reason             Age   From                   Message
  ----    ------             ----  ----                   -------
  Normal  ScalingReplicaSet  32m   deployment-controller  Scaled up replica set nginx-deployment-readiness-69dd4cfdd9 to 3
  Normal  ScalingReplicaSet  9s    deployment-controller  Scaled up replica set nginx-deployment-readiness-69dd4cfdd9 to 10 from 3
```

## Rolling Update

```shell
$ kubectl apply -f nginx-deployment-rollingupdate.yaml
deployment.apps/nginx-deployment-rollingupdate created

$ kubectl get po
NAME                                              READY   STATUS    RESTARTS   AGE
nginx-deployment-rollingupdate-69d855cf4b-nshn2   1/1     Running   0          24s
nginx-deployment-rollingupdate-69d855cf4b-pqvjh   1/1     Running   0          24s
nginx-deployment-rollingupdate-69d855cf4b-tdxzl   1/1     Running   0          24s

$ kubectl get po -o wide
NAME                                              READY   STATUS    RESTARTS   AGE   IP           NODE                      NOMINATED NODE   READINESS GATES
nginx-deployment-rollingupdate-69d855cf4b-nshn2   1/1     Running   0          50s   10.244.2.2   my-kind-cluster-worker    <none>           <none>
nginx-deployment-rollingupdate-69d855cf4b-pqvjh   1/1     Running   0          50s   10.244.3.2   my-kind-cluster-worker3   <none>           <none>
nginx-deployment-rollingupdate-69d855cf4b-tdxzl   1/1     Running   0          50s   10.244.1.2   my-kind-cluster-worker2   <none>           <none>

$ kubectl get po -o wide | awk '{print $1, $2, $6, $7}'
NAME READY IP NODE
nginx-deployment-rollingupdate-69d855cf4b-nshn2 1/1 10.244.2.2 my-kind-cluster-worker
nginx-deployment-rollingupdate-69d855cf4b-pqvjh 1/1 10.244.3.2 my-kind-cluster-worker3
nginx-deployment-rollingupdate-69d855cf4b-tdxzl 1/1 10.244.1.2 my-kind-cluster-worker2
```

Update the YAML and apply Deployment

```shell
$ kubectl apply -f nginx-deployment-rollingupdate.yaml
deployment.apps/nginx-deployment-rollingupdate configured

$ kubectl rollout status deployment.apps/nginx-deployment-rollingupdate
deployment "nginx-deployment-rollingupdate" successfully rolled out

$ kubectl describe deploy nginx-deployment-rollingupdate
Name:                   nginx-deployment-rollingupdate
...<removed for brevity>...
Events:
  Type    Reason             Age    From                   Message
  ----    ------             ----   ----                   -------
  Normal  ScalingReplicaSet  8m21s  deployment-controller  Scaled up replica set nginx-deployment-rollingupdate-69d855cf4b to 3
  Normal  ScalingReplicaSet  2m51s  deployment-controller  Scaled up replica set nginx-deployment-rollingupdate-5479f5d87f to 1
  Normal  ScalingReplicaSet  2m51s  deployment-controller  Scaled down replica set nginx-deployment-rollingupdate-69d855cf4b to 2 from 3
  Normal  ScalingReplicaSet  2m51s  deployment-controller  Scaled up replica set nginx-deployment-rollingupdate-5479f5d87f to 2 from 1
  Normal  ScalingReplicaSet  2m24s  deployment-controller  Scaled down replica set nginx-deployment-rollingupdate-69d855cf4b to 1 from 2
  Normal  ScalingReplicaSet  2m24s  deployment-controller  Scaled up replica set nginx-deployment-rollingupdate-5479f5d87f to 3 from 2
  Normal  ScalingReplicaSet  2m14s  deployment-controller  Scaled down replica set nginx-deployment-rollingupdate-69d855cf4b to 0 from 1
```

Check RepicaSet

```shell
$ kubectl get rs
NAME                                        DESIRED   CURRENT   READY   AGE
nginx-deployment-rollingupdate-5479f5d87f   3         3         3       4m22s
nginx-deployment-rollingupdate-69d855cf4b   0         0         0       9m52s
```

Check image

```shell
$ kubectl get po
NAME                                              READY   STATUS    RESTARTS   AGE
nginx-deployment-rollingupdate-5479f5d87f-2k7d6   1/1     Running   0          5m41s
nginx-deployment-rollingupdate-5479f5d87f-6gn9m   1/1     Running   0          5m14s
nginx-deployment-rollingupdate-5479f5d87f-mft6b   1/1     Running   0          5m41s

$ kubectl describe pod nginx-deployment-rollingupdate-5479f5d87f-2k7d6|grep 'Image:'
    Image:         nginx:1.18
```

Rolling update using imperative commands

```shell
$ kubectl set image deployment nginx-deployment-rollingupdate nginx=nginx:1.19
deployment.apps/nginx-deployment-rollingupdate image updated

$ kubectl rollout status deployment.apps/nginx-deployment-rollingupdate
deployment "nginx-deployment-rollingupdate" successfully rolled out
```

Rollback

```shell
$ kubectl rollout history deployment.apps/nginx-deployment-rollingupdate
deployment.apps/nginx-deployment-rollingupdate
REVISION  CHANGE-CAUSE
1         <none>
2         <none>
3         <none>

$ kubectl rollout history deploy nginx-deployment-rollingupdate --revision=2
deployment.apps/nginx-deployment-rollingupdate with revision #2
Pod Template:
  Labels:       app=nginx
        environment=test
        pod-template-hash=5479f5d87f
  Containers:
   nginx:
    Image:      nginx:1.18
    Port:       80/TCP
    Host Port:  0/TCP
    Command:
      /bin/sh
      -c
      touch /usr/share/nginx/html/ready
      echo "You have been served by Pod with IP address: $(hostname -i)" > /usr/share/nginx/html/index.html
      nginx -g "daemon off;"

    Readiness:  http-get http://:80/ready delay=5s timeout=10s period=2s #success=1 #failure=2
    Environment:        <none>
    Mounts:     <none>
  Volumes:      <none>

$ kubectl rollout undo deploy nginx-deployment-rollingupdate
deployment.apps/nginx-deployment-rollingupdate rolled back

# or
kubectl rollout undo deploy nginx-deployment-rollingupdate --to-revision=2

$ kubectl rollout history deployment.apps/nginx-deployment-rollingupdate
deployment.apps/nginx-deployment-rollingupdate
REVISION  CHANGE-CAUSE
1         <none>
3         <none>
4         <none>
```

## Canary Deployments

```yaml
# Stable app
  ...
  name: frontend-stable
  replicas: 3
  ...
  labels:
    app: myapp
    tier: frontend
    version: stable
  ...
  image: frontend-app:1.0
```

```yaml
# Canary version
  ...
  name: frontend-canary
  replicas: 1
  ...
  labels:
    app: myapp
    tier: frontend
    version: canary
  ...
  image: frontend-app:2.0
```

## Appendix

### Building container image

```shell
$ podman build -t nginx-custom:1.0 .
$ podman tag localhost/nginx-custom:1.0 quay.io/iamgini/nginx-custom:1.0
$ podman login quay.io
$ podman push quay.io/iamgini/nginx-custom:1.0
```