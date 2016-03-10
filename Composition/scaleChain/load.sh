#!/bin/bash

echo "--- Start deploying service chain ---"

cfy deployments delete -d serviceChain

cfy blueprints delete -b firewall
cfy blueprints delete -b loadbalancer
cfy blueprints delete -b serviceChain
cfy blueprints delete -b webserver 

cfy blueprints upload -b firewall     -p firewall.yaml
cfy blueprints upload -b loadbalancer -p loadbalancer.yaml
cfy blueprints upload -b serviceChain -p serviceChain.yaml
cfy blueprints upload -b webserver    -p webserver.yaml

cfy deployments create -b serviceChain -d serviceChain

cfy executions start -d  serviceChain -w install
cfy executions list | grep serviceChain
