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
$ kubectl apply -f https://k8s.io/examples/admin/dns/dnsutils.yaml
pod/dnsutils created
```