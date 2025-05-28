from __future__ import print_function
import os
import time
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from swagger_server.utils import auxiliary_functions
from pprint import pprint
from swagger_server.models import NodesResponse
from swagger_server.utils import connector_db
configuration = client.Configuration()
import requests
import paramiko
from requests.structures import CaseInsensitiveDict
# import traceback
import logging
from swagger_server.models.service_function_node_migration import ServiceFunctionNodeMigration
import json

#K8S AUTH

adapter_name = os.environ['EDGE_CLOUD_ADAPTER_NAME']
if adapter_name=='piedge':

    master_node_password=os.environ["KUBERNETES_MASTER_PASSWORD"].strip()
    master_node_hostname=os.environ["KUBERNETES_MASTER_HOSTNAME"].strip()
    master_node_ip=os.environ["KUBERNETES_MASTER_IP"].strip()
    master_node_port=os.environ["KUBERNETES_MASTER_PORT"].strip()
    token_k8s=os.environ["KUBERNETES_MASTER_TOKEN"].strip()
    kube_config_path=os.environ["KUBE_CONFIG_PATH"].strip()
    username = os.environ["KUBERNETES_USERNAME"].strip()

    host="https://"+master_node_ip+":"+master_node_port
    configuration.api_key['authorization'] = token_k8s
    configuration.api_key_prefix['authorization'] = 'Bearer'

    configuration.host =  host

    configuration.username = username
    configuration.verify_ssl=False

    # config.load_kube_config(config_file=kube_config_path)
    v1 = client.CoreV1Api(client.ApiClient(configuration))

    # config.lod
    #client.Configuration.set_default(configuration)
    #Defining host is optional and default to http://localhost
    # Enter a context with an instance of the API kubernetes.client
    with client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
        api_instance = client.AdmissionregistrationApi(api_client)
        api_instance_appsv1 = client.AppsV1Api(api_client)
        api_instance_apiregv1 = client.ApiregistrationV1beta1Api(api_client)
        api_instance_v1autoscale = client.AutoscalingV1Api(api_client)
        api_instance_v2beta1autoscale = client.AutoscalingV2beta1Api(api_client)
        api_instance_v2beta2autoscale = client.AutoscalingV2beta2Api(api_client)
        api_instance_corev1api = client.CoreV1Api(api_client)
        api_instance_storagev1api = client.StorageV1Api(api_client)
        api_instance_batchv1 = client.BatchV1Api(api_client)

        api_custom=client.CustomObjectsApi(api_client)
        try:
            api_response = api_instance.get_api_group()
        except ApiException as e:
            print("Exception when calling AdmissionregistrationApi->get_api_group: %s\n" % e)

#!!!!!!!!!!!!!!!!
# Configure API key authorization: BearerToken
# configuration.api_key['authorization'] = token_k8s
#!!!!!!!!!!!!!!!!


# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['authorization'] = 'Bearer'

# configuration.host =  host

# configuration.username = "user"
# configuration.verify_ssl=False

#################### Works when we run the controller on the localhost!!!!!!!!###################
#config.load_kube_config()
#v1 = client.CoreV1Api()
#########################################################


def add_node(node_info):

    #retrieve the command that the new node should execute
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(master_node_ip,22, master_node_hostname,master_node_password)
    #stdin, stdout, stderr= ssh.exec_command("microk8s add-node")
    stdin, stdout, stderr= ssh.exec_command("echo '"+master_node_password+"' | sudo -S -k microk8s add-node")
    #example: stdin, stdout, stderr= ssh.exec_command("echo '146.124.106.253 testcode' | sudo tee -a  /etc/hosts")
    stdout.channel.set_combine_stderr(True)
    lines= stdout.readlines()
    command_worker=lines[1][:-2] + " --worker"




    #first check if ip exists in /etc/hosts at master node!
    stdin_check, stdout_check, stderr_check = ssh.exec_command("grep "+node_info["ip"]+ " /etc/hosts")
    lines_check=stdout_check.readlines()


    if len(lines_check)==0:
        # write host to /etc/host of master node
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(master_node_ip, 22, master_node_hostname, master_node_password)
        # was implemtented using these commnads (complex) because we couldn't execute a simple sudo echo to /etc/hosts: we got permission denied!!!!
        stdin_check, stdout_check, stderr_check = ssh.exec_command("echo '"+master_node_password+"' | sudo -S -k cp /dev/null hosts")
        stdin_check, stdout_check, stderr_check =ssh.exec_command("echo '"+master_node_password+"' | sudo -S -k cp /etc/hosts hosts")
        stdin_check, stdout_check, stderr_check =ssh.exec_command("cp /dev/null new_host")
        stdin_check, stdout_check, stderr_check =ssh.exec_command("echo '" + node_info["ip"] + " " + node_info["name"] + "' |  tee -a  new_host")
        stdin_check, stdout_check, stderr_check =ssh.exec_command("echo '"+master_node_password+"' | sudo -S -k cat hosts new_host >> hosts")
        stdin_check, stdout_check, stderr_check =ssh.exec_command("echo '"+master_node_password+"' | sudo -S -k cp hosts /etc/hosts")


    #then should exexute the command to new node cli

    #execute the command to the new node

    ssh_worker_node = paramiko.SSHClient()
    ssh_worker_node.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_worker_node.connect(node_info["ip"], 22, node_info["hostname"], node_info["password"])

    #### configure firewall to allow pod-to-pod and pod-to-internet communication######
    stdin_worker_node, stdout_worker_node, stderr_worker_node = ssh_worker_node.exec_command("echo '"+node_info["password"]+"' | sudo -S -k ufw allow in on cni0 && sudo ufw allow out on cni0")
    stdin_worker_node, stdout_worker_node, stderr_worker_node = ssh_worker_node.exec_command("echo '"+node_info["password"]+"' | sudo -S -k ufw default allow routed")

    ########################################################################################

    command_worker_final= "echo '"+node_info["password"]+"' | sudo -S -k "+ command_worker + " --skip-verify"

    stdin_worker_node, stdout_worker_node, stderr_worker_node = ssh_worker_node.exec_command(command_worker_final)
    stdout_worker_node.channel.set_combine_stderr(True)
    lines_worker = stdout_worker_node.readlines()


    if any("The node has joined the cluster" in word for word in lines_worker):

    #if "The node has joined the cluster" in lines_worker[2]:

        # ssh to master node again and -> add label to new node#
        # kubectl label nodes k8sthird location = Peania_Athens_19002_3
        #print("echo '"+master_node_password+"' | sudo -S -k microk8s.kubectl label nodes "+node_info["name"]+ " location="+node_info["location"])
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(master_node_ip, 22, master_node_hostname, master_node_password)

        while(True):
            stdin, stdout, stderr = ssh.exec_command("echo '"+master_node_password+"' | sudo -S -k microk8s.kubectl get nodes ")
            stdout.channel.set_combine_stderr(True)
            lines_get_node = stdout.readlines()
            if any(node_info["name"] in word for word in lines_get_node):
                #node READY!!!
                break

        # need to check if node was added to cluster (kubectl get nodes)
        stdin, stdout, stderr = ssh.exec_command("echo '"+master_node_password+"' | sudo -S -k microk8s.kubectl label nodes "+node_info["name"]+ " location="+node_info["location"] + " node_type="+node_info["node_type"])

        logging.info("Node added")

        final_result ="Node added successfully!"

    else:
        final_result= "Node NOT added successfully!"


    return final_result




def remove_node(node_info):

    ssh_worker_node = paramiko.SSHClient()
    ssh_worker_node.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_worker_node.connect(node_info["ip"], 22, node_info["hostname"], node_info["password"])
    #cdm="microk8s leave"
    #stdin_worker_node, stdout_worker_node, stderr_worker_node=ssh_worker_node.exec_command(nohup %s &' % cdm, timeout=1)

    #THIS TAKES SOME TIME TO EXECUTE! NEED TO FIND A BETTER IMPLEMENTATION
    command_worker_final = "echo '" + node_info["password"] + "' |  sudo -S -k microk8s leave"
    stdin_worker_node, stdout_worker_node, stderr_worker_node = ssh_worker_node.exec_command(command_worker_final)
    stdout_worker_node.channel.set_combine_stderr(True)
    lines_worker = stdout_worker_node.readlines()

    #retrieve the command that the new node should execute
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(master_node_ip,22,master_node_hostname,master_node_password)
    #stdin, stdout, stderr= ssh.exec_command("microk8s add-node")
    stdin, stdout, stderr= ssh.exec_command("echo '"+master_node_password+"' | sudo -S -k microk8s remove-node "+node_info["name"])
    #stdin, stdout, stderr= ssh.exec_command("echo '146.124.106.253 k8sSadadada23132242' | sudo tee -a  /etc/hosts")
    stdout.channel.set_combine_stderr(True)

    return "Node deleted"


def execute_with_ssh_and_cli(commands):


    #retrieve the command that the new node should execute
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())


    for command in commands:
        ssh.connect(master_node_ip,22, master_node_hostname,master_node_password)
        stdin, stdout, stderr= ssh.exec_command(command)

        stdout.channel.set_combine_stderr(True)
        #lines= stdout.readlines()


def get_PoP_statistics(nodeName):

    #x1 = v1.list_node().to_dict()

    try:
        url = host + "/api/v1/nodes"
        headers = {"Authorization": "Bearer " + token_k8s}
        x = requests.get(url, headers=headers, verify=False)
        x1=x.json()
    except requests.exceptions.HTTPError as e:
        # logging.error(traceback.format_exc())
        return ("Exception when calling CoreV1Api->/api/v1/namespaces/sunrise6g/persistentvolumeclaims: %s\n" % e)
    k8s_nodes = api_custom.list_cluster_custom_object("metrics.k8s.io", "v1beta1", "nodes")


    # client.models.v1_node_list.V1NodeList
    # kubernetes.client.models.v1_node_list.V1NodeList\


    pop_output= {}
    for pop in x1['items']:

        name=pop['metadata']['name']
        if name==nodeName:
            pop_output["nodeName"]=name
            pop_output["nodeId"]=pop['metadata']['uid']
            pop_output["nodeLocation"]= pop['metadata']['labels']['location']

            node_addresses={}
            node_addresses["nodeHostName"]=pop['status']['addresses'][1]['address']
            node_addresses["nodeExternalIP"]=pop['status']['addresses'][0]['address']
            node_addresses["nodeInternalIP"]=pop['metadata']['annotations']['projectcalico.org/IPv4VXLANTunnelAddr']
            pop_output["nodeAddresses"]=node_addresses


            node_conditions={}
            for condition in pop['status']['conditions']:
                type=condition['type']
                node_type="node"+type
                node_conditions[node_type] = condition['status']
            pop_output["nodeConditions"] = node_conditions

            node_capacity= {}
            node_capacity["nodeCPUCap"]=pop['status']['capacity']['cpu']
            memory=pop['status']['capacity']['memory']
            memory_size=len(memory)
            node_capacity["nodeMemoryCap"]=memory[:memory_size - 2]
            node_capacity["nodeMemoryCapMU"]=memory[-2:]
            storage = pop['status']['capacity']['ephemeral-storage']
            storage_size = len(storage)
            node_capacity["nodeStorageCap"]=storage[:storage_size - 2]
            node_capacity["nodeStorageCapMU"]=storage[-2:]
            node_capacity["nodeMaxNoofPods"]=pop['status']['capacity']['pods']
            pop_output["nodeCapacity"] = node_capacity

            node_allocatable_resources= {}
            node_allocatable_resources["nodeCPUCap"] = pop['status']['allocatable']['cpu']
            memory = pop['status']['allocatable']['memory']
            memory_size = len(memory)
            node_allocatable_resources["nodeMemoryCap"] = memory[:memory_size - 2]
            node_allocatable_resources["nodeMemoryCapMU"] = memory[-2:]
            storage = pop['status']['allocatable']['ephemeral-storage']
            storage_size = len(storage)
            node_allocatable_resources["nodeStorageCap"] = storage[:storage_size - 2]
            node_allocatable_resources["nodeStorageCapMU"] = storage[-2:]
            # node_allocatable_resources["nodeMaxNoofPods"] = pop['status']['allocatable']['pods']
            pop_output["nodeAllocatableResources"] = node_allocatable_resources


            #calculate usage
            for stats in k8s_nodes['items']:
                if stats['metadata']['name']==nodeName:
                    node_usage={}
                    cpu=stats['usage']['cpu']
                    cpu_size=len(cpu)
                    memory=stats['usage']['memory']
                    memory_size = len(memory)

                    node_usage["nodeMemoryInUse"]=memory[:memory_size - 2]
                    node_usage["nodeMemoryInUseMU"]=memory[-2:]
                    node_usage["nodeMemoryUsage"]=int(node_usage["nodeMemoryInUse"])/int(node_capacity["nodeMemoryCap"])
                    node_usage["nodeCPUInUse"]=cpu[:cpu_size - 1]
                    node_usage["nodeCPUInUseMU"]=cpu[-1:]
                    node_usage["nodeCPUUsage"]=int(node_usage["nodeCPUInUse"])/(int(node_capacity["nodeCPUCap"])*1000)
                    pop_output["nodeUsage"] = node_usage


            node_general_info={}
            node_general_info["nodeOS"]=pop['status']['nodeInfo']['osImage']
            node_general_info["nodeKubernetesVersion"]=pop['status']['nodeInfo']['kernelVersion']
            node_general_info["nodecontainerRuntimeVersion"]=pop['status']['nodeInfo']['containerRuntimeVersion']
            node_general_info["nodeKernelVersion"]=pop['status']['nodeInfo']['kernelVersion']
            node_general_info["nodeArchitecture"]=pop['status']['nodeInfo']['architecture']
            pop_output["nodeGeneralInfo"] = node_general_info

    return pop_output


def get_PoPs():

    try:
        pops_ = []
        x1 = v1.list_node()
        for node in x1.items:
            pop_ = {}
            pop_['name'] = node.metadata.name
            pop_['uid'] = node.metadata.uid
            pop_['location'] = node.metadata.labels.get('location')
            pop_['serial'] = node.status.addresses[0].address
            pop_['node_type'] = node.metadata.labels.get('node_type')
            pop_['status'] = 'active' if node.status.conditions[-1].status=='True' else 'inactive'
            # pop_= NodesResponse(id=uid,name=name,location=location,serial=address, node_type=node_type, status=ready_status)
            pops_.append(pop_)
        return pops_
        # url = host + "/api/v1/nodes"
        # headers = {"Authorization": "Bearer " + token_k8s}
        # x=requests.get(url, headers=headers, verify=False)
        # x1 = x.json()
    except requests.exceptions.HTTPError as e:
        # logging.error(traceback.format_exc())
        return ("Exception when calling CoreV1Api->/api/v1/namespaces/sunrise6g/persistentvolumeclaims: %s\n" % e)


    # client.models.v1_node_list.V1NodeList
    # kubernetes.client.models.v1_node_list.V1NodeList
    # pops_= []
    # for pop in x1['items']:

    #     name=pop['metadata']['name']
    #     #pop_..(name)
    #     uid = pop['metadata']['uid']
    #     #pop_.id(uid)
    #     location = pop['metadata']['labels']['location']
    #     #pop_.location(location)
    #     address = pop['status']['addresses'][0]['address']
    #     #pop_.serial(address)
    #     node_type = pop['metadata']['labels']['node_type']
    #     ready_status = 'Ready' if pop['status']['conditions'][-1]['status']=='True' else 'Offline'
    #     pop_= NodesResponse(id=uid,name=name,location=location,serial=address, node_type=node_type, status=ready_status)

    #     pops_.append(pop_)
    # return pops_
#


def delete_service_function(service_function_name):

    deleted_app = api_instance_appsv1.delete_namespaced_deployment(name=service_function_name, namespace="sunrise6g")


    deleted_service = v1.delete_namespaced_service(name=service_function_name, namespace="sunrise6g")



    hpa_list = api_instance_v1autoscale.list_namespaced_horizontal_pod_autoscaler("sunrise6g")

    #hpas=hpa_list["items"]

    for hpa in hpa_list.items:
        if hpa.metadata.name==service_function_name:
            deleted_hpa = api_instance_v1autoscale.delete_namespaced_horizontal_pod_autoscaler(name=service_function_name, namespace="sunrise6g")
            break
    #deletevolume
    volume_list = v1.list_namespaced_persistent_volume_claim("sunrise6g")
    for volume in volume_list.items:
        name_v=service_function_name+str("-")
        if name_v in volume.metadata.name:
            deleted_pv = v1.delete_persistent_volume(
                name=volume.spec.volume_name)

            deleted_pvc = v1.delete_namespaced_persistent_volume_claim(
                name=volume.metadata.name, namespace="sunrise6g")

    doc = {}
    doc["instance_name"] = service_function_name
    sf = connector_db.delete_document_deployed_service_functions(document=doc)


def delete_chain(chain_name):

    apps=get_deployed_service_functions()
    chain_found=False
    for app in apps:
        chain_app_names= app["appname"].split("-",1) #0 will be chain name
        if chain_app_names[0]==chain_name: #should delete the app
            try:
                delete_service_function(app["appname"])
                #chain_found = True
            except Exception as ce_:
                raise Exception("An exception occurred :", ce_)
    # if chain_found:
    #     return True
    # else:
    #     return False


def deploy_service_function(descriptor_service_function):
    #deploys a Deployment yaml file, a service, a pvc and a hpa
    # logging.info('DESCRIPTOR: '+descriptor_service_function)
    # logging.info(descriptor_service_function)
    if "volumes" in descriptor_service_function:
        for volume in descriptor_service_function["volumes"]:
            #first solution (python k8s client raises error without reason!)
            #body_volume = create_pvc(descriptor_service_function["name"], volume)
            #api_response_pvc = v1.create_namespaced_persistent_volume_claim("sunrise6g", body_volume)


            # #deploy pv
            # print("deploy pv")
            # try:
            #     url = host + "/api/v1/persistentvolumes"
            #     body_volume = create_pv_dict(descriptor_service_function["name"], volume)
            #
            #
            #     headers = {"Authorization": "Bearer " + token_k8s}
            #     x = requests.post(url, headers=headers, json=body_volume, verify=False)
            #     print (x.status_code)
            # except requests.exceptions.HTTPError as e:
            #     # logging.error(traceback.format_exc())
            #     return ("Exception when calling CoreV1Api->/api/v1/persistentvolumes: %s\n" % e)


            #deploy pvc

            if volume.get("hostpath") is None:
                try:
                    url = host+"/api/v1/namespaces/sunrise6g/persistentvolumeclaims"
                    body_volume = create_pvc_dict(descriptor_service_function["name"], volume)
                    headers = {"Authorization": "Bearer "+token_k8s}
                    requests.post(url, headers=headers, json=body_volume, verify=False)
                except requests.exceptions.HTTPError as e:
                    # logging.error(traceback.format_exc())
                    return ("Exception when calling CoreV1Api->/api/v1/namespaces/sunrise6g/persistentvolumeclaims: %s\n" % e)

            #api_response_pvc = api_instance_corev1api.create_namespaced_persistent_volume_claim
    body_deployment = create_deployment(descriptor_service_function)
    body_service = create_service(descriptor_service_function)



    try:
        api_response_deployment = api_instance_appsv1.create_namespaced_deployment("sunrise6g", body_deployment)
        #api_response_service = api_instance_apiregv1.create_api_service(body_service)
        api_response_service=v1.create_namespaced_service("sunrise6g",body_service)
        if "autoscaling_policies" in descriptor_service_function:
            #V1 AUTOSCALER
            body_hpa = create_hpa(descriptor_service_function)
            api_instance_v1autoscale.create_namespaced_horizontal_pod_autoscaler("sunrise6g",body_hpa)
            # V2beta1 AUTOSCALER
            #body_hpa = create_hpa(descriptor_paas)
            #api_instance_v2beta1autoscale.create_namespaced_horizontal_pod_autoscaler("sunrise6g",body_hpa)
        body_r = "Service " + descriptor_service_function["name"] + " deployed successfully"
        return body_r
    except ApiException as e:
        #logging.error(traceback.format_exc())
        return ("Exception when calling AppsV1Api->create_namespaced_deployment or ApiregistrationV1Api->create_api_service: %s\n" % e)
       # Exception("An exception occurred : ", e)


def patch_service_function(descriptor_paas):

    #deploys a Deployment yaml file and a service node port

    body_deployment = create_deployment(descriptor_paas)
    body_service=create_service(descriptor_paas)

    if "autoscaling_policies" in descriptor_paas:
        body_hpa = create_hpa(descriptor_paas)

    try:

        api_response_deployment = api_instance_appsv1.patch_namespaced_deployment(namespace="sunrise6g", name=descriptor_paas["name"], body=body_deployment)
        #api_response_service = api_instance_apiregv1.create_api_service(body_service)
        api_response_service=v1.patch_namespaced_service(namespace="sunrise6g", name=descriptor_paas["name"], body=body_service)
        if "autoscaling_policies" in descriptor_paas:
            api_response_hpa = api_instance_v1autoscale.patch_namespaced_horizontal_pod_autoscaler(namespace="sunrise6g", name=descriptor_paas["name"], body=body_hpa)

        body_r="PaaS service "+descriptor_paas["name"] +" updated successfuly"
        return body_r
    except ApiException as e:

        return ("Exception when calling AppsV1Api->create_namespaced_deployment or ApiregistrationV1Api->create_api_service: %s\n" % e)
       # Exception("An exception occurred : ", e)




def create_deployment(descriptor_service_function):


    metadata = client.V1ObjectMeta(name=descriptor_service_function["name"])
    # selector
    dict_label = {}
    dict_label['sunrise6g'] = descriptor_service_function["name"]
    selector = client.V1LabelSelector(match_labels=dict_label)

    # create spec

    # spec.selector=selector
    # replicas
    # spec.replicas=descriptor_paas("count-min")
    # template

    metadata_spec = client.V1ObjectMeta(labels=dict_label)

    # template spec
    containers = []
    for container in descriptor_service_function["containers"]:
        #privileged
        if "privileged" in container:
            security_context = client.V1SecurityContext(privileged=container["privileged"])
        else:
            security_context = None
        ports = []
        for port_id in container["application_ports"]:
            port_ = client.V1ContainerPort(container_port=port_id)
            ports.append(port_)

        #check env_parameters
        envs = []

        if "env_parameters" in descriptor_service_function:
            if descriptor_service_function["env_parameters"] is not None:

                for env in descriptor_service_function["env_parameters"]:
                    if "value" in env:
                        env_=client.V1EnvVar(name=env["name"], value=env["value"])
                    elif "value_ref" in env:
                        #env_name_ should based on paas_instance_name
                        if "paas_name" in descriptor_service_function:
                            #check if value is something like:  http://edgex-core-data:48080

                            env_split = env["value_ref"].split(":")

                            if "@" not in env["value_ref"]: #meaning  that it is reffering to a running paas!!!!!

                                if len(env_split) > 2: #case http://edgex-core-data:48080
                                    prefix=env_split[0] #http
                                    final_env = env_split[1] #//edgex-core-data or edgex-core-data
                                    split2=final_env.split("//")
                                    if len(split2)>=2:
                                        final_env=split2[1]
                                    port_env = env_split[2] #48080
                                    env_= auxiliary_functions.prepare_name_for_k8s(str(descriptor_service_function["paas_name"]+str("-")+final_env))

                                    env_name_=prefix + ":" + "//"+ env_ + ":" + port_env

                                elif len(env_split)>1: #case edgex-core-data:48080
                                    final_env = env_split[0]
                                    port_env=env_split[1]
                                    env_ = auxiliary_functions.prepare_name_for_k8s(str(descriptor_service_function["paas_name"] + str("-") + final_env))
                                    env_name_ = env_ + ":" + port_env
                                else: #case edgex-core-data
                                    final_env = env_split[0]
                                    env_name_= auxiliary_functions.prepare_name_for_k8s(str(descriptor_service_function["paas_name"]+str("-")+final_env))
                                env_ = client.V1EnvVar(name=env["name"], value=env_name_)

                    envs.append(env_)

        #create volumes
        volumes=[]
        volume_mounts=[]
        if "volumes" in descriptor_service_function:
            if descriptor_service_function["volumes"] is not None:

                for volume in descriptor_service_function["volumes"]:

                    if volume.get("hostpath") is None:

                        pvc=client.V1PersistentVolumeClaimVolumeSource(claim_name=str(descriptor_service_function["name"]+str("-")+volume["name"]))
                        #volume_=client.V1Volume(name=volume["name"], persistent_volume_claim=pvc)
                        volume_=client.V1Volume(name=str(descriptor_service_function["name"]+str("-")+volume["name"]), persistent_volume_claim=pvc)

                        volumes.append(volume_)

                    else:
                        hostpath=client.V1HostPathVolumeSource(path=volume["hostpath"])
                        volume_ = client.V1Volume(name=str(descriptor_service_function["name"] + str("-") + volume["name"]),host_path=hostpath)
                        volumes.append(volume_)

                    volume_mount = client.V1VolumeMount(
                        name=str(descriptor_service_function["name"] + str("-") + volume["name"]),
                        mount_path=volume["path"])
                    volume_mounts.append(volume_mount)

        if "autoscaling_policies" in descriptor_service_function:
            limits_dict = {}
            request_dict = {}
            for auto_scale_policy in descriptor_service_function["autoscaling_policies"]:
                limits_dict[auto_scale_policy["metric"]]=auto_scale_policy["limit"]
                request_dict[auto_scale_policy["metric"]]=auto_scale_policy["request"]


            resources= client.V1ResourceRequirements(limits=limits_dict, requests=request_dict)
            if not envs:
                con = client.V1Container(name=descriptor_service_function["name"], image=container["image"], ports=ports, image_pull_policy='Always',
                                     resources=resources, volume_mounts=volume_mounts if volume_mounts else None, security_context=security_context)
            else:
                con = client.V1Container(name=descriptor_service_function["name"], image=container["image"],
                                         ports=ports, image_pull_policy='Always',
                                         resources=resources, env=envs, volume_mounts=volume_mounts if volume_mounts else None, security_context=security_context )
        else:
            if not envs:
                con = client.V1Container(name=descriptor_service_function["name"], image=container["image"], ports=ports, image_pull_policy='Always',
                                         volume_mounts=volume_mounts if volume_mounts else None, security_context=security_context )
            else:
                con = client.V1Container(name=descriptor_service_function["name"], image=container["image"], image_pull_policy='Always',
                                         ports=ports, env=envs, volume_mounts=volume_mounts if volume_mounts else None, security_context=security_context)

        containers.append(con)


    node_selector_dict = {}
    if "location" in descriptor_service_function:
        node_selector_dict['location'] = descriptor_service_function["location"]

        template_spec_ = client.V1PodSpec(containers=containers, node_selector=node_selector_dict, hostname=descriptor_service_function["name"], restart_policy='Always',
                                      volumes=None if not volumes else volumes)
    else:
        template_spec_ = client.V1PodSpec(containers=containers,
                                          hostname=descriptor_service_function["name"], restart_policy='Always',
                                          volumes=None if not volumes else volumes)

    template = client.V1PodTemplateSpec(metadata=metadata_spec, spec=template_spec_)

    spec = client.V1DeploymentSpec(selector=selector, template=template, replicas=descriptor_service_function["count-min"])

    body = client.V1Deployment(api_version="apps/v1", kind="Deployment", metadata=metadata, spec=spec)
    return body


def create_service(descriptor_service_function):
    dict_label = {}
    dict_label['sunrise6g'] = descriptor_service_function["name"]
    metadata = client.V1ObjectMeta(name=descriptor_service_function["name"], labels=dict_label)

    #  spec


    if "exposed_ports" in descriptor_service_function["containers"][0]: #create NodePort svc object
        ports=[]
        hepler=0
        for port_id in descriptor_service_function["containers"][0]["exposed_ports"]:

            # if "grafana" in descriptor_service_function["name"]:
            #     ports_=client.V1ServicePort(port=port_id,
            #                                 node_port=31000,
            #                                 target_port=port_id, name=str(port_id))
            # else:
            #     ports_ = client.V1ServicePort(port=port_id,
            #                                   # node_port=descriptor_paas["containers"][0]["exposed_ports"][hepler],
            #                                   target_port=port_id, name=str(port_id))
            ports_ = client.V1ServicePort(port=port_id,
                                          target_port=port_id, name=str(port_id))
            ports.append(ports_)
            hepler=hepler+1
        spec=client.V1ServiceSpec(selector=dict_label, ports=ports, type="NodePort")
        #body = client.V1Service(api_version="v1", kind="Service", metadata=metadata, spec=spec)
    else: #create ClusterIP svc object
        ports = []
        for port_id in descriptor_service_function["containers"][0]["application_ports"]:
            ports_ = client.V1ServicePort(port=port_id,
                                          target_port=port_id, name=str(port_id))
            ports.append(ports_)
        spec = client.V1ServiceSpec(selector=dict_label, ports=ports, type="ClusterIP")
    body = client.V1Service(api_version="v1", kind="Service", metadata=metadata, spec=spec)

    return body


def create_pvc(name, volumes):
    dict_label = {}
    name_vol=name+str("-")+volumes["name"]
    dict_label['sunrise6g'] = name_vol
    #metadata = client.V1ObjectMeta(name=name_vol)
    metadata = client.V1ObjectMeta(name=name_vol, labels=dict_label)
    api_version = 'v1',
    kind = 'PersistentVolumeClaim',
    spec = client.V1PersistentVolumeClaimSpec(
        access_modes=[
            'ReadWriteMany'
        ],
        resources=client.V1ResourceRequirements(
            requests={
                'storage': volumes["storage"]
            }
        )
    )
    body=client.V1PersistentVolumeClaim(api_version="v1", kind=kind, metadata=metadata, spec=spec)

    return body


def create_pvc_dict(name, volumes, storage_class='microk8s-hostpath', volume_name=None):
    name_vol = name + str("-") + volumes["name"]
    # body={}
    # body["api_version"]="v1"
    # body["kind"]="PersistentVolumeClaim"
    # metadata={}
    # labels={}
    body={"api_version": "v1",
     "kind": "PersistentVolumeClaim",
     "metadata": {
         "labels": {"sunrise6g": name_vol},
         "name": name_vol},
     "spec": {
         "accessModes": ["ReadWriteOnce"],
         "resources": {"requests": {"storage": volumes["storage"]}},
         "storageClassName": storage_class
     }
     }

    if volume_name is not None:
        body["spec"]["volume_name"] = volume_name

    return body

def create_pv_dict(name, volumes, storage_class, node=None):
    name_vol = name + "-" + volumes["name"]

    body = {
        "apiVersion": "v1",
        "kind": "PersistentVolume",
        "metadata": {
            "name": name_vol,
            "labels": {
                "sunrise6g": name_vol,
            }
        },
        "spec": {
            "capacity": {
                "storage": volumes["storage"]
            },
            "volumeMode": "Filesystem",
            "accessModes": [
                "ReadWriteOnce"
            ],
            "persistentVolumeReclaimPolicy": "Delete",
            "storageClassName": storage_class,
            "hostPath": {
                "path": "/mnt/" + name_vol,
                "type": "DirectoryOrCreate"
            }
        }
    }

    if node is not None:
        body["spec"]["nodeAffinity"] = {
            "required": {
                "nodeSelectorTerms": [
                    {
                        "matchExpressions": [
                            {
                                "key": "kubernetes.io/hostname",
                                "operator": "In",
                                "values": [
                                    node
                                ]
                            }
                        ]
                    }
                ]
            }
        }

    return body

def check_for_update_hpas(deployed_hpas):

    for hpa in deployed_hpas:
        for catalogue_policy in hpa["catalogue_policy"]:
            if catalogue_policy["policy"]==hpa["deployed_scaling_type"]:
                for metrics in catalogue_policy["monitoring_metrics"]:

                    if metrics["metric_name"]== hpa["deployed_metric"]:

                        if metrics["catalogue_util"]!=hpa["deployed_util"]: #need to update hpa
                            desc_paas={}
                            desc_paas["name"]=hpa["name"]
                            desc_paas["count-max"]=hpa["max"]
                            desc_paas["count-min"]=hpa["min"]
                            policy={}
                            policy["limit"]=metrics["catalogue_limit"]
                            policy["request"]=metrics["catalogue_request"]
                            policy["util_percent"]=metrics["catalogue_util"]
                            policy["metric_name"]=metrics["metric_name"]
                            policies=[]
                            policies.append(policy)
                            desc_paas["autoscaling_policies"]=policies
                            body_hpa = create_hpa(desc_paas)
                            api_instance_v1autoscale.patch_namespaced_horizontal_pod_autoscaler(namespace="sunrise6g",
                                                                                                name=desc_paas["name"],
                                                                                                body=body_hpa)
                        break
                break


def create_hpa(descriptor_service_function):


    #V1!!!!!!!

    dict_label = {}
    dict_label['name'] = descriptor_service_function["name"]
    metadata = client.V1ObjectMeta(name=descriptor_service_function["name"], labels=dict_label)


    #  spec

    scale_target=client.V1CrossVersionObjectReference(api_version="apps/v1", kind="Deployment", name= descriptor_service_function["name"])

    #todo!!!! check 0 gt an exoume kai cpu k ram auto dn tha einai auto to version!
    spec=client.V1HorizontalPodAutoscalerSpec(max_replicas=descriptor_service_function["count-max"],
                                              min_replicas=descriptor_service_function["count-min"],
                                              target_cpu_utilization_percentage=int(descriptor_service_function["autoscaling_policies"][0]["util_percent"]),
                                              scale_target_ref=scale_target)
    body = client.V1HorizontalPodAutoscaler(api_version="autoscaling/v1", kind="HorizontalPodAutoscaler", metadata=metadata, spec=spec)


    #V2BETA1 K8S API IMPLEMENTATION!!!!

    # dict_label = {}
    # dict_label['name'] = descriptor_paas["name"]
    # metadata = client.V1ObjectMeta(name=descriptor_paas["name"], labels=dict_label)
    #
    # #  spec
    #
    # scale_target = client.V2beta1CrossVersionObjectReference(api_version="extensions/v1beta1", kind="Deployment",
    #                                                     name=descriptor_paas["name"])
    #
    # metrics=[]
    #
    # for metric in descriptor_paas["autoscaling_policies"]:

    #     resource_=client.V2beta1ResourceMetricSource(name=metric["metric"],target_average_utilization=int(metric["util_percent"]))
    #     metric_=client.V2beta1MetricSpec(type="Resource", resource=resource_)
    #     metrics.append(metric_)
    #
    #
    # spec = client.V2beta1HorizontalPodAutoscalerSpec(max_replicas=descriptor_paas["count-max"],
    #                                             min_replicas=descriptor_paas["count-min"],
    #                                             metrics=metrics,
    #                                             scale_target_ref=scale_target)
    # body = client.V2beta1HorizontalPodAutoscaler(api_version="autoscaling/v2beta1", kind="HorizontalPodAutoscaler",
    #                                         metadata=metadata, spec=spec)


    #V2BETA2 K8S API IMPLEMENTATION!!!!

    # dict_label = {}
    # dict_label['name'] = descriptor_paas["name"]
    # metadata = client.V1ObjectMeta(name=descriptor_paas["name"], labels=dict_label)
    #
    # #  spec
    #
    # scale_target = client.V2beta2CrossVersionObjectReference(api_version="apps/v1", kind="Deployment",
    #                                                          name=descriptor_paas["name"])
    #
    # metrics = []
    #
    # for metric in descriptor_paas["autoscaling_policies"]:
    #
    #     target=client.V2beta2MetricTarget(average_utilization=int(metric["util_percent"]),type="Utilization")
    #     resource_ = client.V2beta2ResourceMetricSource(name=metric["metric"],
    #                                                   target=target)
    #     metric_ = client.V2beta2MetricSpec(type="Resource", resource=resource_)
    #     metrics.append(metric_)
    #
    # spec = client.V2beta2HorizontalPodAutoscalerSpec(max_replicas=descriptor_paas["count-max"],
    #                                                  min_replicas=descriptor_paas["count-min"],
    #                                                  metrics=metrics,
    #                                                  scale_target_ref=scale_target)
    # body = client.V2beta2HorizontalPodAutoscaler(api_version="autoscaling/v2beta2", kind="HorizontalPodAutoscaler",
    #                                              metadata=metadata, spec=spec)

    return body

def get_deployed_dataspace_connector(instance_name):
    label_selector = {}
    api_response = api_instance_appsv1.list_namespaced_deployment("sunrise6g")

    api_response_service = v1.list_namespaced_service("sunrise6g")
    app_ = {}
    for app in api_response.items:
        metadata = app.metadata
        spec = app.spec
        status = app.status

        dataspace_name=instance_name+"-dataspace-connector"

        if dataspace_name==metadata.name:

            app_["dataspace_connector_name"] = metadata.name

        if app_:  # if app_ is not empty

            if (status.available_replicas is not None) and (status.ready_replicas is not None):
                if status.available_replicas >= 1 and status.ready_replicas >= 1:
                    app_["status"] = "running"
                    app_["replicas"] = status.ready_replicas
                else:
                    app_["status"] = "not_running"
                    app_["replicas"] = 0
            else:
                app_["status"] = "not_running"
                app_["replicas"] = 0

            for app_service in api_response_service.items:

                metadata_svc = app_service.metadata

                spec_svc = app_service.spec
                svc_ports = []
                if metadata_svc.name == app_["dataspace_connector_name"]:
                    app_["internal_ip"]=spec_svc.cluster_ip
                    for port in spec_svc.ports:
                        port_ = {}
                        if port.node_port is not None:

                            port_["exposed_port"] = port.node_port
                            port_["protocol"] = port.protocol
                            port_["application_port"] = port.port
                            svc_ports.append(port_)
                        else:
                            port_["protocol"] = port.protocol
                            port_["application_port"] = port.port
                            svc_ports.append(port_)
                    app_["ports"] = svc_ports
                    break
            return app_
    return app_


def get_deployed_service_functions():
    label_selector={}
    deployed_hpas=get_deployed_hpas()
    #

    #SHOULD UNCOMMENT IT IF WE WOULD LIKE LIVE UPDATE OF A RUNNING PAAS SERVICE
    # if deployed_hpas:
    #     check_for_update_hpas(deployed_hpas)
    ##########
    api_response = api_instance_appsv1.list_namespaced_deployment("sunrise6g")

    api_response_service= v1.list_namespaced_service("sunrise6g")
    api_response_pvc= v1.list_namespaced_persistent_volume_claim("sunrise6g")


    #
    # hpa_list = api_instance_v1autoscale.list_namespaced_horizontal_pod_autoscaler("sunrise6g")
    # api_response_pod = v1.list_namespaced_pod("sunrise6g")
    #
    apps=[]
    for app in api_response.items:
        metadata=app.metadata
        spec=app.spec
        status=app.status
        app_={}
        apps_col = connector_db.get_documents_from_collection(collection_input="service_functions")
        deployed_apps_col = connector_db.get_documents_from_collection(collection_input="deployed_service_functions")
        actual_name=None
        for app_col in deployed_apps_col:
            if  metadata.name == app_col["instance_name"]:
                app_["service_function_instance_name"] =app_col["instance_name"]
                app_['uid'] = metadata.uid
                actual_name =app_col["name"]
                #app_["appid"] = app_col["_id"]
                if "monitoring_service_URL" in app_col:
                    app_["monitoring_service_URL"]=app_col["monitoring_service_URL"]
                if "paas_name" in app_col:
                    app_["paas_name"] = app_col["paas_name"]
                break
        for app_col in apps_col:
            if  actual_name == app_col["name"]:
                app_["service_function_catalogue_name"] =app_col["name"]
                #app_["appid"] = app_col["_id"]
                break

        #find volumes!
        for app_col in apps_col:
            if  app_col.get("required_volumes") is not None:
                volumes_=[]
                for volume in app_col["required_volumes"]:
                    for item in api_response_pvc.items:
                        name_v=str("-")+volume["name"]
                        if name_v in item.metadata.name and metadata.name in item.metadata.name:
                            volumes_.append(item.metadata.name)
                            app_["volumes"] =volumes_
                            break
                break
        if app_: #if app_ is not empty

            if (status.available_replicas is not None) and (status.ready_replicas is not None):
                if status.available_replicas>=1 and status.ready_replicas>=1:
                    app_["status"]="running"
                    app_["replicas"] = status.ready_replicas
                else:
                    app_["status"] = "not_running"
                    app_["replicas"] = 0
            else:
                app_["status"] = "not_running"
                app_["replicas"] = 0


            #we need to find the compute node
            if spec.template.spec.node_selector is not None:  # giati kati mporei na min exei node selector
                if "location" in spec.template.spec.node_selector.keys():
                    location=spec.template.spec.node_selector["location"]
                    nodes=connector_db.get_documents_from_collection(collection_input="points_of_presence")
                    for node in nodes:
                        if location==node["location"]:
                            app_["node_name"] = node["name"]
                            app_["node_id"] = node["_id"]
                            app_["location"]=node["location"]
                            break

            for app_service in api_response_service.items:
                metadata_svc=app_service.metadata
                spec_svc=app_service.spec
                svc_ports = []
                if metadata_svc.name == app_["service_function_instance_name"]:

                    for port in spec_svc.ports:
                        port_={}
                        if port.node_port is not None:

                            port_["exposed_port"]=port.node_port
                            port_["protocol"]=port.protocol
                            port_["application_port"]=port.port
                            svc_ports.append(port_)
                        else:
                            port_["protocol"] = port.protocol
                            port_["application_port"] = port.port
                            svc_ports.append(port_)
                    app_["ports"]=svc_ports
                    break


            apps.append(app_)

    return apps


def get_deployed_hpas():
    label_selector={}

    #APPV1 Implementation!
    api_response = api_instance_v1autoscale.list_namespaced_horizontal_pod_autoscaler("sunrise6g")

    hpas=[]
    for hpa in api_response.items:
        metadata=hpa.metadata
        spec=hpa.spec
        hpa_={}

        deployed_hpas_col = connector_db.get_documents_from_collection(collection_input="deployed_apps")
        apps_col = connector_db.get_documents_from_collection(collection_input="paas_services")

        actual_name=None
        for hpa_col in deployed_hpas_col:
            if  metadata.name == hpa_col["deployed_name"]:
                hpa_["name"] = metadata.name
                if "scaling_type" in hpa_col:
                    hpa_["deployed_scaling_type"] =hpa_col["scaling_type"]

                actual_name= hpa_col["name"]
                break
        for app_col in apps_col:
            if  actual_name == app_col["name"]:
                hpa_["paascataloguename"] =app_col["name"]
                hpa_["appid"] = app_col["_id"]
                if "autoscaling_policies" in app_col:
                    pol = []
                    for autoscaling_ in app_col["autoscaling_policies"]:


                        metric_=[]
                        for auto_metric in autoscaling_["monitoring_metrics"]:
                            hpa__={}
                            # if auto_metric["metric_name"]=="cpu": #TODO!! CHANGE IT FOR v1beta2 etc.....!!!!! (only cpu wokrs now)
                            hpa__["catalogue_util"] = auto_metric["util_percent"]
                            hpa__["metric_name"] =  auto_metric["metric_name"]
                            hpa__["catalogue_limit"] = auto_metric["limit"]
                            hpa__["catalogue_request"] = auto_metric["request"]
                            metric_.append(hpa__)
                            #pol["monitoring_metrics"]=  metric_

                        polic={}
                        polic["policy"]=autoscaling_["policy"]
                        polic["monitoring_metrics"] = metric_
                        pol.append(polic)


                    hpa_["catalogue_policy"]=pol
                break

        if hpa_: #if hpa_ is empty
            hpa_["min"]=spec.min_replicas
            hpa_["max"] = spec.max_replicas
            hpa_["deployed_util"] = spec.target_cpu_utilization_percentage
            hpa_["deployed_metric"] = "cpu"

            hpas.append(hpa_)

    return hpas


def operate_service_function_node_migration(service_function_to_migrate: ServiceFunctionNodeMigration):
    try:
        instance_name = service_function_to_migrate.service_function_instance_name
        api_response_current = api_instance_appsv1.read_namespaced_deployment(instance_name, 'sunrise6g')

        source_location = api_response_current.spec.template.spec.node_selector['location']
        destination_location = service_function_to_migrate.destination_location

        if source_location == destination_location:
            return f"Destination location is the same with the current location. Service function remains to {destination_location} node"

        volumes = api_response_current.spec.template.spec.volumes

        nodes = connector_db.get_documents_from_collection(collection_input="points_of_presence")

        #finding the name of the node which is labelled with the destination_location
        for node in nodes:
            if node['location'] == destination_location:
                destination_node = node['name']
            if node['location'] == source_location:
                source_node = node['name']

        #Creating a new PVC which will be immediately bound; will be used to transfer data before transferring the actual service function
        if volumes is not None:

            #scale down deployment; should stop writing in the volume until migration
            replicas_before_scale_down = api_response_current.spec.replicas
            api_response_current.spec.replicas = 0
            api_response_scaled_down = api_instance_appsv1.patch_namespaced_deployment(instance_name, namespace='sunrise6g', body=api_response_current)

            for volume in volumes:
                pvc_name = volume.persistent_volume_claim.claim_name
                #find the volume_name
                volume_name = pvc_name.replace(f"{instance_name}-", "")

                if source_node in volume_name:
                    volume_name = volume_name.replace(f"{source_node}-", "")


                new_pvc_name = f'{instance_name}-{destination_node}-pvc'
                new_pv_name = f'{instance_name}-{destination_node}-pv'

                pvc_body = v1.read_namespaced_persistent_volume_claim(pvc_name, 'sunrise6g')

                pv_name = pvc_body.spec.volume_name

                storage_size = pvc_body.spec.resources.requests['storage']

                volumes = {"name": volume_name, "storage": storage_size}

                new_pv = create_pv_dict(name=new_pv_name, volumes=volumes, storage_class='immediate-storageclass', node=destination_node)
                new_pvc = create_pvc_dict(name=new_pvc_name, volumes=volumes, storage_class='immediate-storageclass', volume_name=new_pv_name)
                new_pvc_name_final = new_pvc["metadata"]["name"]

                pv_created = v1.create_persistent_volume(body=new_pv)
                pvc_created = v1.create_namespaced_persistent_volume_claim(body=new_pvc, namespace='sunrise6g')

                #create a k8s job that will perform the persistent volume migration
                job_body = create_pv_migration_job(pvc_name, new_pvc_name_final, source_location)

                job_created = api_instance_batchv1.create_namespaced_job(namespace='sunrise6g', body=job_body)

                job_name = job_body["metadata"]["name"]

                while True:
                    if is_job_completed(job_name):
                        print(f"Job  {job_name} completed successfully")

                        api_instance_batchv1.delete_namespaced_job(job_name, namespace='sunrise6g')
                        break
                    else:
                        print(f"Waiting for job {job_name} to be completed...")
                        time.sleep(5)

            #migrating deployment to destination node and scaling up to previous number of replicas
            api_response_scaled_down_read = api_instance_appsv1.read_namespaced_deployment(name=instance_name, namespace='sunrise6g')
            api_response_scaled_down_read.spec.template.spec.node_selector = {'location': service_function_to_migrate.destination_location}
            api_response_scaled_down_read.spec.template.spec.volumes[0].persistent_volume_claim.claim_name = new_pvc_name_final
            api_response_scaled_down_read.spec.replicas = replicas_before_scale_down

            print(f"Replicas before scale down were: {replicas_before_scale_down}")

            api_response_scaled_up = api_instance_appsv1.patch_namespaced_deployment(instance_name, namespace='sunrise6g',
                                                                                       body=api_response_scaled_down_read)


            api_response_pvc_removal = api_instance_corev1api.delete_namespaced_persistent_volume_claim(pvc_name, namespace='sunrise6g')

            api_response_pv_removal = api_instance_corev1api.delete_persistent_volume(pv_name)
        else:

            api_response_current.spec.template.spec.node_selector = {'location': service_function_to_migrate.destination_location}
            api_response_new = api_instance_appsv1.patch_namespaced_deployment(name=service_function_to_migrate.service_function_instance_name, namespace='sunrise6g',
                                                                              body=api_response_current)

        body_r = f"Service function {service_function_to_migrate.service_function_instance_name} successfully migrated from {source_location} to {destination_location}!"

        return body_r

    except ApiException as e:
        if e.status == 404:
            print(f"Deployment {service_function_to_migrate.service_function_instance_name} does not exist.")
        else:
            print(f"An error occured {e}.")


def create_pv_migration_job(source_pvc, destination_pvc, source_location):
    job_manifest = {
        "apiVersion": "batch/v1",
        "kind": "Job",
        "metadata": {
            "name": "pv-migrate-job",
        },
        "spec": {
            "template": {
                "metadata": {
                    "labels": {
                        "sidecar.istio.io/inject": "false"
                    }
                },
                "spec": {
                    "containers": [
                        {
                            "name": "pv-migrate",
                            "image": "utkuozdemir/pv-migrate:v1.7.1",
                            "args": [
                                "pv-migrate", "migrate", f"{source_pvc}", f"{destination_pvc}",
                                "-k", "/root/.kube/config",
                                "-n", "sunrise6g",
                                "-N", "sunrise6g",
                                "-i", "-s", "svc,lbsvc", "-b"
                            ],
                            "volumeMounts": [
                                {
                                    "name": "kube-config",
                                    "mountPath": "/root/.kube"
                                }
                            ]
                        }
                    ],
                    "restartPolicy": "Never",
                    "volumes": [
                        {
                            "name": "kube-config",
                            "hostPath": {
                                "path": f"/home/gzorro/.kube"
                            }
                        }
                    ],
                    "nodeSelector": {
                        "location": f"{get_master_node_location()}"  # Replace 'key' and 'value' with appropriate labels for your nodes
                    }
                }
            },
            "backoffLimit": 4
        }
    }

    return job_manifest

def is_job_completed(job_name):
    job = api_instance_batchv1.read_namespaced_job(name=job_name, namespace="sunrise6g")
    if job.status.succeeded is not None and job.status.succeeded > 0:
        return True
    return False

#Create storageClass resource for a node - useless for now
def create_immediate_storageclass(node=None):
    api_version = 'storage.k8s.io/v1'
    kind = 'StorageClass'
    name = 'immediate-storageclass'
    provisioner = 'microk8s.io/hostpath'
    reclaim_policy = 'Delete'
    volume_binding_mode = 'Immediate'

    metadata = client.V1ObjectMeta(name=name)

    # match_label_expressions = client.V1TopologySelectorLabelRequirement(key='kubernetes.io/hostname', values=[node.name])
    #
    # topology_selector_term = client.V1TopologySelectorTerm([match_label_expressions])

    # storage_class = client.V1StorageClass(api_version=api_version, kind=kind, metadata=metadata, provisioner=provisioner
    #                                       , volume_binding_mode=volume_binding_mode, reclaim_policy=reclaim_policy
    #                                       , allowed_topologies=[topology_selector_term])

    storage_class = client.V1StorageClass(api_version=api_version, kind=kind, metadata=metadata, provisioner=provisioner
                                          , volume_binding_mode=volume_binding_mode, reclaim_policy=reclaim_policy)

    try:
        api_response = api_instance_storagev1api.create_storage_class(body=storage_class)
    except ApiException as e:
        print("Exception when calling StorageV1Api->create_storage_class: %s\n" % e)


def get_master_node_location():
    nodes = connector_db.get_documents_from_collection(collection_input="points_of_presence")

    # finding the name of the node which is labelled with the destination_location
    for node in nodes:
        if node['serial'] == master_node_ip:
            return node['location']

    return "There is no master node in this cluster"

def immediate_storage_class_exists():
    try:
        storage_classes = api_instance_storagev1api.list_storage_class().items()

        for sc in storage_classes:
            if sc.metadata.name == "immediate-storageclass":
                return True

        return False

    except ApiException as e:
        return (f"Exception when calling StorageV1Api->list_storage_class: {e}")