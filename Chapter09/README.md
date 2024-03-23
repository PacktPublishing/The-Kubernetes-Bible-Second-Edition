# Persistent Storage in Kubernetes

```shell
$ kubectl get persistentvolume
No resource found

$ kubectl get persistentvolumes
No resource found

$ kubectl get pv
No resource found
```

```shell
$ kubectl create -f pv-hostpath.yaml
persistentvolume/pv-hostpath created

$ kubectl describe pv pv-hostpath
Name:            pv-hostpath
Labels:          type=local
Annotations:     <none>
Finalizers:      [kubernetes.io/pv-protection]
StorageClass:    manual
Status:          Available
Claim:
Reclaim Policy:  Retain
Access Modes:    RWO
VolumeMode:      Filesystem
Capacity:        1Gi
Node Affinity:   <none>
Message:
Source:
    Type:          HostPath (bare host directory volume)
    Path:          /mnt/data
    HostPathType:
Events:            <none>
```


```shell
$ kubectl create -f pv.yaml
persistentvolume/my-hostpath-pv created
$ kubectl get pv
NAME             CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS      CLAIM   STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
my-hostpath-pv   1Gi        RWO            Retain           Available           slow           <unset>                          3s
```

```shell
$ kubectl create -f pvc.yaml
persistentvolumeclaim/my-hostpath-pvc created

$ kubectl get pv,pvc
NAME                              CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                     STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
persistentvolume/my-hostpath-pv   1Gi        RWO            Retain           Bound    default/my-hostpath-pvc   slow           <unset>                          17s

NAME                                    STATUS   VOLUME           CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
persistentvolumeclaim/my-hostpath-pvc   Bound    my-hostpath-pv   1Gi        RWO            slow           <unset>                 2s
```

```shell
$ kubectl create -f pod.yaml
pod/nginx created

$ kubectl get po
NAME    READY   STATUS    RESTARTS   AGE
nginx   1/1     Running   0          10s
```