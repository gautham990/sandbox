from aws_cdk import Stack
from aws_cdk import aws_s3 as s3
from aws_cdk import RemovalPolicy
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecs_patterns as ecs_patterns
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_iam as iam  
from aws_cdk import aws_logs as logs
from constructs import Construct
from aws_cdk import CfnOutput

class SandboxStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        app_name = "Sandbox"

        #S3 Bucket
        bucket = s3.Bucket(self, "SandboxBucket", bucket_name="sandbox-bucket-837648",removal_policy=RemovalPolicy.DESTROY) 
        CfnOutput(self, "BucketArnOutput", value=bucket.bucket_arn)
        
        #VPC
        vpc = ec2.Vpc(self, f"{app_name}",cidr="10.0.0.0/16",max_azs=2, 
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name=f"{app_name}-PublicSubnet",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name=f"{app_name}-PrivateSubnet",
                    # subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                    cidr_mask=24
                )
            ],
            nat_gateways=0
        )

        #Secruity Groups
        internetSecurityGroup = ec2.SecurityGroup(self, "InternetSecurityGroup", vpc=vpc, allow_all_outbound=True, security_group_name=f"{app_name}-InternetSecurityGroup")
        internetSecurityGroup.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(443), "Allow HTTPS from anywhere")
        intranetSecurityGroup = ec2.SecurityGroup(self, "IntranetSecurityGroup", vpc=vpc, allow_all_outbound=True, security_group_name=f"{app_name}-IntranetSecurityGroup")
        intranetSecurityGroup.add_ingress_rule(ec2.Peer.security_group_id(internetSecurityGroup.security_group_id), ec2.Port.all_traffic(), "Allow traffic from internet SG")

        # #EC2 Instance
        # instance = ec2.Instance(self, "SandboxInstance", instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO), machine_image=ec2.MachineImage.from_ssm_parameter(
        #     '/aws/service/canonical/ubuntu/server/jammy/stable/current/amd64/hvm/ebs-gp2/ami-id',
        #     os=ec2.OperatingSystemType.LINUX
        # ), instance_name=f"{app_name}Instance", vpc=vpc, vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED), security_group=intranetSecurityGroup)
        # CfnOutput(self, "InstanceOutput", value=instance.instance_id)

        #ECS Cluster
        cluster = ecs.Cluster(self, "FargateCluster",vpc=vpc,container_insights=True,cluster_name=f"{app_name}Cluster") 