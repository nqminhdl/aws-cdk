from webapp.vpc import VPCStack
from attr import __version__
from aws_cdk import (
    aws_rds as rds,
    aws_ec2 as ec2,
    core
)
import json

class RDSStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc=ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        prj_name = self.node.try_get_context("project_name")
        env_name = self.node.try_get_context("env")

        rds_sg = ec2.SecurityGroup(self, 'rds-sg',
            vpc=vpc,
            security_group_name=prj_name + env_name + '-rds-sg',
            description="SG for RDS",
            allow_all_outbound=True
        )

        for subnet in vpc.private_subnets:
            rds_sg.add_ingress_rule(peer=ec2.Peer.ipv4(subnet.ipv4_cidr_block),connection=ec2.Port.tcp(3306),description='Allow all private subnet to access RDS')

        db_mysql = rds.DatabaseCluster(self,'mysql',
            default_database_name=prj_name + env_name,
            engine=rds.DatabaseClusterEngine.aurora_mysql(
                version=rds.AuroraMysqlEngineVersion.VER_5_7_12
            ),
            instances=1,
            instance_props=rds.InstanceProps(
                vpc=vpc,
                instance_type=ec2.InstanceType(instance_type_identifier="t3.small"),
                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE)
            ),
            removal_policy=core.RemovalPolicy.DESTROY
        )

