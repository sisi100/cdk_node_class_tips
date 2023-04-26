# python app_s3_cloudfront.py

import aws_cdk as cdk
from aws_cdk import aws_cloudfront as cloudfront
from aws_cdk import aws_cloudfront_origins as origins
from aws_cdk import aws_s3 as s3

app = cdk.App()
stack = cdk.Stack(app, "HogeStack")

# バケットの L2 コンストラクト
bucket = s3.Bucket(stack, "HogeBucket")

# ここまでのコンストラクトツリーを表示する
# print([node.to_string() for node in app.node.find_all()])
# [
#     "<root>",
#     "HogeStack",
#     "HogeStack/HogeBucket",
#     "HogeStack/HogeBucket/Resource [AWS::S3::Bucket]",
# ]


# ディストリビューションの L2 コンストラクト
distribution = cloudfront.Distribution(
    stack,
    "HogeDistribution",
    default_behavior=cloudfront.BehaviorOptions(origin=origins.S3Origin(bucket)),
)

# ここまでのコンストラクトツリーを表示する
# print([node.to_string() for node in app.node.find_all()])
# [
#     "<root>",
#     "HogeStack",
#     "HogeStack/HogeBucket",
#     "HogeStack/HogeBucket/Resource [AWS::S3::Bucket]",
#     "HogeStack/HogeBucket/Policy",
#     "HogeStack/HogeBucket/Policy/Resource [AWS::S3::BucketPolicy]",
#     "HogeStack/HogeDistribution",
#     "HogeStack/HogeDistribution/Origin1",
#     "HogeStack/HogeDistribution/Origin1/S3Origin",
#     "HogeStack/HogeDistribution/Origin1/S3Origin/Resource [AWS::CloudFront::CloudFrontOriginAccessIdentity]",
#     "HogeStack/HogeDistribution/Resource [AWS::CloudFront::Distribution]",
# ]

# S3Origin にアクセスする
oai: cloudfront.OriginAccessIdentity = distribution.node.find_child("Origin1").node.find_child("S3Origin")
# print(oai.to_string())
# HogeStack/HogeDistribution/Origin1/S3Origin

# （おまけ）　OAIを使ってポリシーを作成して、バケットに付与する
from aws_cdk import aws_iam as iam

policy = iam.PolicyStatement(
    effect=iam.Effect.ALLOW,
    principals=[iam.CanonicalUserPrincipal(oai.cloud_front_origin_access_identity_s3_canonical_user_id)],
    resources=[bucket.bucket_arn],
    actions=["s3:ListBucket"],
)
bucket.add_to_resource_policy(policy)


app.synth()
