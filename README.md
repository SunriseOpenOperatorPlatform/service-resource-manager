# Service Resource Manager

The Service Resource Manager (SRM) is a web service written in Python and and based on the Flask micro we framework. It implements the Service Resource manager role of the Operator Platform, defined by the  [GSMA Operator Platform Group (OPG)](https://www.gsma.com/solutions-and-impact/technologies/networks/gsma_resources/gsma-operator-platform-group-september-2024-publications/)

## Description

The Service Resource Manager facilitates the North-South Bound Interface (NSBI) specification of GSMA, by acting as an interconenction link between the CAMARA-defined API exposed by the Open Exposure Gateway, and the transformation functions that expose the underlying infrastructure techology. Since a principal goal of the SUNRISE6G Operator Platform is the exposure of diverse technology stacks, SRM seamlessly handles the Application Provider's request for infrastructure access by selecting the appropriate transformation function. 

SRM supports the following CAMARA functions:

NOTE: NEF APIs are not yet implemented

<br>

| Edge Cloud Management API  | Network Exposure API  (QoD & Traffic Influence)|
| ------------- | ------------- |
| Application Metadata registration  | Create QoD Session  |
| App Metadata Removal  | Remove QoD Session  |
| App Metadata Retrieval  | Retrieve QoD Session  |
| Application Instantiation  | Create TrafficeInfluence Resource  |
| Application Instance Retrieval  | Remove TrafficeInfluence Resource  |
| Application Instance Removal  | Retrieve TrafficeInfluence Resource  |

## Deployment

SRM can be deployed in a Kubernetes cluster by executing the file _srm-deployment.yaml_ located in the root folder. This file will create a SRM Deployment resource and its supporting native K8s Service. The following table contains the necesssary environment variables for the Kubernetes adapter. If you have defined a custom adapter, include your variables accordingly.

| Edge Cloud Management API  | Description |
| ------------- | ------------- |
|  KUBERNETES_MASTER_IP |  Root url of the Kubernetes apiserver (eg. 10.10.10.10)|
| KUBERNETES_MASTER_PORT  |  Port of the Kubernetes apiserver (eg. 16443)|
| EMP_STORAGE_URI  | Root url of the management database, if deployed  |
|  KUBERNETES_MASTER_TOKEN | Token with which all access to K8s apiserver will authenticated  |
|  ARTIFACT_MANAGER_ADDRESS |  Address of the Artefact Manager |
| EDGE_CLOUD_ADAPTER_NAME  | The adapter SRM is going to use throughout its lifecycle. For direct access to K8s just type 'kubernetes'  |
|PLATFORM_PROVIDER| The Edge Cloud infrastructure provider|

## Usage

Assuming an instance of Open Exposure Gateway (OEG) is running so that CAMARA APIs are accessible, here are a few request examples with responses, all CAMARA compatible:

### Get all registered apps

_curl -X GET http://[OEG_address]/apps_

Example response:

_[
  {
    "appId": "68503f9fe81dc7441fdaae94",
    "appRepo": {
      "imagePath": "mongo:4.4.18"
    },
    "componentSpec": [
      {
        "componentName": "mongodb",
        "networkInterfaces": [
          {
            "port": 27017,
            "protocol": "TCP"
          }
        ]
      }
    ],
    "name": "mongodb",
    "packageType": "QCOW2"
  },
  {
    "appId": "685122aa8fff437507ec8932",
    "appRepo": {
      "imagePath": "nginx"
    },
    "componentSpec": [
      {
        "componentName": "nginx",
        "networkInterfaces": [
          {
            "port": 80,
            "protocol": "TCP"
          },
          {
            "port": 443,
            "protocol": "TCP"
          }
        ]
      }
    ],
    "name": "nginx",
    "packageType": "QCOW2"
  }
]_

### Register app metadata

_curl -X POST http://172.18.0.2:32414/apps --data '{"name": "nginx", "version": "1", "packageType": "QCOW2", "appRepo": {"imagePath": "nginx", "type": "PRIVATEREPO"}
, "componentSpec": [{"componentName": "nginx", "networkInterfaces": [{"protocol": "TCP", "port": 80, "interfaceId": "Uj6qThvzkegxa3L4b88", "visibilityType": "VISIBILITY_EXTERNAL"}, {"protoco
l": "TCP", "port": 443, "interfaceId": "Uj6qThvzkegxa3L4b88", "visibilityType": "VISIBILITY_EXTERNAL"}]}]}' -H "Content-Type: application/json"_

Example Response:

_{
  "appId": "685bdc7dc2db24cc0e8927dc"
}_

### Instantiate registered app

