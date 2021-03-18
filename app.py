#!/usr/bin/env python3

from aws_cdk import core
from webapp.vpc import VPCStack

selected_env = core.Environment(account="658564819138", region="us-east-1")

app = core.App()

vpc = VPCStack(app,'vpc', env=selected_env)

app.synth()
