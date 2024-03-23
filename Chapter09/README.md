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
