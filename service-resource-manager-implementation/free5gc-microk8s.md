# Free5GC and UERANSIM Kubernetes Deployment

Useful links:
 - [Free5GC User Guide](https://free5gc.org/guide/)
 - [ Free5gc-UERANSIM Kubernetes Deployment with helm](https://github.com/Orange-OpenSource/towards5gs-helm)

### Prepare VM
```
apt update
apt install curl git make gcc -y
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```


### Installing Microk8s

```
snap install microk8s --classic
newgrp microk8s
usermod -a -G microk8s $USER
chown -f -R $USER ~/.kube

su - $USER

microk8s status --wait-ready
```

### Set aliases
```
alias kubectl='microk8s kubectl'
alias k='microk8s kubectl'
alias helm='microk8s helm3'

echo "alias kubectl='microk8s kubectl'" >> ~/.bashrc
echo "alias k='microk8s kubectl'" >> ~/.bashrc
echo "alias helm='microk8s helm3'" >> ~/.bashrc
echo 'complete -F __start_kubectl k' >> ~/.bashrc # autocomplete for k8s

source ~/.bashrc
```

### config calico
```
# /var/snap/microk8s/current/args/cni-network/

microk8s kubectl apply -f /var/snap/microk8s/current/args/cni-network/cni.yaml
sudo snap restart microk8s

microk8s kubectl delete ippools default-ipv4-ippool
microk8s kubectl rollout restart daemonset/calico-node -n kube-system
```

```
microk8s enable dns ingress dashboard storage community helm3
microk8s enable multus
```


### Building gtp5g module
```
mkdir /root/5gc
cd /root/5gc
git clone https://github.com/free5gc/gtp5g.git
cd gtp5g
make
make install

```

### setting up ip forwarding in the node
```
echo "sudo sysctl -w net.ipv4.ip_forward=1" >> ~/.bashrc
echo "iptables -t nat -A POSTROUTING -o enp0s3 -j MASQUERADE" >> ~/.bashrc
echo "systemctl stop ufw" >> ~/.bashrc
echo "iptables -I FORWARD 1 -j ACCEPT" >> ~/.bashrc

source ~/.bashrc

```

### pull free5gc and ueransim repos
```
cd /root/5gc
helm repo add towards5gs 'https://raw.githubusercontent.com/Orange-OpenSource/towards5gs-helm/main/repo/'
helm repo update
helm search repo
helm pull towards5gs/free5gc; helm pull towards5gs/ueransim

tar -zxvf ueransim-2.0.17.tgz
tar -zxvf free5gc-1.1.7.tgz

```

### create the persistent volume for mongodb pod
```
cd /root/ ; mkdir kubedata
cd /root/5gc/
nano pv.yaml

---------

apiVersion: v1
kind: PersistentVolume
metadata:
  name: example-local-pv9
  labels:
    project: free5gc
spec:
  capacity:
    storage: 8Gi
  accessModes:
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  local:
    path: /root/kubedata
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - 5gcore

kubectl apply -f pv.yaml

```

### deploy free5gc and ueransim with helm

VM default interface: ```enp0s3```
VM IP: ```10.0.2.15```
VM Gateway: ```10.0.2.2```
VM Subnet: ```10.0.2.0```

```
k create ns 5g


helm -n 5g install free5gc towards5gs/free5gc \
    --set global.n2network.masterIf=enp0s3 \
    --set global.n3network.masterIf=enp0s3 \
    --set global.n4network.masterIf=enp0s3 \
    --set global.n9network.masterIf=enp0s3 \
    --set global.n6network.masterIf=enp0s3 \
    --set global.n6network.subnetIP=10.0.2.0 \
    --set global.n6network.gatewayIP=10.0.2.2 \
    --set global.n6network.excludeIP=10.0.2.2 \
    --set free5gc-upf.upf.n6if.ipAddress=10.0.2.11 \
    --set free5gc-upf.upf.securityContext.privileged=true 


    
helm -n 5g install  ueransim towards5gs/ueransim \
            --set global.n2network.masterIf=enp0s3 \
            --set global.n3network.masterIf=enp0s3
```

### how to uninstall
```
helm -n 5g uninstall free5gc 
helm -n 5g uninstall ueransim
```

### prepare upf

 - add google dns: ```echo "nameserver 8.8.8.8" >> /etc/resolv.conf```
 - add tcpdup tool:
```
apk update
apk add tcpdump
tcpdump -i any icmp
```
 - enable ip_forwarding in upf
```
echo "1" >  /proc/sys/net/ipv4/ip_forward
cat /proc/sys/net/ipv4/ip_forward
```
 - capture network traffic in pod: ```tcpdump -i any -s 0 -w /test-amf.pcap```


### MicroK8s CNI Configuration
 - https://microk8s.io/docs/change-cidr
 - ```/var/snap/microk8s/current/args/cni-network```


### Connect Multiple UEs (In Progress):

 - UE2 ConfigMap
```
apiVersion: v1
kind: ConfigMap
metadata:
  labels:
    app: ueransim
    component: ue2
  name: ue2-configmap
data:
  ue-config.yaml: |
    supi: "imsi-208930000000004"  # IMSI number
    mcc: '208' # Mobile Country Code value
    mnc: '93' # Mobile Network Code value (2 or 3 digits)
    key: "8baf473f2f8fd09487cccbd7097c6862" # Operator code (OP or OPC) of the UE
    op: "8e27b6af0e692e750f32667a3b14605e" # This value specifies the OP type and it can be either 'OP' or 'OPC'
    opType: "OPC" # This value specifies the OP type and it can be either 'OP' or 'OPC'
    amf: '8000' # Authentication Management Field (AMF) value
    imei: '356938035643803' # IMEI number of the device
    imeiSv: '4370816125816151'
    # UAC Access Identities Configuration
    uacAic:
      mps: false
      mcs: false
    # UAC Access Control Class
    uacAcc:
      normalClass: 0
      class11: false
      class12: false
      class13: false
      class14: false
      class15: false
    sessions:
      - type: "IPv4"
        apn: "internet"
        slice:
          sst: 0x01
          sd: 0x010203
    # Configured NSSAI for this UE by HPLMN
    configured-nssai:
      - sst: 0x01
        sd: 0x010203
    # Default Configured NSSAI for this UE
    default-nssai:
      - sst: 1
        sd: 1
    # Supported encryption and integrity algorithms by this UE
    integrity:
      IA1: true
      IA2: true
      IA3: true
    ciphering:
      EA1: true
      EA2: true
      EA3: true
    # Integrity protection maximum data rate for user plane
    integrityMaxRate:
      uplink: 'full'
      downlink: 'full'

    # List of gNB IP addresses for Radio Link Simulation
    gnbSearchList:
      - gnb-service
  wrapper.sh: |
    #!/bin/bash

    mkdir /dev/net
    mknod /dev/net/tun c 10 200

    ./nr-ue -c ../config/ue-config.yaml
```

 - UE2 Deployment
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ueransim-ue2
  labels:
    app: ueransim
    component: ue2
spec:
  selector:
    matchLabels:
      app: ueransim
      component: ue2
  replicas: 1
  template:
    metadata:
      labels:
        app: ueransim
        component: ue2
    spec:
      containers:
      - command:
        - /ueransim/config/wrapper.sh
        image: towards5gs/ueransim-ue:v3.2.6
        name: ue2
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
        securityContext:
          capabilities:
            add:
            - NET_ADMIN
        volumeMounts:
        - mountPath: /ueransim/config
          name: ue-volume2
      dnsPolicy: ClusterFirst
      restartPolicy: Always
      securityContext: {}
      volumes:
      - configMap:
          defaultMode: 420
          items:
          - key: ue-config.yaml
            path: ue-config.yaml
          - key: wrapper.sh
            mode: 493
            path: wrapper.sh
          name: ue2-configmap
        name: ue-volume2
```


### multiple UPFs attemps (In Progress)

```
helm -n 5g install free5gc towards5gs/free5gc \
    --set global.userPlaneArchitecture=ulcl \
    --set global.n2network.masterIf=enp0s3 \
    --set global.n3network.masterIf=enp0s3 \
    --set global.n4network.masterIf=enp0s3 \
    --set global.n9network.masterIf=enp0s3 \
    --set global.n6network.masterIf=enp0s3 \
    --set global.n6network.subnetIP=10.0.2.0 \
    --set global.n6network.gatewayIP=10.0.2.2 \
    --set global.n6network.excludeIP=10.0.2.2 \
    --set free5gc-upf.upf1.n6if.ipAddress=10.0.2.17 \
    --set free5gc-upf.upf1.securityContext.privileged=true \
    --set free5gc-upf.upf2.n6if.ipAddress=10.0.2.18 \
    --set free5gc-upf.upf2.securityContext.privileged=true \
    --set free5gc-upf.upfb.n6if.ipAddress=10.0.2.19 \
    --set free5gc-upf.upfb.securityContext.privileged=true

helm -n 5g install free5gc towards5gs/free5gc \
    --set global.userPlaneArchitecture=ulcl \
    --set global.n2network.masterIf=enp0s3 \
    --set global.n3network.masterIf=enp0s3 \
    --set global.n4network.masterIf=enp0s3 \
    --set global.n9network.masterIf=enp0s3 \
    --set global.n6network.masterIf=enp0s3 \
    --set global.n6network.subnetIP=10.0.2.0 \
    --set global.n6network.gatewayIP=10.0.2.2 \
    --set global.n6network.excludeIP=10.0.2.2 \
    --set free5gc-upf.upf1.n6if.ipAddress=10.0.2.17 \
    --set free5gc-upf.upf1.securityContext.privileged=true \
    --set free5gc-upf.upf2.n6if.ipAddress=10.0.2.18 \
    --set free5gc-upf.upf2.securityContext.privileged=true \
    --set free5gc-upf.upf3.n6if.ipAddress=10.0.2.20 \
    --set free5gc-upf.upf3.securityContext.privileged=true \
    --set free5gc-upf.upfb.n6if.ipAddress=10.0.2.19 \
    --set free5gc-upf.upfb.securityContext.privileged=true


```


