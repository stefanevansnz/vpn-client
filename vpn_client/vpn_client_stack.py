from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
import aws_cdk as cdk
import aws_cdk.aws_ec2 as ec2
            
from constructs import Construct

class VpnClientStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Parameters
        server_cert_arn= cdk.CfnParameter(self, "ServerCertARN", type="String", description="Server Cert ARN")
        client_cert_arn= cdk.CfnParameter(self, "ClientCertARN", type="String", description="Client Cert ARN")        

        # Client VPN VPC
        self.vpc = ec2.Vpc(self, "ClientVPNVPC",
                           max_azs=1,
                           cidr="192.168.0.0/16",
                           subnet_configuration=[ 
                           ec2.SubnetConfiguration (
                               subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                               name="PrivateSubnetVPNTarget",
                               cidr_mask=24
                               )                           
                           ]
        )

        # Save private subnet details
        self.private_subnet = self.vpc.select_subnets(subnet_group_name="PrivateSubnetVPNTarget").subnets[0]

        # Create VPN Endpoint and Associate with VPC
        self.endpoint = self.vpc.add_client_vpn_endpoint("VPNClientEndpoint",
            cidr="10.10.0.0/16",
            server_certificate_arn=server_cert_arn.value_as_string,
            client_certificate_arn=client_cert_arn.value_as_string,
            logging=False  
        )

        # Create new public subnet and add to VPC
        self.public_subnet = ec2.PublicSubnet(self, "PublicSubnetVPNApp",
            vpc_id=self.vpc.vpc_id,
            availability_zone='ap-southeast-2c',
            cidr_block='192.168.100.0/24'
        )
        # Associate Public Subnet with VPN Client endpoint
        self.clientvpnassoc = ec2.CfnClientVpnTargetNetworkAssociation(self, "ClientVPNAssociation",
            client_vpn_endpoint_id=self.endpoint.endpoint_id,
            subnet_id=self.public_subnet.subnet_id
        )                

        # Create IGW and add to public subnet
        self.igw = ec2.CfnInternetGateway(self, "InternetGateway")
        self.vpc_gateway_attachment = ec2.CfnVPCGatewayAttachment(self, "VPCGatewayAttachment",
            vpc_id=self.vpc.vpc_id,
            internet_gateway_id=self.igw.ref)
        self.public_subnet.add_default_internet_route(
            gateway_id=self.igw.ref,
            gateway_attachment=self.vpc_gateway_attachment,            
        )

        # Allow internet through the VPN Endpoint
        self.endpoint.add_authorization_rule("Rule",
            cidr="0.0.0.0/0"
        )
    
        # Route internet traffic to public subnet        
        self.endpoint.add_route("VPNEndpointInternetRoute",
            cidr="0.0.0.0/0",
            target=ec2.ClientVpnRouteTarget.subnet(self.public_subnet)
        )
        
        

