# This python program will be running inside the container and pull in the 
# config from config.yaml
# Put error handling around creates and deletes. Gets are fine.
import yaml
import boto3
from botocore.exceptions import ClientError
import sys
import time

# Pull in the config file
with open("config.yaml", "r") as config:
    cfg = yaml.load(config)

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
    else:
        print("ERROR: An " + errorCode + " exception occurred")
        print("ERROR: " + errorMessage)
        sys.exit()

# Create a Service Role for EKS (Uses mature resource API)
# Returns the ARN as a string
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
        return role.arn
    except ClientError as e:
        exceptionHandler(e)

def deleteEKSRole(roleName):
    try:
        iam = boto3.resource("iam")
        role = iam.Role(roleName)
        response = role.detach_policy(
            PolicyArn="arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
        )
        response = role.detach_policy(
            PolicyArn="arn:aws:iam::aws:policy/AmazonEKSServicePolicy"
        )
        response = role.delete()
        print("INFO: Deleted [" + roleName + "] successfully")
    except ClientError as e:
        exceptionHandler(e)

# Create the EKS VPC Network (Have to use low level client for waiters)
# Returns a list of dict items
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
        response = client.describe_stacks(
            StackName=stackName
        )
        return response["Stacks"][0]["Outputs"]
    except ClientError as e:
        exceptionHandler(e)

def deleteEKSClusterVPC(stackName):
    try:
        client = boto3.client("cloudformation")
        waiter = client.get_waiter('stack_delete_complete')
        response = client.delete_stack(
            StackName=stackName
        )
        waiter.wait(
            StackName=stackName
        )
        print("INFO: Deleted [" + stackName + "] successfully")
    except ClientError as e:
        exceptionHandler(e)


# TODO
# Create the actual EKS Cluster
# Use stack.outputs["key"] from CloudFormation
# Need these wait helpers until EKS waiters are made
def waitEKSClusterActive(clusterName):
    client = boto3.client("eks")
    clusterNotActive = True

    while clusterNotActive:
        time.sleep(30)
        resource = client.describe_cluster(
            name=clusterName
        )
        if resource["cluster"]["status"] == "ACTIVE":
            clusterNotActive = False

def waitEKSClusterDeleted(clusterName):
    client = boto3.client("eks")
    clusterDeleting = True

    while clusterDeleting:
        time.sleep(30)
        resource = client.delete_cluster(
            name=clusterName
        )
        if resource["cluster"]["status"] != "DELETING":
            clusterDeleting = False

def createEKSCluster(clusterName, roleArn, networkStackOutputs):
    for i in networkStackOutputs:
        if i["OutputKey"] == "SecurityGroups":
            securityGroup = i["OutputValue"]
        if i["OutputKey"] == "SubnetIds":
            subnetList = i["OutputValue"].split(",")

    try:
        client = boto3.client("eks")
        response = client.create_cluster(
            name=clusterName,
            roleArn=roleArn,
            resourcesVpcConfig={
                "subnetIds": subnetList,
                "securityGroupIds": [
                    securityGroup
                ]
            }
        )
        waitEKSClusterActive(clusterName)
        print("INFO: Created [" + clusterName + "] EKS cluster successfully")
    except ClientError as e:
        exceptionHandler(e)

def deleteEKSCluster(clusterName):
    try:
        client = boto3.client("eks")
        response = client.delete_cluster(
            name=clusterName
        )
        waitEKSClusterDeleted(clusterName)
        print("INFO: Deleted [" + clusterName + "] successfully")
    except ClientError as e:
        exceptionHandler(e)

        


# TODO
# Link the cluster to the kubectl CLI by creating a kubeconfig file
# export KUBECONFIG=$KUBECONFIG:~/.kube/config-<clustername>
# kubectl cluster-info

# TODO
# Create a set of minions by running a CloudFormation template
# https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-06-05/amazon-eks-nodegroup.yaml

# TODO
# Link the worker nodes by modifying and installing the AWS authenticator configuration map
# curl -O https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-06-05/aws-auth-cm.yaml
# kubectl apply -f aws-auth-cm.yaml


# deleteEKSCluster(CLUSTER_NAME)
# deleteEKSClusterVPC(NETWORK_STACK_NAME)
# deleteEKSRole(SERVICE_ROLE_NAME)


# serviceRoleARN = createEKSRole(SERVICE_ROLE_NAME)
# networkStackOutputs = createEKSClusterVPC(NETWORK_STACK_NAME, NETWORK_STACK_TEMPLATE_URL)
# createEKSCluster(CLUSTER_NAME, serviceRoleARN, networkStackOutputs)
