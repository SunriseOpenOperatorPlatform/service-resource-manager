# Service Resource Manager
<br>
The Service Resource Manager (SRM) is a web service written in Python and and based on the Flask micro we framework. It implements the Service Resource manager role of the Operator Platform, defined by the  [GSMA Operator Platform Group (OPG)](https://www.gsma.com/solutions-and-impact/technologies/networks/gsma_resources/gsma-operator-platform-group-september-2024-publications/)

## Description
<br>
The Service Resource Manager facilitates the North-South Bound Interface (NSBI) specification of GSMA, by acting as an interconenction link between the CAMARA-defined API exposed by the Open Exposure Gateway, and the transformation functions that expose the underlying infrastructure techology. Since a principal goal of the SUNRISE6G Operator Platform is the exposure of diverse technology stacks, SRM seamlessly handles the Application Provider's request for infrastructure access by selecting the appropriate transformation function. 

SRM support the following CAMARA functions:

<br>

| Edge Cloud Management API  | Network Exposure API  (QoD & Traffic Influence)|
| ------------- | ------------- |
| Application Metadata registration  | Create QoD Session  |
| App Metadata Removal  | Remove QoD Session  |
| App Metadata Retrieval  | Retrieve QoD Session  |
| Application Instantiation  | Create TrafficeInfluence Resource  |
| Application Instance Retrieval  | Remove TrafficeInfluence Resource  |
| Application Instance Removal  | Retrieve TrafficeInfluence Resource  |
