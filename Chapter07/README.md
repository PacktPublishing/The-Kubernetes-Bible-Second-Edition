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
$ kubectl run nginx --image nginx:latest
pod/nginx created

$ kubectl expose pod nginx --port=80 --target-port=8000
service/nginx exposed

$ kubectl get po nginx --show-labels 
NAME    READY   STATUS    RESTARTS   AGE     LABELS
nginx   1/1     Running   0          6m32s   run=nginx

$ kubectl describe svc nginx 
Name:              nginx
Namespace:         default
Labels:            run=nginx
Annotations:       <none>
Selector:          run=nginx
Type:              ClusterIP
IP Family Policy:  SingleStack
IP Families:       IPv4
IP:                10.107.75.133
IPs:               10.107.75.133
Port:              <unset>  80/TCP
TargetPort:        80/TCP
Endpoints:         10.244.0.115:80
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

## Appendix

### Building container image

```shell
$ podman build -t k8sutils:debian12 .
$ podman tag localhost/k8sutils:debian12 quay.io/iamgini/k8sutils:debian12 
$ podman login quay.io
$ podman push quay.io/iamgini/k8sutils:debian12
```