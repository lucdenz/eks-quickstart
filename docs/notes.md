/data/GitHub/ekscore # ekscore
INFO: Deleted [eks-service-role] successfully
INFO: Created [eks-service-role] using IAM with managed policies
/data/GitHub/ekscore # python
Python 3.6.5 (default, Jun  6 2018, 23:08:29) 
[GCC 6.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import ekscore
>>> ekscore.run()
INFO: Deleted [eks-service-role] successfully
INFO: Created [eks-service-role] using IAM with managed policies
>>> ekscore.cluster.deleteEKSRole("eks-service-role")
INFO: Deleted [eks-service-role] successfully
>>> ekscore.cluster.deleteEKSRole("eks-service-role")
INFO: Role not found for eks-service-role
>>> result = ekscore.cluster.createEKSRole("eks-service-role")
INFO: Created [eks-service-role] using IAM with managed policies
>>> result = ekscore.cluster.createEKSRole("eks-service-role")
ERROR: An EntityAlreadyExists exception occurred
ERROR: Role with name eks-service-role already exists.
/data/GitHub/ekscore # 


    """
    userHome = os.environ["HOME"]
    kubeDir = "{}/.kube/".format(userHome)
    fileName = "{}config-{}".format(kubeDir, clusterName)
    os.makedirs(kubeDir, exist_ok=True)
    """


def buildDockerImage(clusterName):
    dockerfile = """
    FROM python:alpine

    WORKDIR /app

    ADD . /app

    ENV CLUSTER_NAME eksbase
    ENV KUBECONFIG ~/.kube/config-$CLUSTER_NAME

    RUN mkdir -p ~/.kube
    # RUN cp kubeconfig ~/.kube/config-$CLUSTER_NAME
    """
    dockerfile = BytesIO(dockerfile.encode('utf-8'))

    client = docker.APIClient(base_url="unix://var/run/docker.sock")
    response = [
        line for line in client.build(
            fileobj=dockerfile, 
            rm=True, 
            tag="awskube"
        )
    ]
    print(response)



        # createKubeconfigFile("endpointUrl", "certData", clusterName)

    # path = os.path.dirname(os.path.abspath(__file__))

    # os.system("docker build -t awskube " + path)

    # print("INFO: Run your client container with:")
    # print("INFO: docker run -it --rm --env-file ~/.aws/awscreds.sh awskube /bin/ash")



    