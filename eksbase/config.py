CLUSTER_NAME = "eksbase"
SERVICE_ROLE_NAME = "eks-service-role"

NETWORK_STACK_NAME = "eksbase-vpc"
NETWORK_STACK_TEMPLATE_URL = "https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-06-05/amazon-eks-vpc-sample.yaml"

WORKER_STACK_NAME = "eksbase-worker-nodes"
NETWORK_STACK_TEMPLATE_URL = "https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-06-05/amazon-eks-nodegroup.yaml"
WORKER_NODE_GROUP = "eksbase-node-group"
WORKER_NODE_IMAGE_ID = "ami-dea4d5a1"

DEPLOY_KUBE_UI = False