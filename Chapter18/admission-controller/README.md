```shell
$ openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=admission-controller"

$ podman build -t quay.io/iamgini/k8s-admission-controller:1.0 .
$ podman push quay.io/iamgini/k8s-admission-controller:1.0
````