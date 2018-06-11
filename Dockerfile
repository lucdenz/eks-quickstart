FROM python:alpine

WORKDIR /app

ADD . /app

ENV AWS_ACCESS_KEY_ID "S4MPL3K3Y"
ENV AWS_SECRET_ACCESS_KEY "53CR3TK3Y"
ENV AWS_KUBECTL "https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-06-05/bin/linux/amd64/kubectl"
ENV AWS_HEPTIO_AUTH "https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-06-05/bin/linux/amd64/heptio-authenticator-aws"

RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN apk add --update ca-certificates; apk add --update -t deps curl; \
 curl -L ${AWS_KUBECTL} -o /usr/local/bin/kubectl; \
 curl -L ${AWS_HEPTIO_AUTH} -o /usr/local/bin/heptio-authenticator-aws; \
 chmod +x /usr/local/bin/kubectl; \
 chmod +x /usr/local/bin/heptio-authenticator-aws; \
 apk del --purge deps; rm /var/cache/apk/*
