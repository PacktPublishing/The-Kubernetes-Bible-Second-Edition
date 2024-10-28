# Security in Kubernetes


```yaml
# /etc/kubernetes/manifests/kube-apiserver.yaml
...<removed for brevity>...
spec:
  containers:
  - command:
    - kube-apiserver
    - --advertise-address=192.168.59.154
    - --allow-privileged=true
    - --authorization-mode=Node,RBAC
    - --token-auth-file=/etc/kubernetes/user-tokens.csv
    - --client-ca-file=/var/lib/minikube/certs/ca.crt
...<removed for brevity>...
```

## Service Account

```shell
$ kubectl apply -f 01_serviceaccount/
namespace/example-ns created
serviceaccount/example-sa created
role.rbac.authorization.k8s.io/pod-reader created
rolebinding.rbac.authorization.k8s.io/read-pods created
```

```shell
$ kubectl create token example-sa -n example-ns
eyJhbGciOiJSUzI1NiIsImtpZCI6IlcyczVtMEFVQ3hVaC1fNnlrLWVqcVlaUnVUQzBkeUdLY1cwTU5DM3JtbzAifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwiXSwiZXhwIjoxNzE4NDQ1NDc5LCJpYXQiOjE3MTg0NDE4NzksImlzcyI6Imh0dHBzOi8va3ViZXJuZXRlcy5kZWZhdWx0LnN2Yy5jbHVzdGVyLmxvY2FsIiwianRpIjoiNDVkYzg2MWMtMTAyNC00ODU3LWE2OTQtMDBhNWQyZWViYTVmIiwia3ViZXJuZXRlcy5pbyI6eyJuYW1lc3BhY2UiOiJleGFtcGxlLW5zIiwic2VydmljZWFjY291bnQiOnsibmFtZSI6ImV4YW1wbGUtc2EiLCJ1aWQiOiJlYmM1NTU0Yi0zMDZmLTQ4ZmUtYjlkNy0zZTU3NzdmYWJmMDYifX0sIm5iZiI6MTcxODQ0MTg3OSwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50OmV4YW1wbGUtbnM6ZXhhbXBsZS1zYSJ9.biCcURfFWre3YLg3jMzlYWAS9LkCb0CXODELxbN0WeHrcK338P3D1CqlA9fJudlzXxeujRBc-AkQTBJDyOae1xCXOefTXyLyHBEnkM5-RnVX6zkkIG9CcE1Vj1FqT48o_sKKuFFlpuWpJID9jTM5jJHyUsjLqA4lGYMHS6Xbgwoy96qRZhRAsYxC7H1w1xsynBKs89kQ9ZSJ54zpWDuqhz-7pPpKxj4TbFMFuOY0Gvi8mrYB6CUJ861ZN99q1IVDAptYwYw-bHdrwudO8S8z5V8vCqSjPXQEjsNeEV7cMvWD4bgDg1NQiHizOSR6aoXvjGkGmLLr8G422yT-Tp-qWw
```

Configure kubeconfig

```shell
$ kubectl config set-credentials example-sa --token=<your-token>
User "example-sa" set.

$ kubectl config set-context example-sa-context --user=example-sa --cluster=minikube
Context "example-sa-context" created.

# Check current content before switching
$ kubectl config current-context
minikube

# Switch to the new contenxt
$ kubectl config use-context example-sa-context
Switched to context "example-sa-context".

$ kubectl auth whoami
ATTRIBUTE                                           VALUE
Username                                            system:serviceaccount:example-ns:example-sa
UID                                                 ebc5554b-306f-48fe-b9d7-3e5777fabf06
Groups                                              [system:serviceaccounts system:serviceaccounts:example-ns system:authenticated]
Extra: authentication.kubernetes.io/credential-id   [JTI=45dc861c-1024-4857-a694-00a5d2eeba5f]
```

```shell
$ kubectl get po -n example-ns
NAME        READY   STATUS    RESTARTS   AGE
nginx-pod   1/1     Running   0          18m

$ kubectl get pods -n kube-system
Error from server (Forbidden): pods is forbidden: User "system:serviceaccount:example-ns:example-sa" cannot list resource "pods" in API group "" in the namespace "kube-system"

$ kubectl get svc -n example-ns
Error from server (Forbidden): services is forbidden: User "system:serviceaccount:example-ns:example-sa" cannot list resource "services" in API group "" in the namespace "example-ns"
```

# X.509 Certificate

```yaml
# /etc/kubernetes/manifests/kube-apiserver.yaml
...<removed for brevity>...
spec:
  containers:
  - command:
    - kube-apiserver
    - --advertise-address=192.168.59.154
    - --allow-privileged=true
    - --authorization-mode=Node,RBAC
    - --client-ca-file=/var/lib/minikube/certs/ca.crt
...<removed for brevity>...
```

```shell
$ kubectl config view -o json | jq '.users[] | select(.name == "minikube")'
{
  "name": "minikube",
  "user": {
    "client-certificate": "/home/iamgini/.minikube/profiles/minikube/client.crt",
    "client-key": "/home/iamgini/.minikube/profiles/minikube/client.key"
  }
}
```

or

```shell
$ kubectl config view -o json | jq '.users[]'
{
  "name": "example-sa",
  "user": {
    "token": "REDACTED"
  }
}
{
  "name": "minikube",
  "user": {
    "client-certificate": "/home/iamgini/.minikube/profiles/minikube/client.crt",
    "client-key": "/home/iamgini/.minikube/profiles/minikube/client.key"
  }
}
```

Create Certificate and CSR

```shell
$ openssl genrsa -out iamgini.key 2048
$ openssl req -new -key iamgini.key -out iamgini.csr -subj "/CN=iamgini/O=web1/O=frontend"
$ cat iamgini.csr | base64 -w 0
```

```shell
$ kubectl apply -f csr.yaml
certificatesigningrequest.certificates.k8s.io/iamgini created
``

```shell
$ kubectl get csr
NAME      AGE   SIGNERNAME                            REQUESTOR       REQUESTEDDURATION   CONDITION
iamgini   25s   kubernetes.io/kube-apiserver-client   minikube-user   <none>              Pending

$ kubectl certificate approve iamgini
certificatesigningrequest.certificates.k8s.io/iamgini approved
```

Retreive certificate

```shell
$ kubectl get csr iamgini -o json | jq -r '.status.certificate' | base64 --decode > iamgini.crt
```

```shell
$ ls iamgini.*
iamgini.crt  iamgini.csr  iamgini.key
```

```shell
$ kubectl config set-credentials iamgini --client-key=/full-path/iamgini.key --client-certificate=/full-path/iamgini.crt
User "iamgini" set.
$ kubectl config set-context iamgini --cluster=minikube --user=iamgini
Context "iamgini" created.
$ kubectl config view
$ kubectl config get-contexts

$ kubectl config use-context iamgini
Switched to context "iamgini".

$ kubectl auth whoami
ATTRIBUTE   VALUE
Username    iamgini
Groups      [web1 frontend system:authenticated]
```


## RBAC

```shell
$ kubectl apply -f 02_rbac/rbac-demo-ns.yaml
namespace/rbac-demo-ns created

$ kubectl create -f 02_rbac/nginx-pod.yaml
pod/nginx-pod created

$ kubectl apply -f 02_rbac/pod-logger-serviceaccount.yaml
serviceaccount/pod-logger created

$ kubectl apply -f 02_rbac/pod-reader-role.yaml
role.rbac.authorization.k8s.io/pod-reader created

$ kubectl apply -f 02_rbac/pod-logger-app.yaml
pod/pod-logger-app created

$  kubectl get po -n rbac-demo-ns
NAME             READY   STATUS    RESTARTS   AGE
nginx-pod        1/1     Running   0          15m
pod-logger-app   1/1     Running   0          9s

$ kubectl exec -it -n rbac-demo-ns pod-logger-app -- bash
root@pod-logger-app:/# ls -l /var/run/secrets/kubernetes.io/serviceaccount/
total 0
lrwxrwxrwx 1 root root 13 Jul 14 03:33 ca.crt -> ..data/ca.crt
lrwxrwxrwx 1 root root 16 Jul 14 03:33 namespace -> ..data/namespace
lrwxrwxrwx 1 root root 12 Jul 14 03:33 token -> ..data/token


$ kubectl logs -n rbac-demo-ns pod-logger-app -f
Querying Kubernetes API Server for Pods in default namespace...
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   335  100   335    0     0  15678      0 --:--:-- --:--:-- --:--:-- 15952
{
  "kind": "Status",
  "apiVersion": "v1",
  "metadata": {},
  "status": "Failure",
  "message": "pods is forbidden: User \"system:serviceaccount:rbac-demo-ns:pod-logger\" cannot list resource \"pods\" in API group \"\" in the namespace \"kube-system\"",
  "reason": "Forbidden",
  "details": {
    "kind": "pods"
  },
  "code": 403
}

$ kubectl apply -f 02_rbac/read-pods-rolebinding.yaml
rolebinding.rbac.authorization.k8s.io/read-pods created


$ kubectl logs -n rbac-demo-ns pod-logger-app -f
...<removed for brevity>...
Querying Kubernetes API Server for Pods in default namespace...
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
{
  "kind": "PodList",
  "apiVersion": "v1",
  "metadata": {
    "resourceVersion": "4889"
  },
  "items": [
    {
      "metadata": {
        "name": "nginx-pod",
        "namespace": "rbac-demo-ns",
        "uid": "b62b2bdb-2677-4809-a134-9d6cfa07ecad",
...<removed for brevity>...
```

Delete RoleBinding and test again

```shell
$ kubectl delete -n rbac-demo-ns rolebindings read-pods
rolebinding.rbac.authorization.k8s.io "read-pods" deleted
```

## Admission controllers

```shell
$ minikube ssh 'sudo grep -- '--enable-admission-plugins' /etc/kubernetes/manifests/kube-apiserver.yaml'
    - --enable-admission-plugins=NamespaceLifecycle,LimitRanger,ServiceAccount,DefaultStorageClass,DefaultTolerationSeconds,NodeRestriction,MutatingAdmissionWebhook,ValidatingAdmissionWebhook,ResourceQuota
```

### Create SSL for admissiton controllers

```shell
# Create a Private Key for the CA:
$ openssl genrsa -out ca.key 2048

# Create a Self-Signed Certificate for the CA:
$ openssl req -x509 -new -nodes -key ca.key -sha256 -days 365 -out ca.crt -subj "/CN=my-admission-ca"

# Create a Private Key and CSR for the Admission Controller:
$ openssl req -new -newkey rsa:2048 -nodes -keyout admission-controller.key -out admission-controller.csr -config openssl.cnf

# Sign the Admission Controller CSR with the CA:
$ openssl x509 -req -in admission-controller.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out admission-controller.crt -days 365 -sha256

# For the certificate
$ cat admission-controller.crt | base64 -w 0

# For the key
$ cat admission-controller.key | base64 -w 0
```


```shell
# kubectl create secret tls admission-controller-secret \
#   --cert=admission-controller.crt \
#   --key=admission-controller.key \
#   --namespace admission-controllers
```

```shell
$ kubectl apply -f pod-with-security-context.yaml
pod/security-context-demo created
```

```shell
$ kubectl exec -it security-context-demo -- /bin/sh
~ $ id
uid=1000 gid=1000 groups=1000
~ $ touch /testfile
touch: /testfile: Read-only file system
~ $
```

## NetworkPolicy

```shell
$ minikube start --network-plugin=cni --cni=calico --container-runtime=containerd
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

## Private Registry Credentials in Kubernetes

```shell
$ kubectl create secret docker-registry my-registry-secret \
  --docker-server=your-registry.com \
  --docker-username=your_username \
  --docker-password=your_password \
  --docker-email=your-email@example.com
```