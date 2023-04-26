# python app.py

import aws_cdk as cdk
from aws_cdk import aws_ec2

app = cdk.App()
stack = cdk.Stack(app, "HogeStack")

# vpc の L2 コンストラクト
vpc = aws_ec2.Vpc(
    stack,
    "HogeVpc",
    cidr="10.123.0.0/16",
    max_azs=1,
    subnet_configuration=[
        aws_ec2.SubnetConfiguration(
            name="HogePublicSubnet",
            subnet_type=aws_ec2.SubnetType.PUBLIC,
        ),
        aws_ec2.SubnetConfiguration(
            name="HogePrivateSubnet",
            subnet_type=aws_ec2.SubnetType.PRIVATE_WITH_NAT,
        ),
    ],
)

# ここまでのコンストラクトツリーを表示する
print([node.to_string() for node in app.node.find_all()])
# [
#     "<root>",
#     "HogeStack",
#     "HogeStack/HogeVpc",
#     "HogeStack/HogeVpc/Resource [AWS::EC2::VPC]",
#     "HogeStack/HogeVpc/HogePublicSubnetSubnet1",
#     "HogeStack/HogeVpc/HogePublicSubnetSubnet1/Subnet [AWS::EC2::Subnet]",
#     "HogeStack/HogeVpc/HogePublicSubnetSubnet1/Acl",
#     "HogeStack/HogeVpc/HogePublicSubnetSubnet1/RouteTable [AWS::EC2::RouteTable]",
#     "HogeStack/HogeVpc/HogePublicSubnetSubnet1/RouteTableAssociation [AWS::EC2::SubnetRouteTableAssociation]",
#     "HogeStack/HogeVpc/HogePublicSubnetSubnet1/DefaultRoute [AWS::EC2::Route]",
#     "HogeStack/HogeVpc/HogePublicSubnetSubnet1/EIP [AWS::EC2::EIP]",
#     "HogeStack/HogeVpc/HogePublicSubnetSubnet1/NATGateway [AWS::EC2::NatGateway]",
#     "HogeStack/HogeVpc/HogePrivateSubnetSubnet1",
#     "HogeStack/HogeVpc/HogePrivateSubnetSubnet1/Subnet [AWS::EC2::Subnet]",
#     "HogeStack/HogeVpc/HogePrivateSubnetSubnet1/Acl",
#     "HogeStack/HogeVpc/HogePrivateSubnetSubnet1/RouteTable [AWS::EC2::RouteTable]",
#     "HogeStack/HogeVpc/HogePrivateSubnetSubnet1/RouteTableAssociation [AWS::EC2::SubnetRouteTableAssociation]",
#     "HogeStack/HogeVpc/HogePrivateSubnetSubnet1/DefaultRoute [AWS::EC2::Route]",
#     "HogeStack/HogeVpc/IGW [AWS::EC2::InternetGateway]",
#     "HogeStack/HogeVpc/VPCGW [AWS::EC2::VPCGatewayAttachment]",
# ]

# パブリックサブネットを取り出してみる
hoge_public_subnet_subnet_1: aws_ec2.CfnSubnet = vpc.node.find_child("HogePublicSubnetSubnet1").node.find_child(
    "Subnet"
)
print(hoge_public_subnet_subnet_1.to_string())
# 'HogeStack/HogeVpc/HogePublicSubnetSubnet1/Subnet [AWS::EC2::Subnet]'

# 　サブネットを修正する
hoge_public_subnet_subnet_1.cidr_block = "10.123.1.0/24"

app.synth()
