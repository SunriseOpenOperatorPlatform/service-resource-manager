import paramiko
import logging
from swagger_server.models.helm_install_model import HelmInstall
from os import environ
import connexion

master_node_password=environ["KUBERNETES_MASTER_PASSWORD"].strip()
master_node_hostname=environ["KUBERNETES_MASTER_HOSTNAME"].strip()
master_node_ip=environ["KUBERNETES_MASTER_IP"].strip()
master_node_port=environ["KUBERNETES_MASTER_PORT"].strip()

def install_helm_chart(helm=None):
    logging.info('Installing helm chart')
    if connexion.request.is_json:
        try:
            # logging.info(connexion.request.get_json())
            helm =connexion.request.get_json()
            ssh=paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(master_node_ip,22, username='dlaskaratos', password=master_node_password)
            creds_string=''
            if helm.get('repo_password') is not None and helm.get('repo_username') is not None:
                creds_string=' --username '+helm['repo_username']+' --password '+helm['repo_password']
            stdin, stdout, stderr= ssh.exec_command('echo | sudo helm install '+helm['deployment_name']+' '+helm['uri']+creds_string)
            stdout.channel.set_combine_stderr(True)
            lines=stdout.readlines()
            return lines
        except Exception as e:
            logging.error(e)
            return e.__cause__
    else:
        return 'Error installing helm chart'

def uninstall_helm_chart(name: str):
    logging.info('Uninstalling helm chart')
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(master_node_ip,22, master_node_hostname,master_node_password)
    stdin, stdout, stderr= ssh.exec_command('echo | sudo helm uninstall '+name)
    stdout.channel.set_combine_stderr(True)
    lines=stdout.readlines()
    return lines
