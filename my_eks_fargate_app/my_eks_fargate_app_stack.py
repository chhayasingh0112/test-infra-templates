from aws_cdk import (
    Stack,
    aws_eks as eks,
    aws_ec2 as ec2,
)
from constructs import Construct
import os
import yaml

class EksFargateAppStack(Stack):

    def __init__(self, scope: Construct, id: str, env_name: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Load environment parameters from YAML
        with open('env-list.yaml', 'r') as envfile:
            yaml_environment = yaml.safe_load(envfile)

        env_params = None
        for env_entry in yaml_environment['env']:
            if env_entry['env_name'] == env_name:
                env_params = env_entry
                break

        if not env_params:
            raise ValueError(f"No parameters found for environment with name '{env_name}'")

        vpc_id = env_params['vpc_id']
        subnet_ids = env_params['subnet_ids']
        kubernetes_version = env_params['kubernetes_version']

        # Create VPC
        vpc = ec2.Vpc.from_lookup(self, 'Vpc', vpc_id=vpc_id)

        # Create EKS Fargate cluster
        cluster = eks.FargateCluster(self, "EksFargateCluster",
            vpc=vpc,
            default_capacity=0,  # This will create an empty cluster without nodes
            version=eks.KubernetesVersion.from_version_string(kubernetes_version)
        )

        # Add Fargate profile to the cluster
        cluster.add_auto_scaling_group_capacity("FargateNodes",
            min_capacity=1,
            max_capacity=3,
            instance_type=eks.FargateProfileSelector(instance_types=[eks.FargateInstanceType.STANDARD_1_4]),
            spot_price="0.0835"
        )

# This part is needed if you intend to use this script as a standalone CDK app
from aws_cdk import core

app = core.App()
env_name = "dev"  # Specify the environment name you want to use
EksFargateAppStack(app, f"EksFargateAppStack-{env_name}", env_name=env_name)
app.synth()
