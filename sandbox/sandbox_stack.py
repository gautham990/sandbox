from aws_cdk import Stack
from aws_cdk import aws_s3 as s3
from aws_cdk import RemovalPolicy
from constructs import Construct
from aws_cdk import CfnOutput

class SandboxStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(self, "SandboxBucket", bucket_name="sandbox-bucket-837648",removal_policy=RemovalPolicy.DESTROY) 
        CfnOutput(self, "BucketArnOutput", value=bucket.bucket_arn)