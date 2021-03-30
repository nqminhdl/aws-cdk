import os
from aws_cdk import (
    aws_ec2 as ec2,
   aws_elasticloadbalancingv2 as elbv2,
   core
)
class ALBStack(core.Stack):
    def __init__(self, app: core.App, id: str, vpc, asg, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        lb = elbv2.ApplicationLoadBalancer(
                scope = self, id = "LB",
                vpc=vpc,
                internet_facing=True,
                load_balancer_name = "webapp-alb"
                )

        listener = lb.add_redirect(source_port=80, target_port=443)
        listener.connections.allow_default_port_from_any_ipv4("Open to the world")

        # https_listener =  lb.add_listener("HTTPS listener", port=443)
        # https_listener.add_targets("Target", port=80, targets=[asg])
        # https_listener.connections.allow_default_port_from_any_ipv4("Listen on HTTPS")

        core.CfnOutput(self,"LoadBalancer",export_name="LoadBalancer",value=lb.load_balancer_dns_name)
