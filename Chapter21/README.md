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

## Deploying Ingress

```shell
$ kubectl apply -f ingress/
namespace/ingress-demo created
configmap/blog-configmap created
deployment.apps/blog created
service/blog-service created
ingress.networking.k8s.io/portal-ingress created
configmap/shopping-configmap created
deployment.apps/shopping created
service/shopping-service created
configmap/video-configmap created
deployment.apps/video created
service/video-service created
```

```shell
$ kubectl get po,svc,ingress -n ingress-demo
NAME                            READY   STATUS    RESTARTS   AGE
pod/blog-675df44d5-5s8sg        1/1     Running   0          88s
pod/shopping-6f88c5f485-lw6ts   1/1     Running   0          88s
pod/video-7d945d8c9f-wkxc5      1/1     Running   0          88s

NAME                       TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
service/blog-service       ClusterIP   10.111.70.32    <none>        8080/TCP   88s
service/shopping-service   ClusterIP   10.99.103.137   <none>        8080/TCP   88s
service/video-service      ClusterIP   10.109.3.177    <none>        8080/TCP   88s

NAME                                       CLASS   HOSTS            ADDRESS         PORTS   AGE
ingress.networking.k8s.io/portal-ingress   nginx   k8sbible.local   192.168.39.18   80      88s
```

```shell
$ curl --resolve "k8sbible.local:80:$( minikube ip )" -i http://k8sbible.local/video
```


## AGIC

```shell
$ az aks create --resource-group myResourceGroup --name myAKSCluster --node-count 2 --network-plugin azure --enable-managed-identity -a ingress-appgw --appgw-name MyAppGateway --appgw-subnet-cidr "10.2.0.0/16" --generate-ssh-keys

$ az aks get-credentials --resource-group k8sforbeginners-rg --name k8sforbeginners-aks-agic
Merged "k8sforbeginners-aks-agic" as current context in .kube/config
```

```shell
$ kubectl apply -f aks_agic/
$ kubectl get ingress
```

## IngressClass

```shell
$ kubectl get IngressClass -o yaml
apiVersion: v1
items:
- apiVersion: networking.k8s.io/v1
  kind: IngressClass
  metadata:
    name: nginx
    annotations:
      ingressclass.kubernetes.io/is-default-class: "true"
      kubectl.kubernetes.io/last-applied-configuration: |
        {"apiVersion":"networking.k8s.io/v1","kind":"IngressClass","metadata":{"annotations":{"ingressclass.kubernetes.io/is-default-class":"true"},"labels":{"app.kubernetes.io/component":"controller","app.kubernetes.io/instance":"ingress-nginx","app.kubernetes.io/name":"ingress-nginx"},"name":"nginx"},"spec":{"controller":"k8s.io/ingress-nginx"}}
    creationTimestamp: "2024-08-20T16:13:26Z"
    generation: 1
    labels:
      app.kubernetes.io/component: controller
      app.kubernetes.io/instance: ingress-nginx
      app.kubernetes.io/name: ingress-nginx
    name: nginx
    resourceVersion: "731"
    uid: a6efc47f-7a2f-479a-864b-c7724557bbdd
  spec:
    controller: k8s.io/ingress-nginx
kind: List
metadata:
  resourceVersion: ""
```


```shell
$ kubectl get ingress
NAME              CLASS    HOSTS   ADDRESS         PORTS   AGE
example-ingress   <none>   *       52.191.222.39   80      36m
```

## etcd

```shell
$ ETCDCTL_API=3 etcdctl \
  --endpoints=[https://127.0.0.1:2379] \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  snapshot save /tmp/snapshot-pre-patch.db

$ etcdutl --write-out=table snapshot status snapshot.db
```

## Troubleshooting

```shell
$ kubectl apply -f troubleshooting/video-portal.yaml
namespace/trouble-demo created
configmap/video-configmap created
deployment.apps/video created
service/video-service created

$ kubectl debug -it pod/video-7d945d8c9f-wkxc5 --image=quay.io/iamgini/k8sutils:debian12 -c k8sutils -n ingress-demo

root@video-7d945d8c9f-wkxc5:/# nslookup video-service
Server:         10.96.0.10
Address:        10.96.0.10#53

Name:   video-service.ingress-demo.svc.cluster.local
Address: 10.109.3.177

root@video-7d945d8c9f-wkxc5:/# curl http://video-service:8080

    <!DOCTYPE html>
    <html>
    <head>
      <title>Welcome</title>
      <style>
        body {
          background-color: yellow;
          text-align: center;
...<removed for brevity>...
```

## Logs and Events

```shell
$ kubectl get events
LAST SEEN   TYPE      REASON                    OBJECT                              MESSAGE
39m         Normal    CIDRAssignmentFailed      node/example-node                   Node example-node status is now: CIDRAssignmentFailed
39m         Normal    RegisteredNode            node/example-node                   Node example-node event: Registered Node example-node in Controller
38m         Normal    RemovingNode              node/example-node                   Node example-node event: Removing Node example-node from Controller
41m         Normal    Starting                  node/minikube                       Starting kubelet.
41m         Normal    NodeHasSufficientMemory   node/minikube                       Node minikube status is now: NodeHasSufficientMemory
41m         Normal    NodeHasNoDiskPressure     node/minikube                       Node minikube status is now: NodeHasNoDiskPressure
41m         Normal    NodeHasSufficientPID      node/minikube                       Node minikube status is now: NodeHasSufficientPID
41m         Normal    NodeAllocatableEnforced   node/minikube                       Updated Node Allocatable limit across pods
41m         Normal    Starting                  node/minikube                       Starting kubelet.
41m         Normal    NodeAllocatableEnforced   node/minikube                       Updated Node Allocatable limit across pods
41m         Normal    NodeHasSufficientMemory   node/minikube                       Node minikube status is now: NodeHasSufficientMemory
41m         Normal    NodeHasNoDiskPressure     node/minikube                       Node minikube status is now: NodeHasNoDiskPressure
41m         Normal    NodeHasSufficientPID      node/minikube                       Node minikube status is now: NodeHasSufficientPID
41m         Normal    NodeReady                 node/minikube                       Node minikube status is now: NodeReady
41m         Normal    RegisteredNode            node/minikube                       Node minikube event: Registered Node minikube in Controller
41m         Normal    Starting                  node/minikube
24s         Normal    Starting                  node/minikube                       Starting kubelet.
24s         Normal    NodeHasSufficientMemory   node/minikube                       Node minikube status is now: NodeHasSufficientMemory
24s         Normal    NodeHasNoDiskPressure     node/minikube                       Node minikube status is now: NodeHasNoDiskPressure
24s         Normal    NodeHasSufficientPID      node/minikube                       Node minikube status is now: NodeHasSufficientPID
24s         Normal    NodeAllocatableEnforced   node/minikube                       Updated Node Allocatable limit across pods
19s         Normal    Starting                  node/minikube
17s         Normal    RegisteredNode            node/minikube                       Node minikube event: Registered Node minikube in Controller
36m         Normal    Provisioning              persistentvolumeclaim/pvc-example   External provisioner is provisioning volume for claim "default/pvc-example"
36m         Normal    ExternalProvisioning      persistentvolumeclaim/pvc-example   Waiting for a volume to be created either by the external provisioner 'k8s.io/minikube-hostpath' or manually by the system administrator. If volume creation is delayed, please verify that the provisioner is running and correctly registered.
36m         Normal    ProvisioningSucceeded     persistentvolumeclaim/pvc-example   Successfully provisioned volume pvc-1a16fb6b-d9d2-4131-95be-be6d34c65277
29m         Warning   ProvisioningFailed        persistentvolumeclaim/pvc-example   storageclass.storage.k8s.io "standard-gold" not found
2s          Warning   ProvisioningFailed        persistentvolumeclaim/pvc-example   storageclass.storage.k8s.io "standard-gold" not found
```
