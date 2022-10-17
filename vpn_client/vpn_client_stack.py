from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
import aws_cdk as cdk
import aws_cdk.aws_ec2 as ec2
# import aws_cdk.aws_ec2.ClientVpnEndpoint as vpn
            
from constructs import Construct

class VpnClientStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Client VPN VPC
        self.vpc = ec2.Vpc(self, "ClientVPNVPC",
                           max_azs=1,
                           cidr="192.168.0.0/16",
                           subnet_configuration=[ 
                           ec2.SubnetConfiguration(
                               subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                               name="PrivateSubnetVPNTarget",
                               cidr_mask=24
                           )                           
                           ]
                        )

        # Create VPN Endpoint and Associate with VPC
        self.endpoint = self.vpc.add_client_vpn_endpoint("VPNClientEndpoint",
            cidr="10.10.0.0/16",
            server_certificate_arn="arn:aws:acm:ap-southeast-2:915922766016:certificate/1d88cc91-aa0c-4a2e-b2fc-86a4e96ab358",
            client_certificate_arn="arn:aws:acm:ap-southeast-2:915922766016:certificate/b4abb268-abeb-4153-81dd-467378f6e404",
            logging=False  
        )

        # Create new public subnet and add to VPC
        self.private_subnet = self.vpc.select_subnets(subnet_group_name="PrivateSubnetVPNTarget").subnets[0]
        self.public_subnet = ec2.PublicSubnet(self, "PublicSubnetVPNApp",
            vpc_id=self.vpc.vpc_id,
            availability_zone=self.private_subnet.availability_zone,
            cidr_block='192.168.100.0/24')
        

