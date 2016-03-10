#!/bin/bash -e

ctx logger info "---- Set route to FW and start Webserver  $fw_ip "

subnet='172.30.0.0/24'
gw='172.20.0.4'
#gw=$fw_ip

ip=$(ifconfig | grep 172.20 | awk '{print $2}')

# App network gateway
route add -net $subnet gw $gw

cat <<EOF > /root/index.html
<html>
  <head>
    <title>Web Server IP address</title>
  </head>
  <body bgcolor=white>
    This is Web Server ip : $ip
  </body>
</html>
EOF

cd /root

nohup python -m SimpleHTTPServer 80 &
