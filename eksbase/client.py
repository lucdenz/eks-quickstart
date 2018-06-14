""" 
This will create and configure a Docker container as a client to the new
EKS instance. You will log into the container and use the configured
kubectl CLI.
 """

# import docker

"""
TODO
Link the cluster to the kubectl CLI by creating a kubeconfig file
export KUBECONFIG=$KUBECONFIG:~/.kube/config-<clustername>
kubectl cluster-info
"""

"""
TODO
Link the worker nodes by modifying and installing the AWS authenticator configuration map
curl -O https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-06-05/aws-auth-cm.yaml
kubectl apply -f aws-auth-cm.yaml
"""