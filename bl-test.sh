#!/usr/bin/env bash
cfy blueprints upload -b test$1 -p fortinet-simple-blueprint.yaml
sleep 5
cfy deployments create -b test$1 -d test$1 -i fortinet-simple-blueprint-input.yaml 
