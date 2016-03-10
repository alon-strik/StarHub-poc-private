cfy blueprints delete -b vtm-blueprint
cfy blueprints delete -b fortinet-blueprint
cfy blueprints delete -b serviceChain
cfy blueprints upload -b vtm-blueprint -p vtm-blueprint.yaml
cfy blueprints upload -b fortinet-blueprint -p fortinet-blueprint.yaml
cfy blueprints upload -b serviceChain -p serviceChain.yaml
cfy deployments create -b serviceChain -d serviceChain

