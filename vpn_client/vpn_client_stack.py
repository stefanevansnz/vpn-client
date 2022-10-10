from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
import aws_cdk as cdk
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_ec2.ClientVpnEndpoint as vpn
            
from constructs import Construct

class VpnClientStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Client VPN VPC
        self.vpc = ec2.Vpc(self, "ClientVPNVPC",
                           max_azs=1,
                           cidr="192.168.0.0/16",
                           subnet_configuration=
                            [ ec2.SubnetConfiguration(
                               subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                               name="PrivateSubnetApp",
                               cidr_mask=24
                           ), ec2.SubnetConfiguration(
                               subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                               name="PrivateSubnetVPNTarget",
                               cidr_mask=24
                           )                           
                           ]
                        )

        # Create VPN Endpoint and Associate with VPC
        endpoint = self.vpc.add_client_vpn_endpoint("Endpoint",
            cidr="10.10.0.0/16",
            server_certificate_arn="arn:aws:acm:us-east-1:123456789012:certificate/server-certificate-id",
            user_based_authentication=ec2.ClientVpnUserBasedAuthentication.federated(saml_provider),
            authorize_all_users_to_vpc_cidr=False
        )

        endpoint.add_authorization_rule("Rule",
            cidr="10.0.10.0/32",
            group_id="group-id"
        )