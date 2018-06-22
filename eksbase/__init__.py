from eksbase.config import *
from eksbase.aws.cluster import *
from eksbase.kubedock.clientbuild import *

def run():
    deleteCluster(CLUSTER_NAME)
    deleteVPC(NETWORK_STACK_NAME)
    deleteServiceRole(SERVICE_ROLE_NAME)

    """
    serviceRole = createServiceRole(SERVICE_ROLE_NAME)
    networkStackOutputs = createVPC(
        NETWORK_STACK_NAME, 
        NETWORK_STACK_TEMPLATE_URL
    )
    createCluster(CLUSTER_NAME, serviceRole.arn, networkStackOutputs)

    cluster = describeCluster(CLUSTER_NAME)
    buildDockerImage(cluster)
    """
