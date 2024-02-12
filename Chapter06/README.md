# Configuring Your Pods Using ConfigMaps and Secrets

```shell
$ kubectl get configmaps 

# Alternatively, you can use the shorter alias, which is cm: 
$ kubectl get cm 

$  kubectl get configmaps -A 
NAMESPACE         NAME                                                   DATA   AGE
default           kube-root-ca.crt                                       1      23d
kube-node-lease   kube-root-ca.crt                                       1      23d
kube-public       cluster-info                                           1      23d
kube-public       kube-root-ca.crt                                       1      23d
kube-system       coredns                                                1      23d
kube-system       extension-apiserver-authentication                     6      23d
kube-system       kube-apiserver-legacy-service-account-token-tracking   1      23d
kube-system       kube-proxy                                             2      23d
kube-system       kube-root-ca.crt                                       1      23d
kube-system       kubeadm-config                                         1      23d
kube-system       kubelet-config                                         1      23d
wordpress         kube-root-ca.crt                                       1      23d
```

```shell
$ kubectl create configmap my-first-configmap 
configmap/my-first-configmap created 

$ kubectl get cm 
NAME                 DATA   AGE 
my-first-configmap   0      42s 

  kubectl create -f my-second-configmap.yaml 
configmap/my-second-configmap created

$  kubectl get cm
NAME                  DATA   AGE
kube-root-ca.crt      1      23d
my-first-configmap    0      5s
my-second-configmap   0      2s
```

```shell
$ kubectl create cm my-third-configmap --from-literal=color=blue 

$ kubectl create cm my-fourth-configmap --from-literal=color=blue --from-literal=version=1 --from-literal=environment=prod 

$ kubectl get cm
NAME                  DATA   AGE
kube-root-ca.crt      1      23d
my-first-configmap    0      4h53m
my-fourth-configmap   3      109s
my-second-configmap   0      4h53m
my-third-configmap    1      4h52m
```

```shell
$ echo "I'm just a dummy config file" >> $HOME/configfile.txt

$ kubectl create cm my-sixth-configmap --from-literal=color=yellow --from-file=$HOME/configfile.txt

$ kubectl get cm my-sixth-configmap
NAME                 DATA   AGE
my-sixth-configmap   2      28s
```

```shell
$ kubectl create cm my-eight-configmap --from-env-file my-env-file.txt  
configmap/my-eight-configmap created

$ kubectl get cm my-eight-configmap
NAME                 DATA   AGE
my-eight-configmap   3      105s
```

Read ConfigMap

```shell
$  kubectl describe cm my-fourth-configmap 
Name:         my-fourth-configmap
Namespace:    default
Labels:       <none>
Annotations:  <none>

Data
====
color:
----
blue
environment:
----
prod
version:
----
1

BinaryData
====

Events:  <none>
```