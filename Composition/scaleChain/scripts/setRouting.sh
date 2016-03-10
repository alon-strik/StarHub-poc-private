#!/bin/bash

ctx logger info "---> Set route to FW GW 172.30.0.250 "

subnet='172.20.0.0/29'
gw='172.30.0.250'

#route del -net  $subnet gw 172.30.0.3
#route add -net  $subnet gw $gw

