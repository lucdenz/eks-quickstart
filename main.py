# This python program will be running inside the container and pull in the 
# config from config.yaml
# Put error handling around creates and deletes. Gets are fine.
import yaml
import boto3
from botocore.exceptions import ClientError
import sys

# Pull in the config file
with open("config.yaml", "r") as config:
    cfg = yaml.load(config)

IDEMPOTENT_DEPLOY = cfg["IdempotentDeploy"]
CLUSTER_NAME = cfg["ClusterName"]
SERVICE_ROLE_NAME = cfg["ServiceRoleName"]
NETWORK_STACK_NAME = cfg["NetworkStackName"]
NETWORK_STACK_TEMPLATE_URL = cfg["NetworkStackTemplateURL"]

# A basic exception handling function that allows known errors
def exceptionHandler(exception):
    errorCode = exception.response["Error"]["Code"]
    errorMessage = exception.response["Error"]["Message"]

    if errorCode == "NoSuchEntity":
        print("INFO: " + errorMessage)
    elif errorCode == "EntityAlreadyExists":
        print("INFO: " + errorMessage)
    elif errorCode == "AlreadyExistsException":
        print("INFO: " + errorMessage)
    else:
        print("ERROR: An " + errorCode + " exception occurred")
        print("ERROR: " + errorMessage)
        sys.exit()

# Clean the environment if idempotent deploy is enabled
def cleanAll():
    try:
        iam = boto3.resource("iam")
        role = iam.Role(SERVICE_ROLE_NAME)
        response = role.detach_policy(
            PolicyArn="arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
        )
        response = role.detach_policy(
            PolicyArn="arn:aws:iam::aws:policy/AmazonEKSServicePolicy"
        )
        response = role.delete()
    except ClientError as e:
        exceptionHandler(e)
    
    try:
        client = boto3.client("cloudformation")
        waiter = client.get_waiter('stack_delete_complete')
        response = client.delete_stack(
            StackName=NETWORK_STACK_NAME
        )
        waiter.wait(
            StackName=NETWORK_STACK_NAME
        )
        print("INFO: Deleted old resources successfully")
    except ClientError as e:
        exceptionHandler(e)

# Create a Service Role for EKS (Uses mature resource API)
def createEKSRole(roleName):
    try:
        iam = boto3.resource("iam")
        role = iam.create_role(
            RoleName=roleName,
            AssumeRolePolicyDocument='{ "Version": "2012-10-17", "Statement": [ { "Sid": "", "Effect": "Allow", "Principal": { "Service": "eks.amazonaws.com" }, "Action": "sts:AssumeRole" } ]}'
        )       
        response = role.attach_policy(
            PolicyArn="arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
        )
        response = role.attach_policy(
            PolicyArn="arn:aws:iam::aws:policy/AmazonEKSServicePolicy"
        )
        print("INFO: Created [" + roleName + "] using IAM with managed policies")
    except ClientError as e:
        exceptionHandler(e)
    
    return role.arn

# Create the EKS VPC Network (Have to use low level client for waiters)
def createEKSClusterVPC(stackName, templateURL):
    try:
        client = boto3.client("cloudformation")
        waiter = client.get_waiter('stack_create_complete')
        response = client.create_stack(
            StackName=stackName,
            TemplateURL=templateURL
        )
        waiter.wait(
            StackName=stackName
        )
        print("INFO: Created [" + stackName + "] using CloudFormation")
    except ClientError as e:
        exceptionHandler(e)


# TODO
# Create the actual EKS Cluster
# kubectl cluster-info

# TODO
# Link the cluster to the kubectl CLI by creating a kubeconfig file
# export KUBECONFIG=$KUBECONFIG:~/.kube/config-<clustername>

# TODO
# Create a set of minions by running a CloudFormation template
# https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-06-05/amazon-eks-nodegroup.yaml

# TODO
# Link the worker nodes by modifying and installing the AWS authenticator configuration map
# curl -O https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-06-05/aws-auth-cm.yaml
# kubectl apply -f aws-auth-cm.yaml

if IDEMPOTENT_DEPLOY:
    print("INFO: Starting EKS deployment with IdempotentDeploy ON")
    cleanAll()
else:
    print("INFO: Starting EKS deployment with IdempotentDeploy OFF")

ServiceRoleARN = createEKSRole(SERVICE_ROLE_NAME)

createEKSClusterVPC(NETWORK_STACK_NAME, NETWORK_STACK_TEMPLATE_URL)


