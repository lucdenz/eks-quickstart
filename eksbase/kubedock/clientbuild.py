import yaml
import os
import docker
import datetime

path = os.path.dirname(os.path.abspath(__file__))

# create a kubeconfig file for your cluster
def createKubeconfigFile(cluster):
    server = cluster["endpoint"]
    certData = cluster["certificateAuthority"]["data"]
    clusterName = cluster["name"]

    fileName = "{}/kubeconfig".format(path)

    template = {
        "apiVersion": "v1",
        "clusters": [
            {
                "cluster": {
                    "server": server,
                    "certificate-authority-data": certData
                },
                "name": "kubernetes"
            }
        ],
        "contexts": [
            {
                "context": {
                    "cluster": "kubernetes",
                    "user": "aws"
                },
                "name": "aws"
            }
        ],
        "current-context": "aws",
        "kind": "Config",
        "preferences": {},
        "users": [
            {
                "name": "aws",
                "user": {
                    "exec": {
                        "apiVersion": "client.authentication.k8s.io/v1alpha1",
                        "command": "heptio-authenticator-aws",
                        "args": [
                            "token",
                            "-i",
                            clusterName
                        ]
                    }
                }
            }
        ]
    }

    with open(fileName, "w") as outfile:
        yaml.dump(template, outfile, default_flow_style=False)

def createWorkerAuthConfig(nodeInstanceRole):
    fileName = "{}/aws-auth-cm.yaml".format(path)

    stringLiteral = """apiVersion: v1
kind: ConfigMap
metadata:
  name: aws-auth
  namespace: kube-system
data:
  mapRoles: |
    - rolearn: """ + nodeInstanceRole + """
      username: system:node:{{EC2PrivateDNSName}}
      groups:
        - system:bootstrappers
        - system:nodes"""

    with open(fileName, "w") as outfile:
        print(stringLiteral, file=outfile)


def buildDockerImage(cluster, nodeInstanceRole):
    createKubeconfigFile(cluster)
    createWorkerAuthConfig(nodeInstanceRole)

    client = docker.from_env()
    client.images.build(path=path, rm=True, tag="eksbase/kubectl")

    print("INFO: Run your client container with:")
    print("INFO: docker run -it --rm --env-file ~/.aws/awscreds.sh eksbase/kubectl /bin/ash")
