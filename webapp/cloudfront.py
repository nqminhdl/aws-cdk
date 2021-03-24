from aws_cdk import (
    aws_certificatemanager, aws_s3 as s3,
    aws_cloudfront as cloudfront,
    core
)

class CloudFrontStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, frontend_bucket, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        prj_name = self.node.try_get_context("project_name")
        env_name = self.node.try_get_context("env")

        media_distribution = cloudfront.CloudFrontWebDistribution(self, 'media-distribution',
            origin_configs  = [
                cloudfront.SourceConfiguration(
                    behaviors = [
                        cloudfront.Behavior(is_default_behavior=True)
                    ],
                    origin_path = '/media',
                    s3_origin_source = cloudfront.S3OriginConfig(
                        s3_bucket_source = s3.Bucket.from_bucket_name(self, 'frontend_bucket', frontend_bucket),
                        origin_access_identity = cloudfront.OriginAccessIdentity(self,'frontend-origin')
                    )
                )
            ],
            #Edege server location https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_cloudfront/PriceClass.html#aws_cdk.aws_cloudfront.PriceClass
            price_class   = cloudfront.PriceClass.PRICE_CLASS_ALL,
            viewer_certificate = cloudfront.ViewerCertificate.from_acm_certificate(
                certificate = aws_certificatemanager.Certificate.certificate_arn("arn:asdasd"),
                aliases = "abc.domainname.com",
                security_policy = cloudfront.SecurityPolicyProtocol.TLS_V1_2_2019
            )
        )
