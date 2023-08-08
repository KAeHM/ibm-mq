#!/bin/bash

tar -xvf /tmp/9.3.0.0-IBM-MQTRIAL-UbuntuLinuxX64.tar.gz -C /tmp
apt-get update
/tmp/MQServer/mqlicense.sh -accept
apt-get install /tmp/MQServer/*.deb -y
opt/mqm/bin/setmqinst -i -p /opt/mqm/
. opt/mqm/bin/setmqenv -s
su - mqm -c "dspmqver"
cp -r /opt/mqm/web/mq/samp/configuration/basic_registry.xml /var/mqm/web/installations/Installation1/servers/mqweb/
rm /var/mqm/web/installations/Installation1/servers/mqweb/mqwebuser.xml
cd /var/mqm/web/installations/Installation1/servers/mqweb/
mv basic_registry.xml mqwebuser.xml
chmod a+rwx /var/mqm/web/installations/Installation1/servers/mqweb/mqwebuser.xml
su - mqm -c "setmqweb properties -k httpHost -v '*'"
/bin/bash