# Exposing Your Pods with Services

```shell
$ kubectl create -f new-nginx-pod.yaml
pod/new-nginx-pod created

$ kubectl get po -o wide
NAME            READY   STATUS    RESTARTS   AGE   IP             NODE       NOMINATED NODE   READINESS GATES
new-nginx-pod   1/1     Running   0          99s   10.244.0.109   minikube   <none>           <none>

$ kubectl delete -f new-nginx-pod.yaml
pod "new-nginx-pod" deleted

$ kubectl create -f new-nginx-pod.yaml
pod/new-nginx-pod created

$ kubectl get po -o wide
NAME            READY   STATUS    RESTARTS   AGE   IP             NODE       NOMINATED NODE   READINESS GATES
new-nginx-pod   1/1     Running   0          97s   10.244.0.110   minikube   <none>           <none>
```

## Creating services

```shell
$ kubectl run nginx --image nginx --expose=true --port=80
service/nginx created
pod/nginx created

$ kubectl get po,svc nginx
NAME        READY   STATUS    RESTARTS   AGE
pod/nginx   1/1     Running   0          24s

NAME            TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
service/nginx   ClusterIP   10.111.12.100   <none>        80/TCP    24s

$ kubectl get po nginx --show-labels
NAME    READY   STATUS    RESTARTS   AGE   LABELS
nginx   1/1     Running   0          51s   run=nginx

$ kubectl describe svc nginx
Name:              nginx
Namespace:         default
Labels:            <none>
Annotations:       <none>
Selector:          run=nginx
Type:              ClusterIP
IP Family Policy:  SingleStack
IP Families:       IPv4
IP:                10.111.12.100
IPs:               10.111.12.100
Port:              <unset>  80/TCP
TargetPort:        80/TCP
Endpoints:         10.244.0.9:80
Session Affinity:  None
Events:            <none>

# if you want to test it with NodePort in minikube
$ kubectl expose pod nginx --port=80 --type=NodePort
service/nginx exposed

$ minikube service --url nginx
http://192.168.49.2:32156

$ curl http://192.168.49.2:32156
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```


```shell
$ kubectl apply -f k8sutils.yaml
pod/k8sutils created

$ kubectl get po k8sutils
NAME       READY   STATUS    RESTARTS   AGE
k8sutils   1/1     Running   0          13m

$ kubectl exec -it k8sutils -- nslookup nginx.default.svc.cluster.local
Server:         10.96.0.10
Address:        10.96.0.10#53

Name:   nginx.default.svc.cluster.local
Address: 10.106.124.200
```

## NodePort Service

```shell
$ kubectl run whoami1 --image=containous/whoami --port 80 --labels="app=whoami"
pod/whoami1 created
$ kubectl run whoami2 --image=containous/whoami --port 80 --labels="app=whoami"
pod/whoami2 created

$ kubectl get pods --show-labels
NAME      READY   STATUS    RESTARTS   AGE    LABELS
whoami1   1/1     Running   0          3m5s   app=whoami
whoami2   1/1     Running   0          3m     app=whoami
```

```shell
$ kubectl create -f nodeport-whoami.yaml
service/nodeport-whoami created

$ kubectl get service nodeport-whoami
NAME              TYPE       CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
nodeport-whoami   NodePort   10.98.160.98   <none>        80:30001/TCP   14s

$ minikube service --url nodeport-whoami
http://192.168.49.2:30001

$ kubectl describe service nodeport-whoami
Name:                     nodeport-whoami
Namespace:                default
Labels:                   <none>
Annotations:              <none>
Selector:                 app=whoami
Type:                     NodePort
IP Family Policy:         SingleStack
IP Families:              IPv4
IP:                       10.98.160.98
IPs:                      10.98.160.98
Port:                     <unset>  80/TCP
TargetPort:               80/TCP
NodePort:                 <unset>  30001/TCP
Endpoints:                10.244.0.16:80,10.244.0.17:80
Session Affinity:         None
External Traffic Policy:  Cluster
Events:                   <none>
```

## ClusterIP

```shell
$ kubectl run nginx-clusterip --image nginx --expose=true --port=80
service/nginx-clusterip created
pod/nginx-clusterip created

$ kubectl describe svc/nginx-clusterip
Name:              nginx-clusterip
Namespace:         default
Labels:            <none>
Annotations:       <none>
Selector:          run=nginx-clusterip
Type:              ClusterIP
IP Family Policy:  SingleStack
IP Families:       IPv4
IP:                10.101.229.225
IPs:               10.101.229.225
Port:              <unset>  80/TCP
TargetPort:        80/TCP
Endpoints:         10.244.0.10:80
Session Affinity:  None
Events:            <none>

$ kubectl get pods/nginx-clusterip --show-labels
NAME              READY   STATUS    RESTARTS   AGE   LABELS
nginx-clusterip   1/1     Running   0          76s   run=nginx-clusterip
```

Test ClusterIP URL

```shell
$ kubectl exec k8sutils -- curl nginx-clusterip.default.svc.cluster.local
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
100   615  100   615    0     0  65446      0 --:--:-- --:--:-- --:--:-- 68333
```

Delete ClusterIP

```shell
$ kubectl delete  svc nginx-clusterip
service "nginx-clusterip" deleted
```

Named port

```yaml
ports:
- name: liveness-port
  containerPort: 8080
  hostPort: 8080

livenessProbe:
  httpGet:
    path: /healthz
    port: liveness-port
```

## NetworkPolicy

```shell
$ minikube start --network-plugin=cni --cni=calico
```


```shell
$ kubectl apply -f web-app1.yaml
namespace/web1 created
pod/nginx1 created

$ kubectl apply -f web-app2.yaml
namespace/web2 created
pod/nginx2 created

$ kubectl get po -o wide -n web1
NAME     READY   STATUS    RESTARTS   AGE   IP              NODE       NOMINATED NODE   READINESS GATES
nginx1   1/1     Running   0          3m    10.244.120.71   minikube   <none>           <none>
$ kubectl get po -o wide -n web2
NAME     READY   STATUS    RESTARTS   AGE     IP              NODE       NOMINATED NODE   READINESS GATES
nginx2   1/1     Running   0          2m53s   10.244.120.72   minikube   <none>           <none>
```

```shell
$ kubectl -n web1 exec nginx1 -- curl 10.244.0.28
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   615  100   615    0     0   698k      0 --:--:-- --:--:-- --:--:--  600k
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```

Apply deny policy and test access

```shell
$ kubectl apply -f default-deny-ingress.yaml
networkpolicy.networking.k8s.io/default-deny-ingress created

$  kubectl -n web1 exec nginx1 -- curl 10.244.120.65
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:--  0:02:15 --:--:--     0
curl: (28) Failed to connect to 10.244.120.65 port 80 after 135435 ms: Couldn't connect to server
command terminated with exit code 28
```

Allow traffic

```shell
$ kubectl apply -f allow-from-web1-netpol.yaml
networkpolicy.networking.k8s.io/allow-from-web1-netpol created

$ kubectl -n web1 exec nginx1 -- curl 10.244.120.72
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   615  100   615    0     0  1280k      0 --:--:-- --:--:-- --:--:--  600k
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```

```shell
$ kubectl delete networkpolicies.networking.k8s.io nginx2-networkpolicy
networkpolicy.networking.k8s.io "nginx2-networkpolicy" deleted

$ kubectl apply -f nginx2-networkpolicy-8080.yaml
networkpolicy.networking.k8s.io/nginx2-networkpolicy-8080 created
```

## Appendix

### Building container image

```shell
$ podman build -t k8sutils:debian12 .
$ podman tag localhost/k8sutils:debian12 quay.io/iamgini/k8sutils:debian12
$ podman login quay.io
$ podman push quay.io/iamgini/k8sutils:debian12
```