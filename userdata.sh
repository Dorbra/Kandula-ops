#!/bin/bash
sudo touch USERDATA_SUCCESS.txt

aws eks update-kubeconfig --region us-east-1 --name dorbra-kandula-prod-23
kubectl create secret generic consul-gossip-encryption-key --from-literal=key="uDBV4e+LbFW3019YKPxIrg=="
kubectl apply -f dnsutils.yaml
helm install consul hashicorp/consul -f values.yaml
CONSULIP=$(kubectl get svc consul-consul-dns | tail -1 |awk '{ print $3 }')
sed -i -e "s/CONSULIP/${CONSULIP}/g" configmap.yaml
kubectl apply -f configmap.yaml
sed -i -e "s/${CONSULIP}/CONSULIP/g" configmap.yaml

