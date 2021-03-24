from aws_cdk import (
    aws_s3 as s3,
    core
)

class S3Stack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        prj_name = self.node.try_get_context("project_name")
        env_name = self.node.try_get_context("env")

        frontend_bucket = s3.Bucket(self, 'frontend-bucket',
            access_control = s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
            encryption     = s3.BucketEncryption.S3_MANAGED,
            bucket_name    = prj_name + env_name + '-bucket',
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=True,
                block_public_policy=True,
                ignore_public_acls=True,
                restrict_public_buckets=True
            ),
            removal_policy=core.RemovalPolicy.DESTROY
        )

        core.CfnOutput(self,'frontend-bucket-name-output',
            value=frontend_bucket.bucket_name,
            export_name='frontend-bucket-name'
        )
