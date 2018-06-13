# EKS Core
Amazon EKS is a Fully managed Kubernetes control plane (Master). The setup involves running AWS services and installing local cli tools.

## What is EKS Core
An application that provisions an EKS cluster and associated client.

## Prerequisites
- An AWS account
- Python 3
- The AWS CLI
- Docker installed on your local machine

## Getting started
### How the environment is set up
A local Docker container will be used as the client. It contains:
- The AWS CLI for managing AWS services
- The kubectl CLI for interacting with the Kubernetes master
- The heptio-authenticator to use AWS credentials in kubectl

In AWS land we will have:
- A service role so EKS can manage the provisioning of EC2 instances
- A VPC in which to run the EKS Cluster
- The EKS Cluster itself
- Worker EC2 nodes to attach to the Cluster for pod deployment

### Installation
pip install -r requirements.txt
pip install .
ekscore

docker build -t awskube .
source ~/.aws/awscreds.sh
docker run -it --rm --env AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID --env AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY awskube /bin/ash

## Notes
- docker run -it --rm -v ~/:/data python:alpine /bin/ash
- docker rmi $(docker images -q)
