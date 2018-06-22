FROM python:alpine

WORKDIR /app

ADD . /app

RUN pip install awscli

RUN apk add --update ca-certificates; apk add --update -t deps curl; \
 curl -L https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-06-05/bin/linux/amd64/kubectl -o /usr/local/bin/kubectl; \
 curl -L https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-06-05/bin/linux/amd64/heptio-authenticator-aws -o /usr/local/bin/heptio-authenticator-aws; \
 chmod +x /usr/local/bin/kubectl; \
 chmod +x /usr/local/bin/heptio-authenticator-aws; \
 apk del --purge deps; rm /var/cache/apk/*

ENV CLUSTER_NAME eksbase

RUN mkdir -p /root/.kube; \
 cp kubeconfig /root/.kube/config-${CLUSTER_NAME} 

ENV KUBECONFIG /root/.kube/config-${CLUSTER_NAME}

RUN kubectl apply -f aws-auth-cm.yaml