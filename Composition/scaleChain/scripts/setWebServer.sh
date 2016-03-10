#!/bin/bash

ctx logger info "---> Set route to FW 172.20.0.4 and start Webserver  "
ctx logger info "---> Env value fw_lb_ip : $fw_lb_ip  "
ctx logger info "---> Env value fw_app_ip : $fw_app_ip  "

subnet='172.30.0.0/24'
gw='172.20.0.4'
#gw=$fw_app_ip

ip=$(ifconfig | grep 172.20 | awk '{print $2}')

# App network gateway
route add -net $subnet gw $gw

cat <<EOF > /root/index.html
<html>
    <head>
         <title>Web Server IP address</title>
    </head>
    <body bgcolor=white>
        <h1>This is Web Server ip : $ip </h1>
    </body>
</html>
EOF

cd /root
rm -f nohup

dtach -n nohup python -m SimpleHTTPServer 80 

