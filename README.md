
# AWS VPN Client using CDK
This is a project to use the CDK development with Python to create an AWS VPN Client Endpoint.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.


```
$ source .venv/bin/activate
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

```
nvm use --lts  
node 14

cdk deploy --profile sandpit \
--parameters ServerCertARN="arn:aws:acm:ap-southeast-2:915922766016:certificate/1d88cc91-aa0c-4a2e-b2fc-86a4e96ab358" \
--parameters ClientCertARN="arn:aws:acm:ap-southeast-2:915922766016:certificate/b4abb268-abeb-4153-81dd-467378f6e404"
```

```
cdk destroy --profile sandpit
```

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
