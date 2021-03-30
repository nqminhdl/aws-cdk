#!/usr/bin/env python3

import yaml
from aws_cdk import core
from webapp.vpc import VPCStack
from webapp.ec2 import Ec2Stack
from webapp.autoscaling import AutoscalingStack
# This will be commented in order to wait for feature request 'bootstrap_option' to be supported on launch template
# from webapp.eks import EKSStack
from webapp.rds import RDSStack
from webapp.cloudfront import CloudFrontStack
from webapp.alb import ALBStack

selected_env = core.Environment(account="658564819138", region="ap-southeast-1")


config = yaml.load(open('infra.yaml'), Loader=yaml.Loader)
app = core.App()

vpc = VPCStack(app,'vpc', env=selected_env)
ec2 = Ec2Stack(app, 'ec2', env=selected_env, vpc=vpc.vpc, config=config)
autoscaling = AutoscalingStack(app, 'autoscaling', env=selected_env, vpc=vpc.vpc, bastion=ec2.bastion, config=config)
# This will be commented in order to wait for feature request 'bootstrap_option' to be supported on launch template
# eks = EKSStack(app, 'eks',  env=selected_env, vpc=vpc.vpc, config=config)
alb = ALBStack(app, 'alb', env=selected_env, vpc=vpc.vpc, asg=autoscaling.webapp_asg)
rds = RDSStack(app, 'rds', vpc=vpc.vpc, env=selected_env)
cloudfront = CloudFrontStack(app, 'cloudfront', env=selected_env)

core.Tags.of(app).add("Managed-By", "DevOps")
core.Tags.of(app).add("Provisioned-By", "AWS CDK")
core.Tags.of(app).add("CDK Language", "Python")

app.synth()
