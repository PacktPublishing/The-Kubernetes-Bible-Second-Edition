#!/bin/sh

SERVICEACCOUNT=/var/run/secrets/kubernetes.io/serviceaccount
TOKEN=$(cat ${SERVICEACCOUNT}/token)

while true
do
  # Calculate CPU usage by hamster
  HAMSTER_USAGE=$(curl -s --cacert $SERVICEACCOUNT/ca.crt --header "Authorization: Bearer $TOKEN" -X GET https://kubernetes/apis/apps/v1/namespaces/default/deployments/elastic-hamster | jq ${TOTAL_HAMSTER_USAGE}/'.spec.replicas')

  # Hamster sleeps for the rest of the time, with a small adjustment factor
  HAMSTER_SLEEP=$(jq -n 1.2-$HAMSTER_USAGE)

  echo "Hamster uses $HAMSTER_USAGE and sleeps $HAMSTER_SLEEP"
  timeout ${HAMSTER_USAGE}s yes >/dev/null
  sleep ${HAMSTER_SLEEP}s
done
