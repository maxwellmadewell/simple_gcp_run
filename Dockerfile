FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y gnupg lsb-release wget
#COPY ./gcp/creds.json /etc/
#ENV GOOGLE_APPLICATION_CREDENTIALS=/etc/creds.json

RUN lsb_release -c -s > /tmp/lsb_release
RUN GCSFUSE_REPO=$(cat /tmp/lsb_release); echo "deb http://packages.cloud.google.com/apt gcsfuse-$GCSFUSE_REPO main" | tee /etc/apt/sources.list.d/gcsfuse.list
RUN wget -O - https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -

RUN apt-get update
RUN apt-get install -y gcsfuse

RUN mkdir scripts
COPY mountgcs.sh /scripts/mountgcs.sh
RUN chmod +x /scripts/mountgcs.sh
ENTRYPOINT ["bin/bash", "/scripts/mountgcs.sh"]
