"""
TODO
- return the endpoint url and cert from the createEKSCluster call for use in
  generating a kubeconfig file
"""

import time
import boto3
from botocore.exceptions import ClientError

from eksbase.utils import exceptionHandler

# Create a Service Role for EKS (Uses mature resource API)
# Returns the ARN as a string
def createEKSRole(serviceRoleName):
    try:
        iam = boto3.resource("iam")
        role = iam.create_role(
            RoleName=serviceRoleName,
            AssumeRolePolicyDocument='{ "Version": "2012-10-17", "Statement": [ { "Sid": "", "Effect": "Allow", "Principal": { "Service": "eks.amazonaws.com" }, "Action": "sts:AssumeRole" } ]}'
        )       
        response = role.attach_policy(
            PolicyArn="arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
        )
        response = role.attach_policy(
            PolicyArn="arn:aws:iam::aws:policy/AmazonEKSServicePolicy"
        )
        print("INFO: Created [" + serviceRoleName + "] using IAM with managed policies")
        return role.arn
    except ClientError as e:
        exceptionHandler(e)

def deleteEKSRole(serviceRoleName):
    try:
        iam = boto3.resource("iam")
        role = iam.Role(serviceRoleName)
        response = role.detach_policy(
            PolicyArn="arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
        )
        response = role.detach_policy(
            PolicyArn="arn:aws:iam::aws:policy/AmazonEKSServicePolicy"
        )
        response = role.delete()
        print("INFO: Deleted [" + serviceRoleName + "] successfully")
    except ClientError as e:
        exceptionHandler(e)

# Create the EKS VPC Network (Have to use low level client for waiters)
# Returns a list of dict items
def createEKSClusterVPC(networkStackName, networkStackTemplateURL):
    try:
        client = boto3.client("cloudformation")
        waiter = client.get_waiter('stack_create_complete')
        response = client.create_stack(
            StackName=networkStackName,
            TemplateURL=networkStackTemplateURL
        )
        waiter.wait(
            StackName=networkStackName
        )
        print("INFO: Created [" + networkStackName + "] using CloudFormation")
        response = client.describe_stacks(
            StackName=networkStackName
        )
        return response["Stacks"][0]["Outputs"]
    except ClientError as e:
        exceptionHandler(e)

def deleteEKSClusterVPC(networkStackName):
    try:
        client = boto3.client("cloudformation")
        waiter = client.get_waiter('stack_delete_complete')
        response = client.delete_stack(
            StackName=networkStackName
        )
        waiter.wait(
            StackName=networkStackName
        )
        print("INFO: Deleted [" + stackName + "] successfully")
    except ClientError as e:
        exceptionHandler(e)

# Create the actual EKS Cluster
# Need wait helpers until EKS waiters are made
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

def createEKSCluster(clusterName, serviceRoleArn, networkStackOutputs):
    for i in networkStackOutputs:
        if i["OutputKey"] == "SecurityGroups":
            securityGroup = i["OutputValue"]
        if i["OutputKey"] == "SubnetIds":
            subnetList = i["OutputValue"].split(",")

    try:
        client = boto3.client("eks")
        response = client.create_cluster(
            name=clusterName,
            roleArn=serviceRoleArn,
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