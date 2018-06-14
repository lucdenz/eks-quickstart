from eksbase.config import *
from eksbase.cluster import *

def run():
    deleteEKSCluster(CLUSTER_NAME)
    deleteEKSClusterVPC(NETWORK_STACK_NAME)
    deleteEKSRole(SERVICE_ROLE_NAME)

    """
    serviceRoleARN = createEKSRole(SERVICE_ROLE_NAME)
    networkStackOutputs = createEKSClusterVPC(
        NETWORK_STACK_NAME, 
        NETWORK_STACK_TEMPLATE_URL
    )
    createEKSCluster(CLUSTER_NAME, serviceRoleARN, networkStackOutputs)
    """
