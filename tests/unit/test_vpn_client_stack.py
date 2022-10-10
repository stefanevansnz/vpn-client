import aws_cdk as core
import aws_cdk.assertions as assertions

from vpn_client.vpn_client_stack import VpnClientStack

# example tests. To run these tests, uncomment this file along with the example
# resource in vpn_client/vpn_client_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = VpnClientStack(app, "vpn-client")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
