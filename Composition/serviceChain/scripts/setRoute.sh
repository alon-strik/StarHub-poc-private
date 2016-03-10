#!/bin/bash


subnet='172.30.0.0/24'
gw='172.20.0.3'

# App network gateway

route add -net $subnet gw $gw

