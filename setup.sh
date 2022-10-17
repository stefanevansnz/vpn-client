git clone https://github.com/OpenVPN/easy-rsa.git
cd easy-rsa/easyrsa3/

./easyrsa init-pki
./easyrsa build-ca nopass
./easyrsa build-server-full server nopass
./easyrsa build-client-full client1.domain.tld nopass

mkdir ../awscerts
cp pki/ca.crt ../awscerts/
cp pki/issued/server.crt ../awscerts
cp pki/private/server.key ../awscerts/
cp pki/issued/client1.domain.tld.crt ../awscerts/
cp pki/private/client1.domain.tld.key ../awscerts/
cd ../awscerts/

aws acm import-certificate --certificate fileb://server.crt --private-key fileb://server.key --certificate-chain fileb://ca.crt --region ap-southeast-2 --profile sandpit

aws acm import-certificate --certificate fileb://client1.domain.tld.crt --private-key fileb://client1.domain.tld.key --certificate-chain fileb://ca.crt --region ap-southeast-2 --profile sandpit

cd ../..
cdk deploy --profile sandpit

