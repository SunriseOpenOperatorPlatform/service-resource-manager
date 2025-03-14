```mermaid
sequenceDiagram
title Retrieve Edge Cloud Zones
actor AP as App Vertical Provider
participant CE as Capabilities Exposure
box Service Resource Manager
    participant API
    participant SDK as EdgeCloudSDK
end
participant i2Edge
participant PiEdge

note over AP,CE: CAMARA EdgeCloud API
AP ->> CE: GET /edge-cloud-zones
CE ->> API: GET /av. zones
API ->> SDK: sdk.i2edge.get_zones()
SDK ->> i2Edge: GET /zones/list
API ->> SDK: sdk.piedge.get_zones()
SDK ->> PiEdge: GET /nodes
```