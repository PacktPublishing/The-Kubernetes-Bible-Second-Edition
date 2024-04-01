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

$ kubectl get pod,pv,pvc
NAME        READY   STATUS    RESTARTS   AGE
pod/nginx   1/1     Running   0          6s

NAME                              CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                     STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
persistentvolume/my-hostpath-pv   1Gi        RWO            Retain           Bound    default/my-hostpath-pvc   slow           <unset>                          61m

NAME                                    STATUS   VOLUME           CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
persistentvolumeclaim/my-hostpath-pvc   Bound    my-hostpath-pv   1Gi        RWO            slow           <unset>                 61m
```

```shell
$ kubectl api-resources --namespaced=false |grep -i volume
persistentvolumes                 pv           v1                                false        PersistentVolume
volumeattachments                              storage.k8s.io/v1                 false        VolumeAttachment
```

Demonstrate Reclaim policy difference

```shell
$ kubectl get pod,pvc,pv
NAME        READY   STATUS    RESTARTS   AGE
pod/nginx   1/1     Running   0          15s

NAME                                    STATUS   VOLUME           CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
persistentvolumeclaim/my-hostpath-pvc   Bound    my-hostpath-pv   1Gi        RWO            slow           <unset>                 34s

NAME                              CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                     STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
persistentvolume/my-hostpath-pv   1Gi        RWO            Retain           Bound    default/my-hostpath-pvc   slow           <unset>                          40s

$ kubectl delete pod nginx
pod "nginx" deleted
$ kubectl delete pvc my-hostpath-pvc
persistentvolumeclaim "my-hostpath-pvc" deleted

$ kubectl get pod,pvc,pv
NAME                              CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS     CLAIM                     STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
persistentvolume/my-hostpath-pv   1Gi        RWO            Retain           Released   default/my-hostpath-pvc   slow           <unset>                          4m38s

```

Patching reclaim policy

```shell
$ kubectl patch pv/my-hostpath-pv -p '{"spec":{"persistentVolumeReclaimPolicy":"Delete"}}'
persistentvolume/my-hostpath-pv patched

$ kubectl get pod,pvc,pv
No resources found
```

```shell
$ kubectl get sc
NAME                 PROVISIONER                RECLAIMPOLICY   VOLUMEBINDINGMODE   ALLOWVOLUMEEXPANSION   AGE
standard (default)   k8s.io/minikube-hostpath   Delete          Immediate           false                  21d

$ kubectl get storageclasses standard  -o yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
...<removed for brevity>...
  name: standard
  resourceVersion: "290"
  uid: f41b765f-301f-4781-b9d0-46aec694336b
provisioner: k8s.io/minikube-hostpath
reclaimPolicy: Delete
volumeBindingMode: Immediate
```

## Dynamic Provisioning

```shell
$ kubectl create ns dynamicstorage
namespace/dynamicstorage created

$ kubectl get sc
NAME                 PROVISIONER                RECLAIMPOLICY   VOLUMEBINDINGMODE   ALLOWVOLUMEEXPANSION   AGE
standard (default)   k8s.io/minikube-hostpath   Delete          Immediate           false                  21d

$ kubectl create -f pvc-dynamic.yaml -n dynamicstorage
persistentvolumeclaim/my-dynamic-hostpath-pvc created

$ kubectl get pod,pvc,pv -n dynamicstorage
NAME                                            STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
persistentvolumeclaim/my-dynamic-hostpath-pvc   Bound    pvc-4597ab27-c894-40de-a7ac-1b6ca961bcdc   1Gi        RWO            standard       <unset>                 7s

NAME                                                        CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                                    STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
persistentvolume/pvc-4597ab27-c894-40de-a7ac-1b6ca961bcdc   1Gi        RWO            Delete           Bound    dynamicstorage/my-dynamic-hostpath-pvc   standard       <unset>                          7s

$ kubectl create -f pod-with-dynamic-pvc.yaml -n dynamicstorage
pod/nginx-dynamic-storage created

$ kubectl get pod,pvc,pv -n dynamicstorage
NAME                        READY   STATUS    RESTARTS   AGE
pod/nginx-dynamic-storage   1/1     Running   0          45s

NAME                                            STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
persistentvolumeclaim/my-dynamic-hostpath-pvc   Bound    pvc-4597ab27-c894-40de-a7ac-1b6ca961bcdc   1Gi        RWO            standard       <unset>                 7m39s

NAME                                                        CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                                    STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
persistentvolume/pvc-4597ab27-c894-40de-a7ac-1b6ca961bcdc   1Gi        RWO            Delete           Bound    dynamicstorage/my-dynamic-hostpath-pvc   standard       <unset>                          7m39s

$ kubectl delete po nginx-dynamic-storage -n dynamicstorage
pod "nginx-dynamic-storage" deleted

$ kubectl delete pvc my-dynamic-hostpath-pvc -n dynamicstorage
persistentvolumeclaim "my-dynamic-hostpath-pvc" deleted

$ kubectl get pod,pvc,pv -n dynamicstorage
No resources found
```