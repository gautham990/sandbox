from aws_cdk import Stack
from aws_cdk import aws_s3 as s3
from aws_cdk import RemovalPolicy
from aws_cdk import aws_ec2 as ec2
from constructs import Construct
from aws_cdk import CfnOutput

class SandboxStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(self, "SandboxBucket", bucket_name="sandbox-bucket-837648",removal_policy=RemovalPolicy.DESTROY) 
        CfnOutput(self, "BucketArnOutput", value=bucket.bucket_arn)
        vpc_name = "Sandbox"

        vpc = ec2.Vpc(self, f"{vpc_name}",cidr="10.0.0.0/16",max_azs=2, 
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name=f"{vpc_name}-PublicSubnet",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name=f"{vpc_name}-PrivateSubnet",
                    # subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    ubnet_type=ec2.SubnetType.PRIVATE,
                    cidr_mask=24
                )
            ],
            nat_gateways=0
        )
        internetSecurityGroup = ec2.SecurityGroup(self, "InternetSecurityGroup", vpc=vpc, allow_all_outbound=True, security_group_name=f"{vpc_name}-InternetSecurityGroup")
        internetSecurityGroup.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(443), "Allow HTTPS from anywhere")
        intranetSecurityGroup = ec2.SecurityGroup(self, "IntranetSecurityGroup", vpc=vpc, allow_all_outbound=True, security_group_name=f"{vpc_name}-IntranetSecurityGroup")
        intranetSecurityGroup.add_ingress_rule(ec2.Peer.security_group_id(internetSecurityGroup.id), ec2.Port.all_traffic, "Allow traffic from intranet SG")