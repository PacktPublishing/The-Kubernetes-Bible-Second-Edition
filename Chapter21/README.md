# Advanced Kubernetes: From Traffic Management to Multi-Cluster Strategies and Emerging Technologies

## Ingress

```shell
$ minikube addons enable ingress
💡  ingress is an addon maintained by Kubernetes. For any concerns contact minikube on GitHub.
You can view the list of minikube maintainers at: https://github.com/kubernetes/minikube/blob/master/OWNERS
    ▪ Using image registry.k8s.io/ingress-nginx/kube-webhook-certgen:v1.4.1
    ▪ Using image registry.k8s.io/ingress-nginx/controller:v1.10.1
    ▪ Using image registry.k8s.io/ingress-nginx/kube-webhook-certgen:v1.4.1
🔎  Verifying ingress addon...
🌟  The 'ingress' addon is enabled

$ kubectl get pods -n ingress-nginx
NAME                                        READY   STATUS      RESTARTS   AGE
ingress-nginx-admission-create-rsznt        0/1     Completed   0          78s
ingress-nginx-admission-patch-4c7xh         0/1     Completed   0          78s
ingress-nginx-controller-6fc95558f4-zdhp7   1/1     Running     0          78s
```

```shell
$ kubectl get po -n ingress-demo
NAME                        READY   STATUS    RESTARTS   AGE
blog-675df44d5-8q5jm        1/1     Running   0          25m
shopping-6f88c5f485-ngp76   1/1     Running   0          26m
video-7d945d8c9f-58zt6      1/1     Running   0          25m
$ kubectl get ingress -n ingress-demo
NAME             CLASS   HOSTS            ADDRESS         PORTS   AGE
portal-ingress   nginx   k8sbible.local   192.168.39.18   80      13m
```

```shell
$ curl --resolve "k8sbible.local:80:$( minikube ip )" -i http://k8sbible.local/video
```