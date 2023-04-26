# python app.py

import aws_cdk as cdk
from aws_cdk import aws_lambda as lambda_

app = cdk.App()
stack = cdk.Stack(app, "HogeStack")

# Lambda　の L2 コンストラクト
hoge_function = lambda_.Function(
    stack,
    "HogeFunction",
    code=lambda_.Code.from_inline("def handler(event, context): return 'Hello, World!'"),
    runtime=lambda_.Runtime.PYTHON_3_9,
    handler="index.handler",
)

# ここまでのコンストラクトツリーを表示する
print([node.to_string() for node in app.node.find_all()])
# [
#     "<root>",
#     "HogeStack",
#     "HogeStack/HogeFunction",
#     "HogeStack/HogeFunction/ServiceRole",
#     "HogeStack/HogeFunction/ServiceRole/ImportServiceRole",
#     "HogeStack/HogeFunction/ServiceRole/Resource [AWS::IAM::Role]",
#     "HogeStack/HogeFunction/Resource [AWS::Lambda::Function]",
# ]

# ServiceRole にアクセスする
print(hoge_function.role.to_string())
# 'HogeStack/HogeFunction/ServiceRole'

# ImportServiceRoleにアクセスする
print(hoge_function.role.node.find_child("ImportServiceRole").to_string())
print(hoge_function.node.find_child("ServiceRole").node.find_child("ImportServiceRole").to_string())
# 'HogeStack/HogeFunction/ServiceRole/ImportServiceRole'

app.synth()
