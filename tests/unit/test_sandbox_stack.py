import aws_cdk as core
import aws_cdk.assertions as assertions

from sandbox.sandbox_stack import SandboxStack

# example tests. To run these tests, uncomment this file along with the example
# resource in sandbox/sandbox_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = SandboxStack(app, "sandbox")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
