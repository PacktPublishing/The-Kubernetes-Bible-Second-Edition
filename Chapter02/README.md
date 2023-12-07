# Kubernetes Architecture – From Container Images to Running Pods 

```shell
$ kubectl run nginx --restart Never --image nginx
```


## Installing kubectl onIn Linux,

```shell
$ chmod +x ./kubectl 

$ sudo mv ./kubectl /usr/local/bin/kubectl 

$ kubectl version 

Client Version: v1.28.2 

Kustomize Version: v5.0.4-0.20230601165947-6ce0bf390ce3 

The connection to the server localhost:8080 was refused - did you specify the right host or port? 
```

## Installing kubectl On macOS

```shell
# Intel 

$ curl -LO "https://dl.k8s.io/release/$(curl -L -s 

 https://dl.k8s.io/release/stable.txt)/bin/darwin/amd64/kubectl" 

# Aple Silicon 

$ curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/arm64/kubectl" 

$ chmod +x ./kubectl 

$ sudo mv ./kubectl /usr/local/bin/kubectl 

$ sudo chown root: /usr/local/bin/kubectl 
```

## Installing kubectl on Windows

```shell
$ curl.exe -LO https://dl.k8s.io/release/v1.28.4/bin/windows/amd64/kubectl.exe 

# Append or prepend the kubectl binary folder to your PATH environment variable and test to ensure the version of kubectl matches the downloaded one. 
```