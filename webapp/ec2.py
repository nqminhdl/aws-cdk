import os
from aws_cdk import (
    aws_ec2 as ec2,
    core
)

class Ec2Stack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc, config, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        prj_name = self.node.try_get_context("project_name")
        env_name = self.node.try_get_context("env")
        name = config['ec2']['name']
        key = config['ec2']['ssh_key']

        ubuntu_ami = ec2.GenericLinuxImage({
            "ap-southeast-1": "ami-028be27cf930f7a43"
            })

        instance = ec2.Instance(
                self, 'Instance',
                instance_type = ec2.InstanceType("t3.small"),
                instance_name = f"{name}-test",
                key_name      = f"{key}",
                machine_image = ubuntu_ami,
                vpc           = vpc,
                vpc_subnets   = ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE),
            )
        instance.connections.allow_from_any_ipv4(
                port_range=ec2.Port.tcp(22),
                description = 'Ssh connection')

        core.CfnOutput(self, f'{name}-public-ip', value=instance.instance_private_ip)
