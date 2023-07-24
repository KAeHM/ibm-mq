#!/bin/bash

tar -xvf /tmp/9.3.0.0-IBM-MQTRIAL-UbuntuLinuxX64.tar.gz -C /tmp
apt-get update
/tmp/MQServer/mqlicense.sh -accept
apt-get install /tmp/MQServer/ibmmq-runtime_9.3.0.0_amd64.deb
apt-get install /tmp/MQServer/ibmmq-gskit_9.3.0.0_amd64.deb
apt-get install /tmp/MQServer/ibmmq-client_9.3.0.0_amd64.deb
apt-get install /tmp/MQServer/ibmmq-sdk_9.3.0.0_amd64.deb
apt-get install python3.10 -y
apt-get install python3.10-venv -y
apt-get install pip -y
apt-get install python3.10-dev -y
echo "alias python=python3.10" >> /etc/bash.bashrc
bash