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

```shell
$ kubectl create -f flask-pod-with-configmap.yaml 
pod/flask-pod-with-configmap created

$ kubectl exec pods/flask-pod-with-configmap -- env
PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
HOSTNAME=flask-pod-with-configmap
COLOR=blue
KUBERNETES_PORT_443_TCP=tcp://10.96.0.1:443
KUBERNETES_PORT_443_TCP_PROTO=tcp
KUBERNETES_PORT_443_TCP_PORT=443
KUBERNETES_PORT_443_TCP_ADDR=10.96.0.1
KUBERNETES_SERVICE_HOST=10.96.0.1
KUBERNETES_SERVICE_PORT=443
KUBERNETES_SERVICE_PORT_HTTPS=443
KUBERNETES_PORT=tcp://10.96.0.1:443
LANG=C.UTF-8
GPG_KEY=E3FF2839C048B25C084DEBE9B26995E310250568
PYTHON_VERSION=3.9.18
PYTHON_PIP_VERSION=23.0.1
PYTHON_SETUPTOOLS_VERSION=58.1.0
PYTHON_GET_PIP_URL=https://github.com/pypa/get-pip/raw/dbf0c85f76fb6e1ab42aa672ffca6f0a675d9ee4/public/get-pip.py
PYTHON_GET_PIP_SHA256=dfe9fd5c28dc98b5ac17979a953ea550cec37ae1b47a5116007395bfacff2ab9
HOME=/root
```

```shell
# Expose the pod
$ kubectl expose pod flask-pod-with-configmap --port=8081 --target-port=5000 --type=NodePort

# Find the external port for minikube
$ minikube service --url flask-pod-with-configmap
http://192.168.49.2:31997
```

```shell
$ kubectl create -f flask-pod-with-configmap-all.yaml
pod/flask-pod-2-with-configmap created

$ kubectl exec pods/flask-pod-with-configmap-all -- env
PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
HOSTNAME=flask-pod-2-with-configmap
environment=prod
version=1
color=blue
KUBERNETES_PORT_443_TCP_PORT=443
KUBERNETES_PORT_443_TCP_ADDR=10.96.0.1
KUBERNETES_SERVICE_HOST=10.96.0.1
KUBERNETES_SERVICE_PORT=443
KUBERNETES_SERVICE_PORT_HTTPS=443
KUBERNETES_PORT=tcp://10.96.0.1:443
KUBERNETES_PORT_443_TCP=tcp://10.96.0.1:443
KUBERNETES_PORT_443_TCP_PROTO=tcp
LANG=C.UTF-8
GPG_KEY=E3FF2839C048B25C084DEBE9B26995E310250568
PYTHON_VERSION=3.9.18
PYTHON_PIP_VERSION=23.0.1
PYTHON_SETUPTOOLS_VERSION=58.1.0
PYTHON_GET_PIP_URL=https://github.com/pypa/get-pip/raw/dbf0c85f76fb6e1ab42aa672ffca6f0a675d9ee4/public/get-pip.py
PYTHON_GET_PIP_SHA256=dfe9fd5c28dc98b5ac17979a953ea550cec37ae1b47a5116007395bfacff2ab9
HOME=/root
```

```shell
$ kubectl apply -f flask-pod-with-configmap-volume.yaml
pod/flask-pod-with-configmap-volume created

$ kubectl exec pods/flask-pod-with-configmap-volume -- ls /etc/conf
color
configfile.txt

$ kubectl exec pods/flask-pod-with-configmap-volume -- cat /etc/conf/color
yellow

$ kubectl exec pods/flask-pod-with-configmap-volume -- cat /etc/conf/configfile.txt
I'm just a dummy config file
```

Delete ConfigMap

```shell
$ kubectl delete cm my-first-configmap 
configmap "my-first-configmap" deleted 
```

## Secrets

```shell
$ kubectl get secret 
```

```shell
$ kubectl create secret generic my-first-secret --from-literal='db_password=my-db-password'
secret/my-first-secret created

$  kubectl get secrets 
NAME              TYPE     DATA   AGE
my-first-secret   Opaque   1      37s
```

```shell
$ echo 'my-db-password' | base64
bXktZGItcGFzc3dvcmQK

$ kubectl create -f secret-from-file.yaml 
secret/my-second-secret created

$ kubectl get secret my-second-secret -o yaml
apiVersion: v1
data:
  db_password: bXktZGItcGFzc3dvcmQK
kind: Secret
metadata:
  creationTimestamp: "2024-02-13T04:15:56Z"
  name: my-second-secret
  namespace: default
  resourceVersion: "90372"
  uid: 94b7b529-baed-4844-8097-f6c2a001fa7b
type: Opaque
```

```shell
$ echo -n 'mypassword' > ./password.txt 
$ cat  password.txt 
mypassword

$ kubectl describe secret/mypassword 
Name:         mypassword
Namespace:    default
Labels:       <none>
Annotations:  <none>

Type:  Opaque

Data
====
password.txt:  10 bytes
```

```shell
$ kubectl apply -f flask-pod-with-secret.yaml

$ kubectl exec pods/flask-pod-with-secret -- env 
PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
HOSTNAME=flask-pod-with-secret
PASSWORD_ENV_VAR=my-db-password
KUBERNETES_SERVICE_PORT=443
KUBERNETES_PORT=tcp://10.96.0.1:443
FLASK_POD_WITH_CONFIGMAP_PORT=tcp://10.101.204.122:8081
FLASK_POD_WITH_CONFIGMAP_PORT_8081_TCP_PROTO=tcp
FLASK_POD_WITH_CONFIGMAP_PORT_8081_TCP_PORT=8081
FLASK_POD_WITH_CONFIGMAP_PORT_8081_TCP_ADDR=10.101.204.122
KUBERNETES_PORT_443_TCP=tcp://10.96.0.1:443
KUBERNETES_PORT_443_TCP_ADDR=10.96.0.1
FLASK_POD_WITH_CONFIGMAP_SERVICE_HOST=10.101.204.122
FLASK_POD_WITH_CONFIGMAP_SERVICE_PORT=8081
FLASK_POD_WITH_CONFIGMAP_PORT_8081_TCP=tcp://10.101.204.122:8081
KUBERNETES_SERVICE_HOST=10.96.0.1
KUBERNETES_SERVICE_PORT_HTTPS=443
KUBERNETES_PORT_443_TCP_PROTO=tcp
KUBERNETES_PORT_443_TCP_PORT=443
LANG=C.UTF-8
GPG_KEY=E3FF2839C048B25C084DEBE9B26995E310250568
PYTHON_VERSION=3.9.18
PYTHON_PIP_VERSION=23.0.1
PYTHON_SETUPTOOLS_VERSION=58.1.0
PYTHON_GET_PIP_URL=https://github.com/pypa/get-pip/raw/dbf0c85f76fb6e1ab42aa672ffca6f0a675d9ee4/public/get-pip.py
PYTHON_GET_PIP_SHA256=dfe9fd5c28dc98b5ac17979a953ea550cec37ae1b47a5116007395bfacff2ab9
HOME=/root
```

```shell

$ kubectl exec pods/flask-pod-with-secret-volume --  cat /etc/password-mounted-path/db_password 
my-db-password 
```

## Appendix

You can build and play around wit the demo flask application.
Use the `app.py` and the `Containerfile` available in this directory for that.

```shell
$ podman build -t my-flask-app .
```