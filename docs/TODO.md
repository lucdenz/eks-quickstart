TODO

Link the worker nodes by modifying and installing the AWS authenticator configuration map
curl -O https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-06-05/aws-auth-cm.yaml
kubectl apply -f aws-auth-cm.yaml

return the endpoint url and cert from the createEKSCluster call for use in 
generating a kubeconfig file