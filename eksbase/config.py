CLUSTER_NAME = "eksbase"
SERVICE_ROLE_NAME = "eks-service-role"

NETWORK_STACK_NAME = "eksbase-vpc"
NETWORK_STACK_TEMPLATE_URL = "https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-06-05/amazon-eks-vpc-sample.yaml"

CREATE_WORKER_NODES = False
WORKER_STACK_NAME = "eksbase-minions"

DEPLOY_KUBE_UI = False