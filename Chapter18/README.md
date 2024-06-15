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
    "client-certificate": "/home/gmadappa/.minikube/profiles/minikube/client.crt",
    "client-key": "/home/gmadappa/.minikube/profiles/minikube/client.key"
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