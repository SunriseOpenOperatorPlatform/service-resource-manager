from __future__ import print_function
import os
import time
from swagger_server.utils import connector_db
import requests
import json
import copy
from requests.structures import CaseInsensitiveDict
# import traceback
# import logging



def create_value_and_device(iot_device):

    #first check if edgex exists:

    edgex_paas_service_ = connector_db.get_documents_from_collection("deployed_paas_services",
                                                                        input_type="instance_name",
                                                                        input_value="edgex")
    if not edgex_paas_service_:
        return "EdgeX PaaS service not found in the cluster"

    #create value descriptor
    url = "http://edgex-core-data.pi-edge:48080" + "/api/v1/valuedescriptor"

    f=open(os.path.join(os.path.split(os.path.dirname(__file__))[0], 'iot_devices_files/value_descriptor.json'))

    value_descriptor = json.load(f)
    for value_des in iot_device.values:

        value_descriptor["name"]=value_des.name
        value_descriptor["description"]=value_des.description
        value_descriptor["type"]=value_des.type
        value_descriptor["min"]=value_des.min
        value_descriptor["max"]=value_des.max
        value_descriptor["uomLabel"]=value_des.name
        value_descriptor["labels"][1]=value_des.name

        requests.post(url, json=value_des.to_dict(), verify=False)


    #upload the device profile
    url = "http://edgex-core-metadata.pi-edge:48081" + "/api/v1/deviceprofile/uploadfile"

    fv= open(os.path.join(os.path.split(os.path.dirname(__file__))[0], 'iot_devices_files/sensor_Cluster_Device_Profile.json'), encoding='utf-8-sig')

    device_profile = json.load(fv)
    device_profile["name"]= iot_device.device_cluster
    device_profile["description"]= iot_device.device_cluster +" metrics"

    device_resource=device_profile["deviceResources"][0]

    device_resources=[]
    for value_des in iot_device.values:

        device_resource_=copy.deepcopy(device_resource)

        device_resource_["name"]=value_des.name
        device_resource_["description"]=iot_device.device_cluster+ " "+  value_des.name +" values"
        device_resource_["properties"]["value"]["type"]=value_des.type
        device_resource_["properties"]["value"]["minimum"]=value_des.min
        device_resource_["properties"]["value"]["maximum"]=value_des.max


        device_resources.append(device_resource_)

    device_profile["deviceResources"]=copy.deepcopy(device_resources)

    with open((os.path.join(os.path.split(os.path.dirname(__file__))[0],"iot_devices_files/sensor_Cluster_Device_Profile.json")),"w") as jsonFile:
        json.dump(device_profile, jsonFile)

    #f2 = open(os.path.join(os.path.split(os.path.dirname(__file__))[0], 'iot_devices_files/sensor_Cluster_Device_Profile.json'), encoding='utf-8-sig')
    f2 = open((os.path.join(os.path.split(os.path.dirname(__file__))[0],"iot_devices_files/sensor_Cluster_Device_Profile.json")),"rb")
    #files = {'file': open((os.path.join(os.path.split(os.path.dirname(__file__))[0],"iot_devices_files/sensor_Cluster_Device_Profile.json")))}
    # print(f2)

    requests.post(url, files={"file": f2}, verify=False)

    #create device
    url = "http://edgex-core-metadata.pi-edge:48081" + "/api/v1/device"
    #url = "http://10.152.183.110:48081" + "/api/v1/device"

    fd = open(os.path.join(os.path.split(os.path.dirname(__file__))[0],
                           'iot_devices_files/device.json'), encoding='utf-8-sig')

    device = json.load(fd)

    device["name"]=iot_device.device_name
    device["description"]=iot_device.description
    device["location"]=iot_device.location.to_dict()
    device["profile"]["name"]=iot_device.device_cluster

    requests.post(url, json=device, verify=False)

    #create the stream pipeline

    url = "http://edgex-kuiper.pi-edge:48075" + "/streams"
    #url = "http://10.152.183.185:48075" + "/streams"

    stream={}
    stream["sql"]="create stream "+iot_device.device_name+"() WITH (FORMAT=\"JSON\", TYPE=\"edgex\")"

    requests.post(url, json=stream, verify=False)

    return "Device registered successfully"

