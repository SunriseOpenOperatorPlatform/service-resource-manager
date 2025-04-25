# from __future__ import print_function
# import os
# import time
# import copy
# import requests
# import logging
# from threading import Thread


# from requests.structures import CaseInsensitiveDict
# # import traceback
# # import logging
# #scaling_type="minimize_cost"

# #K8S AUTH
# import json
# #import pandas as pd
# from urllib.request import urlopen



# #host="http://grafana.monitoring:3000"
# node_ip=os.environ["MONITORING_IP"].strip()
# node_port=os.environ["MONITORING_NODE_PORT"].strip()

# node_ip_proxy=os.environ["MONITORING_IP_PROXY"].strip()
# node_port_proxy=os.environ["MONITORING_PORT_PROXY"].strip()

# driver = os.environ["DRIVER"].strip()

# host="http://"+node_ip+":"+node_port
# #node_ip="203.0.113.172"
# #node_port="3000"

# if node_ip!=node_ip_proxy:
#     node_for_responce=node_ip_proxy
#     port_for_responce=node_port_proxy
# else:
#     node_for_responce = node_ip
#     port_for_responce = node_port



# username = "admin"
# password = os.environ["MONITORING_SERVICE_PASSWORD"].strip()
# #!!!!!!!!!!!!!!!!
# # Configure API key authorization: BearerToken
# #configuration.api_key['authorization'] = token_k8s
# #!!!!!!!!!!!!!!!!


# # Uncomment below to setup prefix (e.g. Bearer) for API key, if needed

# def get_monitoring_ip():
#     return node_ip

# def get_monitoring_port():
#     return node_port

# #works for grafana/grafana:8.1.3
# def create_monitoring_for_all_infra(nodes):
#     #public url for retrieving infra url

#     if driver == "docker":
#         f=open(os.path.join(os.path.split(os.path.dirname(__file__))[0], 'monitoring_files/infra_metric_with_throughput_beautified_docker.json'))
#     else:
#         f = open(os.path.join(os.path.split(os.path.dirname(__file__))[0], 'monitoring_files/infra_metric_with_throughput.json'))

#     data = json.load(f)

#     # url = "https://raw.githubusercontent.com/tandem-project/TANDEM-project/Master/TANDEM%20Edge/Edge%20Monitoring/grafana_templates/infra_metrics_plus_throughput.json"
#      ### #url = "https://github.com/tandem-project/TANDEM-project/blob/Master/TANDEM%20Edge/Edge%20Monitoring/grafana_templates/Infrastructure%20Metrics.json"
#     #r = requests.get(url)
#     grafana_dashboard = data
#     #print(grafana_dashboard)
#     init_panels = grafana_dashboard["dashboard"]["panels"].copy()
#     grafana_dashboard["dashboard"]["panels"]=[].copy()
#     #check number of nodes
#     new_panels = []
#     # if len(nodes)==1:
#     #     for panel in init_panels:
#     #         panel_={}
#     #         expr=panel["targets"][0]["expr"]
#     #         panel_=panel
#     #
#     #         panel_["targets"][0]["expr"] = expr.replace("NODE_NAME", nodes[0]["name"])
#     #
#     #         panel_["targets"][0]["legendFormat"] = panel["targets"][0]["legendFormat"].replace("NODE_NUMBER", "1")
#     #         panel_["title"] = panel["title"].replace("NODE_NUMBER", "1")
#     #         new_panels.append(panel_)
#     # else:

#     node_number = 0

#     for node in nodes:

#         # node_number = node_number + 1
#         panel_number=0
#         for panel in init_panels:

#             panel_number=panel_number+1
#             expr = panel["targets"][0]["expr"]
#             panel_ = copy.deepcopy(panel)

#             if driver == "docker":
#                 panel_["targets"][0]["expr"] = expr.replace("NODE_NAME", node["serial"]+":9323")
#                 panel_["targets"][0]["legendFormat"] = panel["targets"][0]["legendFormat"].replace("NODE_NUMBER", node['name'])
#                 panel_["title"] = panel["title"].replace("NODE_NUMBER", node['name'])
#             else:
#                 panel_["targets"][0]["expr"] = expr.replace("NODE_NAME", node["name"])
#                 panel_["targets"][0]["legendFormat"] = panel["targets"][0]["legendFormat"].replace("NODE_NUMBER", str(node_number))
#                 panel_["title"] = panel["title"].replace("NODE_NUMBER", str(node_number))

#             panel_["id"] = str(node_number) +""+ str(panel_number)
#             new_panels.append(panel_)


#     grafana_dashboard["dashboard"]["panels"]=new_panels

#     #send request to grafana!
#     try:

#         url = host + "/api/dashboards/import"
#         #body_ = grafana_dashboard
#         body_ = grafana_dashboard.copy()
        
#         #headers = {"Authorization": "Bearer " + token_k8s}

#         x = requests.post(host + "/api/dashboards/import", json=body_, verify=False, auth=(username, password))
#         if x.status_code == 200 or x.status_code == 201:
#             json_response=x.json()
#             # final_mon_url="http://" + node_ip_proxy + ":" + node_port_proxy + json_response["importedUrl"]
#             final_mon_url = f"{host}{json_response['importedUrl']}"
#         else:
#             final_mon_url = "An Error occured, Please try again"

#         return final_mon_url
#     except requests.exceptions.HTTPError as e:
#         # logging.error(traceback.format_exc())
#         return ("Exception when calling /api/dashboards/import %s\n" % e)





# #works for grafana/grafana:8.1.3
# def create_monitoring_infra_per_node(node,node_number):
#     #public url for retrieving infra url
#     if driver == "docker":
#         f = open(os.path.join(os.path.split(os.path.dirname(__file__))[0],
#                               'monitoring_files/infra_metric_with_throughput_beautified_docker.json'))
#     else:
#         f = open(os.path.join(os.path.split(os.path.dirname(__file__))[0],
#                               'monitoring_files/infra_metric_with_throughput.json'))
#     data = json.load(f)
#     #url = "https://raw.githubusercontent.com/tandem-project/TANDEM-project/Master/TANDEM%20Edge/Edge%20Monitoring/grafana_templates/infra_metrics_plus_throughput.json"
#     ###url = "https://github.com/tandem-project/TANDEM-project/blob/Master/TANDEM%20Edge/Edge%20Monitoring/grafana_templates/Infrastructure%20Metrics.json"
#     #r = requests.get(url)
#     grafana_dashboard = data
#     init_panels = grafana_dashboard["dashboard"]["panels"].copy()
#     grafana_dashboard["dashboard"]["panels"]=[].copy()
#     #check number of nodes
#     new_panels = []
#     for panel in init_panels:
#         #panel_={}
#         expr=panel["targets"][0]["expr"]
#         #panel_=panel
#         panel_ = copy.deepcopy(panel)

#         if driver == "docker":
#             panel_["targets"][0]["expr"] = expr.replace("NODE_NAME", node["serial"]+":9323")
#             panel_["targets"][0]["legendFormat"] = panel["targets"][0]["legendFormat"].replace("NODE_NUMBER", node['name'])
#             panel_["title"] = panel["title"].replace("NODE_NUMBER", node['name'])
#         else:
#             panel_["targets"][0]["expr"] = expr.replace("NODE_NAME", node["name"])
#             panel_["targets"][0]["legendFormat"] = panel["targets"][0]["legendFormat"].replace("NODE_NUMBER", str(node_number))
#             panel_["title"] = panel["title"].replace("NODE_NUMBER", str(node_number))
#         new_panels.append(panel_)

#     grafana_dashboard["dashboard"]["panels"]=new_panels

#     old_title=grafana_dashboard["dashboard"]["title"]
#     grafana_dashboard["dashboard"]["title"]= old_title + " Node " + str(node_number)
#     old_uid=grafana_dashboard["dashboard"]["uid"]
#     grafana_dashboard["dashboard"]["uid"] = old_uid + "-node-" + str(node_number)


#     #send request to grafana!
#     try:
#         url = host + "/api/dashboards/import"
#         #body_ = grafana_dashboard
#         #body_ = grafana_dashboard

#         body_=grafana_dashboard
#         #headers = {"Authorization": "Bearer " + token_k8s}
#         x = requests.post(url, json=body_, verify=False, auth=(username, password))

#         if x.status_code==200 or x.status_code==201:
#             json_response=x.json()
#             # final_mon_url="http://"+node_ip_proxy+":"+node_port_proxy+json_response["importedUrl"]
#             final_mon_url=f"{host}{json_response['importedUrl']}"
#         else:
#             final_mon_url = "An Error occured, Please try again"

#         return final_mon_url
#     except requests.exceptions.HTTPError as e:
#         # logging.error(traceback.format_exc())
#         return ("Exception when calling /api/dashboards/import %s\n" % e)



# def create_monitoring_for_all_service_functions(service_functions, node_name):
#     #public url for retrieving infra url

#     f = open(os.path.join(os.path.split(os.path.dirname(__file__))[0], 'monitoring_files/service_function_metrics_with_throughput.json'))
#     data = json.load(f)

#     #url = "https://raw.githubusercontent.com/tandem-project/TANDEM-project/Master/TANDEM%20Edge/Edge%20Monitoring/grafana_templates/basic_service_function_monitoring.json"
#     #url = "https://github.com/tandem-project/TANDEM-project/blob/Master/TANDEM%20Edge/Edge%20Monitoring/grafana_templates/Infrastructure%20Metrics.json"
#     #r = requests.get(url)
#     grafana_dashboard = data
#     init_panels = grafana_dashboard["dashboard"]["panels"].copy()
#     grafana_dashboard["dashboard"]["panels"]=[].copy()
#     #check number of nodes
#     new_panels = []
#     # if len(nodes)==1:
#     #     for panel in init_panels:
#     #         panel_={}
#     #         expr=panel["targets"][0]["expr"]
#     #         panel_=panel
#     #
#     #         panel_["targets"][0]["expr"] = expr.replace("NODE_NAME", nodes[0]["name"])
#     #
#     #         panel_["targets"][0]["legendFormat"] = panel["targets"][0]["legendFormat"].replace("NODE_NUMBER", "1")
#     #         panel_["title"] = panel["title"].replace("NODE_NUMBER", "1")
#     #         new_panels.append(panel_)
#     # else:



#     sf_number=0
#     for sf in service_functions:
#         for panel in init_panels:
#             if node_name==sf.get('node_name'):
#                 sf_number=sf_number+1
#                 expr = panel["targets"][0]["expr"]
#                 panel_ = copy.deepcopy(panel) #VERY IMPORTAND!!!!!!!!!!!!!!
#                 #panel_["id"]=sf_number
#                 panel_["targets"][0]["expr"] = expr.replace("SERVICE_FUNCTION_INSTANCE_NAME", sf["service_function_instance_name"])
#                 panel_["title"] = panel["title"].replace("SERVICE_FUNCTION_INSTANCE_NAME", sf["service_function_instance_name"])
#                 panel_["id"] = panel_["title"]
#                 new_panels.append(panel_)
#                 #panel_.clear()

#     grafana_dashboard["dashboard"]["panels"]=new_panels.copy()

#     #grafana_dashboard["dashboard"]["title"]="Node: "+node_name+ " "+ grafana_dashboard["dashboard"]["title"]
#     grafana_dashboard["dashboard"]["title"]=grafana_dashboard["dashboard"]["title"] +" node: "+node_name
#     grafana_dashboard["dashboard"]["uid"]=grafana_dashboard["dashboard"]["uid"]+"-"+node_name
#     #send request to grafana!


#     try:

#         url = host + "/api/dashboards/import"
#         body_ = grafana_dashboard

#         #headers = {"Authorization": "Bearer " + token_k8s}

#         logging.info("reeady to send post request for monitoring")

#         x = requests.post(url, json=body_, verify=False, auth=(username, password))


#         #x = requests.post(url, json=body_, verify=False, auth=(username, password))
#         if x.status_code==200 or x.status_code==201:
#             json_response=x.json()

#             # final_mon_url="http://"+node_ip_proxy+":"+node_port_proxy+json_response["importedUrl"]
#             final_mon_url = f"{host}{json_response['importedUrl']}"
#         else:
#             final_mon_url="An Error occured, Please try again"

#         return final_mon_url
#     except requests.exceptions.HTTPError as e:
#         # logging.error(traceback.format_exc())
#         return ("Exception when calling /api/dashboards/import %s\n" % e)


# def create_monitoring_for_service_function(service_function):
#     f = open(os.path.join(os.path.split(os.path.dirname(__file__))[0],
#                           'monitoring_files/service_function_metrics_with_throughput.json'))
#     data = json.load(f)
#     grafana_dashboard = data
#     init_panels = grafana_dashboard["dashboard"]["panels"].copy()
#     grafana_dashboard["dashboard"]["panels"] = [].copy()
#     new_panels = []

#     deployed_name = service_function.service_function_instance_name

#     for panel in init_panels:
#         expr = panel["targets"][0]["expr"]
#         panel_ = copy.deepcopy(panel)

#         panel_["targets"][0]["expr"] = expr.replace("SERVICE_FUNCTION_INSTANCE_NAME", deployed_name)

#         panel_["title"] = panel["title"].replace("SERVICE_FUNCTION_INSTANCE_NAME", deployed_name)
#         panel_["id"] = panel_["title"]

#         new_panels.append(panel_)

#     grafana_dashboard["dashboard"]["panels"] = new_panels.copy()
#     grafana_dashboard["dashboard"]["title"] = "Service Function: " + deployed_name
#     grafana_dashboard["dashboard"]["uid"] = "sf" + "-" + deployed_name

#     print(f"UID: {grafana_dashboard['dashboard']['uid']}")

#     # send request to grafana!
#     try:
#         url = host + "/api/dashboards/import"
#         body_ = grafana_dashboard
#         # headers = {"Authorization": "Bearer " + token_k8s}

#         logging.info("reeady to send post request \ monitoring")
#         x = requests.post(url, json=body_, verify=False, auth=(username, password))
#         if x.status_code == 200 or x.status_code == 201:
#             json_response = x.json()
#             # final_mon_url = "http://" + node_dip_proxy + ":" + node_port_proxy + json_response["importedUrl"]
#             final_mon_url = f"{host}{json_response['importedUrl']}"
#         else:
#             final_mon_url = "An Error occured, Please try again"

#         return final_mon_url

#     except requests.exceptions.HTTPError as e:
#         # logging.error(traceback.format_exc())
#         return ("Exception when calling /api/dashboards/import %s\n" % e)


# def create_monitoring_for_paas(service_functions, paas_name):

#     f = open(os.path.join(os.path.split(os.path.dirname(__file__))[0], 'monitoring_files/service_function_metrics_with_throughput.json'))
#     data = json.load(f)
#     grafana_dashboard=data
#     init_panels = grafana_dashboard["dashboard"]["panels"].copy()
#     grafana_dashboard["dashboard"]["panels"]=[].copy()
#     new_panels = []
#     sf_number=0
#     for sf in service_functions:

#         name_container=paas_name+"-"+sf["name"].replace('_', '')
#         for panel in init_panels:
#             sf_number=sf_number+1
#             expr = panel["targets"][0]["expr"]
#             panel_ = copy.deepcopy(panel)
#             #panel_["id"]=sf_number

#             panel_["targets"][0]["expr"] = expr.replace("SERVICE_FUNCTION_INSTANCE_NAME", name_container)

#             panel_["title"] = panel["title"].replace("SERVICE_FUNCTION_INSTANCE_NAME", name_container)
#             panel_["id"] = panel_["title"]


#             new_panels.append(panel_)
#             #panel_.clear()

#     grafana_dashboard["dashboard"]["panels"]=new_panels.copy()
#     grafana_dashboard["dashboard"]["title"]="PaaS: "+paas_name

#     #grafana_dashboard["dashboard"]["title"]="PaaS: "+paas_name+ " "+ grafana_dashboard["dashboard"]["title"]
#     grafana_dashboard["dashboard"]["uid"]="paas"+"-"+paas_name

#     #send request to grafana!
#     try:
#         url = host + "/api/dashboards/import"
#         body_ = grafana_dashboard
#         #headers = {"Authorization": "Bearer " + token_k8s}

#         logging.info("reeady to send post request \ monitoring")
#         x = requests.post(url, json=body_, verify=False, auth=(username, password))
#         if x.status_code == 200 or x.status_code == 201:
#             json_response = x.json()
#             # final_mon_url = "http://" + node_ip_proxy + ":" + node_port_proxy + json_response["importedUrl"]
#             final_mon_url = f"{host}{json_response['importedUrl']}"
#         else:
#             final_mon_url = "An Error occured, Please try again"




#         return final_mon_url
#     except requests.exceptions.HTTPError as e:
#         # logging.error(traceback.format_exc())
#         return ("Exception when calling /api/dashboards/import %s\n" % e)


# def delete_monitoring_for_service_function(sf_name):
#     try:
#         print(f"UID TO DELETE: sf-{sf_name}")
#         url = host + f"/api/dashboards/uid/sf-{sf_name}"
#         x = requests.delete(url, verify=False, auth=(username, password))
#         json_response = x.json()

#         if x.status_code == 200:
#             return "Dashboard deleted"
#     except requests.exceptions.HTTPError as e:
#         # logging.error(traceback.format_exc())
#         return ("Exception when calling /api/dashboards/import %s\n" % e)

# def delete_monitoring_for_paas(paas_name):

#     try:

#         url = host + "/api/dashboards/uid/paas-"+paas_name
#         #headers = {"Authorization": "Bearer " + token_k8s}
#         x = requests.delete(url, verify=False, auth=(username, password))
#         json_response=x.json()

#         if x.status_code==200:
#             return "Dashboard deleted"
#     except requests.exceptions.HTTPError as e:
#         # logging.error(traceback.format_exc())
#         return ("Exception when calling /api/dashboards/import %s\n" % e)





