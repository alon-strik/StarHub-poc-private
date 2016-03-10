#!/bin/bash

echo "--- Start deploying service chain ---"

cfy deployments delete -d serviceChain-f5

cfy blueprints delete -b firewall
cfy blueprints delete -b f5-bigip
cfy blueprints delete -b serviceChain-f5

cfy blueprints upload -b firewall     -p firewall.yaml
cfy blueprints upload -b f5-bigip -p f5-bigip.yaml
cfy blueprints upload -b serviceChain-f5 -p serviceChain-f5.yaml

cfy deployments create -b serviceChain-f5 -d serviceChain-f5 -i serviceChain-input.yaml

cfy executions start -d  serviceChain-f5 -w install
cfy executions list | grep serviceChain-f5
