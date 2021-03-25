import os
from aws_cdk import (
    aws_ec2 as ec2,
    aws_autoscaling as autoscaling,
    core
)

class AutoscalingStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc, bastion, config, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        prj_name = self.node.try_get_context("project_name")
        env_name = self.node.try_get_context("env")
        name = config['ec2']['name']
        key = config['ec2']['ssh_key']

        ubuntu_ami = ec2.GenericLinuxImage({
            "ap-southeast-1": "ami-028be27cf930f7a43"
            })

        # Create security group for webapp instances
        webapp_sg = ec2.SecurityGroup(self, 'webapp-sg',
            vpc=vpc,
            security_group_name=prj_name + env_name + '-webapp-sg',
            description="SG for webapp Instances",
            allow_all_outbound=True
        )

        webapp_sg.add_ingress_rule(
            peer=ec2.Peer.ipv4(f"{bastion.instance_private_ip}/32"),
            connection=ec2.Port.tcp(22),
            description='Allow all bastion instance to SSH'
        )

        for subnet in vpc.public_subnets:
            webapp_sg.add_ingress_rule(
                peer=ec2.Peer.ipv4(subnet.ipv4_cidr_block),
                connection=ec2.Port.tcp(80),
                description='Allow ELB public subnets to access webapp instances'
            )

        # Create launch template and attach to autoscaling group
        webapp_launch_template   = ec2.LaunchTemplate(self, 'launch-template',
            detailed_monitoring  = False,
            ebs_optimized        = False,
            instance_type        = ec2.InstanceType("t3.small"),
            launch_template_name = f"{name}-launch-template",
            key_name             = f"{key}",
            machine_image        = ubuntu_ami,
            security_group       = webapp_sg
        )

        self.webapp_asg = autoscaling.AutoScalingGroup(self, 'webapp-asg',
            vpc                     = vpc,
            auto_scaling_group_name = prj_name + env_name + '-webapp-asg',
            instance_type           = ec2.InstanceType("t3.small"),
            machine_image           = ubuntu_ami,
            min_capacity            = 1,
            max_capacity            = 1,
            desired_capacity        = 1,
            vpc_subnets             = ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE)
        )
