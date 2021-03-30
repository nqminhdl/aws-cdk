from aws_cdk import (
    aws_eks as eks,
    aws_ec2 as ec2,
    core
)
from aws_cdk.aws_autoscaling import UpdateType

class EKSStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc, config, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        prj_name = self.node.try_get_context("project_name")
        env_name = self.node.try_get_context("env")
        name = config['ec2']['name']
        key = config['ec2']['ssh_key']

        eks_cluster = eks.Cluster(self, 'eks-cluster',
            version             = eks.KubernetesVersion.V1_19,
            cluster_name        = prj_name + env_name + '-eks-cluster',
            vpc                 = vpc,
            vpc_subnets         = [ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE)],
            output_cluster_name = True,
            default_capacity    = 0
        )

        # This code block will provision worker nodes with launch configuration
        eks_cluster.add_auto_scaling_group_capacity('spot-asg-az-a',
            auto_scaling_group_name = prj_name + env_name + '-spot-az-a',
            min_capacity            = 1,
            max_capacity            = 1,
            desired_capacity        = 1,
            key_name                = f"{key}",
            instance_type           = ec2.InstanceType('t3.small'),
            vpc_subnets             = ec2.SubnetSelection(availability_zones=["ap-southeast-1a"],subnet_type=ec2.SubnetType.PRIVATE),
            bootstrap_options       = {
                "kubelet_extra_args": "--node-labels=node.kubernetes.io/lifecycle=spot,daemonset=active,app=general --eviction-hard imagefs.available<15% --feature-gates=CSINodeInfo=true,CSIDriverRegistry=true,CSIBlockVolume=true,ExpandCSIVolumes=true"
            }
        )


        # This code block will provision worker nodes with launch templates
        eks_cluster.add_nodegroup_capacity('spot-nodegroup-az-a',
            nodegroup_name = prj_name + env_name + '-spot-az-a',
            instance_types = [
                ec2.InstanceType('t3a.small'),
                ec2.InstanceType('t3.small')
            ],
            disk_size     = 100,
            min_size      = 1,
            max_size      = 1,
            desired_size  = 1,
            capacity_type = eks.CapacityType.SPOT,
            subnets = ec2.SubnetSelection(availability_zones=["ap-southeast-1a"],subnet_type=ec2.SubnetType.PRIVATE),
        )

        eks_cluster.add_nodegroup_capacity('spot-nodegroup-az-b',
            nodegroup_name = prj_name + env_name + '-spot-az-b',
            instance_types = [
                ec2.InstanceType('t3a.small'),
                ec2.InstanceType('t3.small')
            ],
            min_size      = 1,
            max_size      = 1,
            desired_size  = 1,
            capacity_type = eks.CapacityType.SPOT,
            subnets = ec2.SubnetSelection(availability_zones=["ap-southeast-1b"],subnet_type=ec2.SubnetType.PRIVATE)
        )

        eks_cluster.add_nodegroup_capacity('spot-nodegroup-az-c',
            nodegroup_name = prj_name + env_name + '-spot-az-c',
            instance_types = [
                ec2.InstanceType('t3a.small'),
                ec2.InstanceType('t3.small')
            ],
            min_size      = 1,
            max_size      = 1,
            desired_size  = 1,
            capacity_type = eks.CapacityType.SPOT,
            subnets = ec2.SubnetSelection(availability_zones=["ap-southeast-1c"],subnet_type=ec2.SubnetType.PRIVATE)
        )
