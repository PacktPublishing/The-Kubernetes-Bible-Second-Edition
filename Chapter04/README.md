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

## Labelling

```shell
$ kubectl run nginx-pod --image nginx --labels "tier=frontend" 
```

```shell
$ kubectl get pod -l environment=prod
NAME        READY   STATUS    RESTARTS   AGE
nginx-pod   1/1     Running   0          31m
```

```shell
$ kubectl get pods --show-labels
NAME        READY   STATUS    RESTARTS   AGE   LABELS
nginx-pod   1/1     Running   0          56s   environment=prod,tier=frontend
```

Apply label on running resources

```shell
$ kubectl label pod nginx-pod stack=blue
pod/nginx-pod labeled

$ kubectl get pods nginx-pod --show-labels 
NAME        READY   STATUS    RESTARTS   AGE   LABELS
nginx-pod   1/1     Running   0          38m   environment=prod,stack=blue,tier=frontend
```

Overwrite/Update

```shell
$ kubectl label pod nginx-pod stack=green --overwrite 
pod/nginx-pod labeled

$ kubectl get pods nginx-pod --show-labels 
NAME        READY   STATUS    RESTARTS   AGE   LABELS
nginx-pod   1/1     Running   0          41m   environment=prod,stack=green,tier=frontend
```

Remove label

```shell
$ kubectl label pod nginx-pod stack-
pod/nginx-pod unlabeled

$ kubectl get pods nginx-pod --show-labels 
NAME        READY   STATUS    RESTARTS   AGE   LABELS
nginx-pod   1/1     Running   0          45m   environment=prod,tier=frontend
```

## Jobs

```shell
$ kubectl get jobs
NAME              COMPLETIONS   DURATION   AGE
hello-world-job   1/1           9s         8m46s
```

```shell
$ kubectl get jobs -w
NAME              COMPLETIONS   DURATION   AGE
hello-world-job   0/10          4s         4s
hello-world-job   0/10          5s         5s
hello-world-job   0/10          8s         8s
hello-world-job   0/10          9s         9s
hello-world-job   1/10          9s         9s
hello-world-job   1/10          13s        13s
<removed for brevity>
hello-world-job   9/10          83s        83s
hello-world-job   9/10          86s        86s
hello-world-job   9/10          87s        87s
hello-world-job   10/10         87s        87s
```

```shell
$ kubectl get pods -w
NAME                    READY   STATUS              RESTARTS   AGE
hello-world-job-48hjd   0/1     ContainerCreating   0          4s
hello-world-job-4q2tj   0/1     ContainerCreating   0          4s
hello-world-job-ns4b2   0/1     ContainerCreating   0          4s
hello-world-job-v4nkm   0/1     ContainerCreating   0          4s
hello-world-job-xs25l   0/1     ContainerCreating   0          4s
nginx-pod               1/1     Running             0          69m
hello-world-job-ns4b2   1/1     Running             0          4s
hello-world-job-4q2tj   1/1     Running             0          6s
hello-world-job-ns4b2   0/1     Completed           0        7s
<removed for brevity>
```

## CronJobs

```shell
# ┌───────────── minute (0 - 59)
# │ ┌───────────── hour (0 - 23)
# │ │ ┌───────────── day of the month (1 - 31)
# │ │ │ ┌───────────── month (1 - 12)
# │ │ │ │ ┌───────────── day of the week (0 - 6) (Sunday to Saturday;
# │ │ │ │ │                                   7 is also Sunday on some systems)
# │ │ │ │ │                                   OR sun, mon, tue, wed, thu, fri, sat
# │ │ │ │ │
# * * * * *
```

```shell
$ kubectl create -f hello-world-cronjob.yaml 
cronjob.batch/hello-world-cronjob created

$ kubectl get jobs
NAME                           COMPLETIONS   DURATION   AGE
hello-world-cronjob-28390196   1/1           3s         4m47s
hello-world-cronjob-28390197   1/1           3s         3m47s
hello-world-cronjob-28390198   1/1           3s         2m47s
hello-world-cronjob-28390199   1/1           3s         107s
hello-world-cronjob-28390200   1/1           4s         47s
 
$ kubectl get pods
NAME                                 READY   STATUS      RESTARTS   AGE
hello-world-cronjob-28390196-fpmc6   0/1     Completed   0          4m52s
hello-world-cronjob-28390197-vkzw2   0/1     Completed   0          3m52s
hello-world-cronjob-28390198-tj6qv   0/1     Completed   0          2m52s
hello-world-cronjob-28390199-dd666   0/1     Completed   0          112s
hello-world-cronjob-28390200-kn89r   0/1     Completed   0          52s
```