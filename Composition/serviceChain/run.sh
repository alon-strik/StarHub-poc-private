cfy blueprints delete -b vtm-blueprint
cfy blueprints delete -b fortinet-blueprint
cfy blueprints delete -b serviceChain2
cfy blueprints upload -b vtm-blueprint -p vtm-blueprint.yaml
cfy blueprints upload -b fortinet-blueprint -p fortinet-blueprint.yaml
cfy blueprints upload -b serviceChain2 -p serviceChain.yaml
cfy deployments create -b serviceChain2 -d serviceChain2

