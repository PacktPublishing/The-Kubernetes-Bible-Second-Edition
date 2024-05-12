# StatefulSet – Deploying Stateful Applications


## Create a secret

```shell
$ kubectl create ns mysql
```

```shell
$ kubectl create secret generic mysql-secret \
  --from-literal=MYSQL_ROOT_PASSWORD='mysqlroot' \
  --from-literal=MYSQL_USER='mysqluser' \
  --from-literal=MYSQL_PASSWORD='mysqlpassword' \
  -n mysql
```

```shell
$  kubectl create -f mysql-headless-service.yaml
service/mysql-headless created
```

```shell
$ kubectl apply -f mysql-statefulset.yaml
statefulset.apps/mysql-stateful created
```

```shell
$ kubectl get sts -n mysql
NAME             READY   AGE
mysql-stateful   3/3     2m3s


$ kubectl describe statefulsets -n mysql mysql-stateful
Name:               mysql-stateful
Namespace:          mysql
CreationTimestamp:  Sun, 12 May 2024 22:58:54 +0800
Selector:           app=mysql,environment=test
Labels:             app=mysql
Annotations:        <none>
Replicas:           3 desired | 3 total
Update Strategy:    RollingUpdate
  Partition:        0
Pods Status:        3 Running / 0 Waiting / 0 Succeeded / 0 Failed
Pod Template:
  Labels:  app=mysql
           environment=test
  Containers:
   mysql:
    Image:      mysql:8.4.0
    Port:       80/TCP
    Host Port:  0/TCP
    Environment:
      MYSQL_ROOT_PASSWORD:  <set to the key 'MYSQL_ROOT_PASSWORD' in secret 'mysql-secret'>  Optional: false
      MYSQL_USER:           <set to the key 'MYSQL_USER' in secret 'mysql-secret'>           Optional: false
      MYSQL_PASSWORD:       <set to the key 'MYSQL_PASSWORD' in secret 'mysql-secret'>       Optional: false
    Mounts:
      /var/lib/mysql from mysql-data (rw)
  Volumes:  <none>
Volume Claims:
  Name:          mysql-data
  StorageClass:
  Labels:        <none>
  Annotations:   <none>
  Capacity:      1Gi
  Access Modes:  [ReadWriteOnce]
Events:
  Type    Reason            Age   From                    Message
  ----    ------            ----  ----                    -------
  Normal  SuccessfulCreate  26s   statefulset-controller  create Claim mysql-data-mysql-stateful-0 Pod mysql-stateful-0 in StatefulSet mysql-stateful success
  Normal  SuccessfulCreate  26s   statefulset-controller  create Pod mysql-stateful-0 in StatefulSet mysql-stateful successful
  Normal  SuccessfulCreate  23s   statefulset-controller  create Claim mysql-data-mysql-stateful-1 Pod mysql-stateful-1 in StatefulSet mysql-stateful success
  Normal  SuccessfulCreate  23s   statefulset-controller  create Pod mysql-stateful-1 in StatefulSet mysql-stateful successful
  Normal  SuccessfulCreate  19s   statefulset-controller  create Claim mysql-data-mysql-stateful-2 Pod mysql-stateful-2 in StatefulSet mysql-stateful success
  Normal  SuccessfulCreate  19s   statefulset-controller  create Pod mysql-stateful-2 in StatefulSet mysql-stateful successful
```

```shell
$ kubectl get pod -n mysql
NAME               READY   STATUS    RESTARTS   AGE
mysql-stateful-0   1/1     Running   0          2m32s
mysql-stateful-1   1/1     Running   0          2m29s
mysql-stateful-2   1/1     Running   0          2m25s
```

```shell
$ kubectl -n mysql describe pod mysql-stateful-0
Name:             mysql-stateful-0
Namespace:        mysql
Priority:         0
Service Account:  default
...<removed for brevity>...
Volumes:
  mysql-data:
    Type:       PersistentVolumeClaim (a reference to a PersistentVolumeClaim in the same namespace)
    ClaimName:  mysql-data-mysql-stateful-0
    ReadOnly:   false


$ kubectl -n mysql describe pod mysql-stateful-1
Name:             mysql-stateful-1
Namespace:        mysql
Priority:         0
...<removed for brevity>...
Volumes:
  mysql-data:
    Type:       PersistentVolumeClaim (a reference to a PersistentVolumeClaim in the same namespace)
    ClaimName:  mysql-data-mysql-stateful-1
    ReadOnly:   false
...<removed for brevity>...
```

```shell
$ kubectl get pvc -n mysql
NAME                          STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
mysql-data-mysql-stateful-0   Bound    pvc-453dbfee-6076-48b9-8878-e7ac6f79d271   1Gi        RWO            standard       <unset>                 8m38s
mysql-data-mysql-stateful-1   Bound    pvc-36494153-3829-42aa-be6d-4dc63163ea38   1Gi        RWO            standard       <unset>                 8m35s
mysql-data-mysql-stateful-2   Bound    pvc-6730af33-f0b6-445d-841b-4fbad5732cde   1Gi        RWO            standard       <unset>                 8m31s
```

```shell
$ kubectl get pv
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                               STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
pvc-36494153-3829-42aa-be6d-4dc63163ea38   1Gi        RWO            Delete           Bound    mysql/mysql-data-mysql-stateful-1   standard       <unset>                          11m
pvc-453dbfee-6076-48b9-8878-e7ac6f79d271   1Gi        RWO            Delete           Bound    mysql/mysql-data-mysql-stateful-0   standard       <unset>                          11m
pvc-6730af33-f0b6-445d-841b-4fbad5732cde   1Gi        RWO            Delete           Bound    mysql/mysql-data-mysql-stateful-2   standard       <unset>                          11m
```

```shell
$ kubectl create -f k8sutils.yaml -n mysql
pod/k8sutils created
```

Test MySQL

```shell
$ kubectl exec -it -n mysql k8sutils -- /bin/bash
root@k8sutils:/#

root@k8sutils:/# mysql -u root -p -h mysql-headless.mysql.svc.cluster.local
Enter password:
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MySQL connection id is 9
Server version: 8.4.0 MySQL Community Server - GPL

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MySQL [(none)]> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
4 rows in set (0.003 sec)

MySQL [(none)]>
```

Check Headless service

```shell
root@k8sutils:/# nslookup mysql-headless
Server:         10.96.0.10
Address:        10.96.0.10#53

Name:   mysql-headless.mysql.svc.cluster.local
Address: 10.244.0.14
Name:   mysql-headless.mysql.svc.cluster.local
Address: 10.244.0.15
Name:   mysql-headless.mysql.svc.cluster.local
Address: 10.244.0.16
```

```shell
root@k8sutils:/# mysql -u root -p -h mysql-stateful-0.mysql-headless
Enter password:
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MySQL connection id is 13
Server version: 8.4.0 MySQL Community Server - GPL

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MySQL [(none)]>

MySQL [(none)]> create database ststest;
Query OK, 1 row affected (0.002 sec)
MySQL [(none)]> exit;
Bye
```

Delete and test

```shell
$ kubectl delete po -n mysql mysql-stateful-0

$ kubectl get po -n mysql
NAME               READY   STATUS    RESTARTS   AGE
k8sutils           1/1     Running   0          35m
mysql-stateful-0   1/1     Running   0          6s
mysql-stateful-1   1/1     Running   0          52m
mysql-stateful-2   1/1     Running   0          51m
```

```shell
root@k8sutils:/# mysql -u root -p -h mysql-stateful-0.mysql-headless
Enter password:
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MySQL connection id is 9
Server version: 8.4.0 MySQL Community Server - GPL

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MySQL [(none)]> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| ststest            |
| sys                |
+--------------------+
5 rows in set (0.003 sec)
```

```shell
$ kubectl delete po -n mysql mysql-stateful-0 mysql-stateful-1 mysql-stateful-2
pod "mysql-stateful-0" deleted
pod "mysql-stateful-1" deleted
pod "mysql-stateful-2" deleted

$ kubectl get pod -n mysql
NAME               READY   STATUS    RESTARTS   AGE
k8sutils           1/1     Running   0          47m
mysql-stateful-0   1/1     Running   0          44s
mysql-stateful-1   1/1     Running   0          43s
mysql-stateful-2   1/1     Running   0          41s

$ kubectl describe pod -n mysql -l app=mysql |egrep 'ClaimName|Name:'
Name:             mysql-stateful-0
    ClaimName:  mysql-data-mysql-stateful-0
    ConfigMapName:           kube-root-ca.crt
Name:             mysql-stateful-1
    ClaimName:  mysql-data-mysql-stateful-1
    ConfigMapName:           kube-root-ca.crt
Name:             mysql-stateful-2
    ClaimName:  mysql-data-mysql-stateful-2
    ConfigMapName:           kube-root-ca.crt
```

## Scaling

```shell
$ kubectl scale statefulset -n mysql mysql-stateful --replicas 4
statefulset.apps/mysql-stateful scaled

$ kubectl get pod -n mysql
NAME               READY   STATUS    RESTARTS   AGE
k8sutils           1/1     Running   0          56m
mysql-stateful-0   1/1     Running   0          9m13s
mysql-stateful-1   1/1     Running   0          9m12s
mysql-stateful-2   1/1     Running   0          9m10s
mysql-stateful-3   1/1     Running   0          4s

$ kubectl describe sts -n mysql mysql-stateful
Name:               mysql-stateful
Namespace:          mysql
...<removed for brevity>...
Events:
  Type    Reason                   Age                 From                    Message
  ----    ------                   ----                ----                    -------
  Normal  SuccessfulCreate         23m (x2 over 75m)   statefulset-controller  create Pod mysql-stateful-0 in StatefulSet mysql-stateful successful
  Normal  RecreatingTerminatedPod  11m (x13 over 23m)  statefulset-controller  StatefulSet mysql/mysql-stateful is recreating terminated Pod mysql-stateful-0
  Normal  SuccessfulDelete         11m (x13 over 23m)  statefulset-controller  delete Pod mysql-stateful-0 in StatefulSet mysql-stateful successful
  Normal  SuccessfulCreate         2m28s               statefulset-controller  create Claim mysql-data-mysql-stateful-3 Pod mysql-stateful-3 in StatefulSet mysql-stateful success
  Normal  SuccessfulCreate         2m28s               statefulset-controller  create Pod mysql-stateful-3 in StatefulSet mysql-stateful successful
```

```shell
$ kubectl scale statefulset -n mysql mysql-stateful --replicas 2
statefulset.apps/mysql-stateful scaled

$  kubectl get pvc -n mysql
NAME                          STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
mysql-data-mysql-stateful-0   Bound    pvc-453dbfee-6076-48b9-8878-e7ac6f79d271   1Gi        RWO            standard       <unset>                 79m
mysql-data-mysql-stateful-1   Bound    pvc-36494153-3829-42aa-be6d-4dc63163ea38   1Gi        RWO            standard       <unset>                 79m
mysql-data-mysql-stateful-2   Bound    pvc-6730af33-f0b6-445d-841b-4fbad5732cde   1Gi        RWO            standard       <unset>                 79m
mysql-data-mysql-stateful-3   Bound    pvc-6ec1ee2a-5be3-4bf9-84e5-4f5aee566c11   1Gi        RWO            standard       <unset>                 7m4s
```

```yaml
apiVersion: apps/v1
kind: StatefulSet
...
spec:
  persistentVolumeClaimRetentionPolicy:
    whenDeleted: Retain
    whenScaled: Delete
...
```

## Delete StatefulSet

```shell
$ kubectl delete sts -n mysql mysql-stateful
statefulset.apps "mysql-stateful" deleted

$ kubectl delete -n mysql pvc mysql-data-mysql-stateful-0 mysql-data-mysql-stateful-1 mysql-data-mysql-stateful-2 mysql-data-mysql-stateful-3
persistentvolumeclaim "mysql-data-mysql-stateful-0" deleted
persistentvolumeclaim "mysql-data-mysql-stateful-1" deleted
persistentvolumeclaim "mysql-data-mysql-stateful-2" deleted
persistentvolumeclaim "mysql-data-mysql-stateful-3" deleted
```
