import sys
import os
import yaml

# A basic exception handling function that allows known errors
def exceptionHandler(exception):
    errorCode = exception.response["Error"]["Code"]
    errorMessage = exception.response["Error"]["Message"]
    
    if errorCode == "NoSuchEntity":
        print("INFO: " + errorMessage)
    elif errorCode == "ResourceNotFoundException":
        print("INFO: " + errorMessage)
    else:
        print("ERROR: An " + errorCode + " exception occurred")
        print("ERROR: " + errorMessage)
        sys.exit()

# create a kubeconfig file for your cluster
def createKubeconfigFile(endpointUrl, certData, clusterName):
    fileName = "kubeconfig"

    data = {
        "apiVersion": "v1",
        "clusters": [
            {
                "cluster": {
                    "server": endpointUrl,
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
        yaml.dump(data, outfile, default_flow_style=False)
    
    """
    userHome = os.environ["HOME"]
    kubeDir = "{}/.kube/".format(userHome)
    fileName = "{}config-{}".format(kubeDir, clusterName)
    os.makedirs(kubeDir, exist_ok=True)
    """

