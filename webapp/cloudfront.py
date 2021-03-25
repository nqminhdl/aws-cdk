from aws_cdk import (
    aws_certificatemanager, aws_s3 as s3,
    aws_cloudfront as cloudfront,
    core
)

class CloudFrontStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        prj_name = self.node.try_get_context("project_name")
        env_name = self.node.try_get_context("env")

        media_distribution_oai = cloudfront.OriginAccessIdentity(self, 'media-distribution-oai')
        media_distribution_oai.apply_removal_policy(core.RemovalPolicy.DESTROY)

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

        media_distribution = cloudfront.CloudFrontWebDistribution(self, 'media-distribution',
            origin_configs  = [
                cloudfront.SourceConfiguration(
                    behaviors = [
                        cloudfront.Behavior(is_default_behavior=True)
                    ],
                    origin_path = '/media',
                    s3_origin_source = cloudfront.S3OriginConfig(
                        s3_bucket_source = frontend_bucket,
                        origin_access_identity = cloudfront.OriginAccessIdentity(self,'frontend-origin')
                    )
                )
            ],
            #Edege server location https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_cloudfront/PriceClass.html#aws_cdk.aws_cloudfront.PriceClass
            price_class   = cloudfront.PriceClass.PRICE_CLASS_ALL
        )
        media_distribution.apply_removal_policy(core.RemovalPolicy.DESTROY)
