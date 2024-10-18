
```shell
$ helm repo update
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "kubernetes-dashboard" chart repository
...Successfully got an update from the "stable" chart repository
...Successfully got an update from the "bitnami" chart repository
Update Complete. ⎈Happy Helming!⎈
```

```shell
$ helm install prometheus bitnami/kube-prometheus --create-namespace --namespace monitoring
NAME: prometheus
LAST DEPLOYED: Thu Jun  6 14:45:28 2024
NAMESPACE: monitoring
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
CHART NAME: kube-prometheus
CHART VERSION: 9.3.0
APP VERSION: 0.74.0

** Please be patient while the chart is being deployed **

Watch the Prometheus Operator Deployment status using the command:

    kubectl get deploy -w --namespace monitoring -l app.kubernetes.io/name=kube-prometheus-operator,app.kubernetes.io/instance=prometheus

Watch the Prometheus StatefulSet status using the command:

    kubectl get sts -w --namespace monitoring -l app.kubernetes.io/name=kube-prometheus-prometheus,app.kubernetes.io/instance=prometheus

Prometheus can be accessed via port "9090" on the following DNS name from within your cluster:

    prometheus-kube-prometheus-prometheus.monitoring.svc.cluster.local

To access Prometheus from outside the cluster execute the following commands:

    echo "Prometheus URL: http://127.0.0.1:9090/"
    kubectl port-forward --namespace monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090

Watch the Alertmanager StatefulSet status using the command:

    kubectl get sts -w --namespace monitoring -l app.kubernetes.io/name=kube-prometheus-alertmanager,app.kubernetes.io/instance=prometheus

Alertmanager can be accessed via port "9093" on the following DNS name from within your cluster:

    prometheus-kube-prometheus-alertmanager.monitoring.svc.cluster.local

To access Alertmanager from outside the cluster execute the following commands:

    echo "Alertmanager URL: http://127.0.0.1:9093/"
    kubectl port-forward --namespace monitoring svc/prometheus-kube-prometheus-alertmanager 9093:9093

WARNING: There are "resources" sections in the chart not set. Using "resourcesPreset" is not recommended for production. For production installations, please set the following values according to your workload needs:
  - alertmanager.resources
  - blackboxExporter.resources
  - operator.resources
  - prometheus.resources
  - prometheus.thanos.resources
+info https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/

```