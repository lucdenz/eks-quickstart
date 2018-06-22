import time
import boto3
import pprint
from botocore.exceptions import ClientError

from eksbase.utils import exceptionHandler

# Create a Service Role for EKS (Uses mature resource API)
# Returns the IAM Role class
def createServiceRole(name):
    try:
        iam = boto3.resource("iam")
        role = iam.create_role(
            RoleName=name,
            AssumeRolePolicyDocument='{ "Version": "2012-10-17", "Statement": [ { "Sid": "", "Effect": "Allow", "Principal": { "Service": "eks.amazonaws.com" }, "Action": "sts:AssumeRole" } ]}'
        )       
        role.attach_policy(
            PolicyArn="arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
        )
        role.attach_policy(
            PolicyArn="arn:aws:iam::aws:policy/AmazonEKSServicePolicy"
        )
        print("INFO: Created [" + name + "] using IAM with managed policies")
        return role
    except ClientError as e:
        exceptionHandler(e)

def deleteServiceRole(name):
    try:
        iam = boto3.resource("iam")
        role = iam.Role(name)
        role.detach_policy(
            PolicyArn="arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
        )
        role.detach_policy(
            PolicyArn="arn:aws:iam::aws:policy/AmazonEKSServicePolicy"
        )
        role.delete()
        print("INFO: Deleted [" + name + "] successfully")
    except ClientError as e:
        exceptionHandler(e)

# Create the EKS VPC Network (Have to use low level client for waiters)
# Returns a dict of the cloudformation outputs
def createVPC(stackName, templateURL):
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

def deleteVPC(stackName):
    try:
        client = boto3.client("cloudformation")
        waiter = client.get_waiter('stack_delete_complete')
        client.delete_stack(
            StackName=stackName
        )
        waiter.wait(
            StackName=stackName
        )
        print("INFO: Deleted [" + stackName + "] successfully")
    except ClientError as e:
        exceptionHandler(e)

# Create the actual EKS Cluster
# Need wait helpers until EKS waiters are made
def waitClusterActive(name):
    client = boto3.client("eks")
    clusterNotActive = True

    while clusterNotActive:
        time.sleep(30)
        resource = client.describe_cluster(
            name=name
        )
        if resource["cluster"]["status"] == "ACTIVE":
            clusterNotActive = False

# Go ahead and create the EKS cluster with all the previous resources
# Returns the EKS create_cluster dict response.
# https://boto3.readthedocs.io/en/latest/reference/services/eks.html#EKS.Client.create_cluster
def createCluster(name, roleArn, networkStackOutputs):
    for i in networkStackOutputs:
        if i["OutputKey"] == "SecurityGroups":
            securityGroup = i["OutputValue"]
        if i["OutputKey"] == "SubnetIds":
            subnetList = i["OutputValue"].split(",")

    try:
        client = boto3.client("eks")
        response = client.create_cluster(
            name=name,
            roleArn=roleArn,
            resourcesVpcConfig={
                "subnetIds": subnetList,
                "securityGroupIds": [
                    securityGroup
                ]
            }
        )
        waitClusterActive(name)
        print("INFO: Created [" + name + "] EKS cluster successfully")
        return response
    except ClientError as e:
        exceptionHandler(e)

def waitClusterDeleted(name):
    client = boto3.client("eks")
    clusterDeleting = True

    while clusterDeleting:
        time.sleep(30)
        resource = client.delete_cluster(
            name=name
        )
        if resource["cluster"]["status"] != "DELETING":
            clusterDeleting = False

def deleteCluster(name):
    try:
        client = boto3.client("eks")
        response = client.delete_cluster(
            name=name
        )
        waitClusterDeleted(name)
        print("INFO: Deleted [" + name + "] successfully")
        return response
    except ClientError as e:
        exceptionHandler(e)

def describeCluster(name):
    try:
        client = boto3.client("eks")
        response = client.describe_cluster(
            name=name
        )
        return response["cluster"]
    except ClientError as e:
        exceptionHandler(e)