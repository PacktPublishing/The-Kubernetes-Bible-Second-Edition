# Running Your Application Containers 

```shell
$ kubectl run nginx-pod --image nginx:latest 

$ kubectl get pods
NAME        READY   STATUS    RESTARTS   AGE
nginx-pod   1/1     Running   0          3m13s
```

```shell
$ kubectl create -f nginx-pod.yaml  
pod/nginx-pod created 

# this command works too! 
$ kubectl apply -f nginx-pPod.yaml 
```

```shell
$ kubectl get pods -o yaml # In YAML format 
$ kubectl get pods -o json # In JSON format 

# If you know the Pod name, 
# you can also get a specific Pod 
$ kubectl get pods <POD_NAME> -o yaml 

# OR 
$ kubectl get pods <POD_NAME> -o json 
```

## Backup resource YAML

```shell
$ kubectl get pods/nginx-pod -o yaml > nginx-pod.yaml 
```

## List wide

```shell
  kubectl get pods -o wide 
NAME        READY   STATUS    RESTARTS   AGE   IP           NODE       NOMINATED NODE   READINESS GATES
nginx-pod   1/1     Running   0          15m   10.244.0.4   minikube   <none>           <none>
```

## Accessing application inside pod

```shell
$ kubectl port-forward pod/nginx-pod 8080:80 
Forwarding from 127.0.0.1:8080 -> 80
Forwarding from [::1]:8080 -> 80
```

## Accessing container

```shell
$ kubectl exec -it nginx-pod -- bash
root@nginx-pod:/# hostname 
nginx-pod

# exit from container shell
root@nginx-pod:/# exit 
exit 
```

## Delete pod

```shell
$ kubectl delete pods nginx-pod 
# or... 
$ kubectl delete pods/nginx-pod 

# or
$ kubectl delete -f nginx-pod.yaml 
```