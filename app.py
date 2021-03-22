#!/usr/bin/env python3

import yaml
from aws_cdk import core
from webapp.vpc import VPCStack
from webapp.ec2 import Ec2Stack
from webapp.rds import RDSStack

selected_env = core.Environment(account="658564819138", region="ap-southeast-1")

app = core.App()

config = yaml.load(open('infra.yaml'), Loader=yaml.Loader)
app = core.App()

vpc = VPCStack(app,'vpc', env=selected_env)
ec2 = Ec2Stack(app, 'ec2', env=selected_env, vpc=vpc.vpc, config=config)
rds = RDSStack(app, 'rds', vpc=vpc.vpc, env=selected_env)

app.synth()
