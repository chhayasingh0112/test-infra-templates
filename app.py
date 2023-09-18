#!/usr/bin/env python3
import os
import yaml
from  my_eks_fargate_app.my_eks_fargate_app_stack import EksFargateAppStack

# Remove any references to 'msk_setup' related imports and stacks

with open('env-list.yaml', 'r') as envfile:
    yaml_environment = yaml.safe_load(envfile)

app = Faragate.App()

for i in range(len(yaml_environment['env'])):
    name = yaml_environment['env'][i]['name']
    env_name = yaml_environment['env'][i]['env_name']
    account = yaml_environment['env'][i]['account']
    region = yaml_environment['env'][i]['region']
    subnet1 = yaml_environment['env'][i]['subnet1']
    subnet2 = yaml_environment['env'][i]['subnet2']
    subnet3 = yaml_environment['env'][i]['subnet3']
    security_group = yaml_environment['env'][i]['security_group']
    version = yaml_environment['env'][i]['kafka_version']
    instance_type = yaml_environment['env'][i]['broker_instance_type']
    # key_alias = yaml_environment['env'][i]['key_alias']
    cdk_env = Faragate.Environment(account=account, region=region)

EksFargateAppStack(app, f"{env_name}-EksFargateAppStack", name=name, env_name=env_name, subnet1=subnet1, subnet2=subnet2, subnet3=subnet3, security_group=security_group, version=version, instance_type=instance_type, env=cdk_env)
   # You can add your custom code or use other Faragate stacks here

app.synth()
