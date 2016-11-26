__author__ = 'rakesh.varma'

import json

class cloudFormationFactory:

    name = None
    securityGroup = None
    keyName = None
    template = {
                        "Type": "AWS::EC2::Instance",
                        "Properties": {
                            "InstanceType": "t2.micro",
                            "SecurityGroups": [
                            {
                                "Ref": ""
                            }
                            ],
                            "KeyName": "",
                            "ImageId": "ami-a9d276c9",
                            "Tags" : [
                                {"Key" : "Name", "Value" : ""},
                            ]
                        },
                }

    def __init__(self, name, securityGroup, keyName):
        self.name = name
        self.securityGroup = securityGroup
        self.keyName = keyName

    def getEC2Json(self):
        self.template["Properties"]["SecurityGroups"][0]["Ref"] = self.securityGroup
        self.template["Properties"]["Tags"][0]["Value"] = self.name
        self.template["Properties"]["KeyName"] = self.keyName
        return self.template


c = cloudFormationFactory(name = 'namenode', securityGroup = 'HadoopSecurityGroup', keyName = 'testkey')
print c.getEC2Json()
