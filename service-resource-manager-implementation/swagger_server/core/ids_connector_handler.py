
from swagger_server.utils import connector_db, auxiliary_functions, kubernetes_connector, nodes_monitoring

def deploy_ids_connector(name):

    commmads=[]

    #first we need to add icom-repo for helm (dataspace connector)

    commmads.append("helm repo add git-icom https://nikospsar.github.io/charts/")
    #deploy the connector
    deploy_command="helm install "+  name+" git-icom/dataspace-connector -n pi-edge"
    commmads.append(deploy_command)
    kubernetes_connector.execute_with_ssh_and_cli(commmads)

    #Should inform MEC PLATFORM about the new service



def delete_ids_connector(name):
    commmads=[]
    commmads.append("helm delete "+  name+"  -n pi-edge")
    kubernetes_connector.execute_with_ssh_and_cli(commmads)



