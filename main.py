#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack
from cdktf_cdktf_provider_aws import AwsProvider, kms, datasources

class MyStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        # define resources here
        myregion = "us-east-1"
        AwsProvider(self, "aws", region=myregion)

        datasources.DataAwsCallerIdentity(self, "aws_id")

        policy = """{
        "Version": "2012-10-17",
        "Statement": [
          {
            "Sid": "Enable IAM User Permissions",
            "Effect": "Allow",
            "Principal": {
              "AWS": "arn:aws:iam::${awsAccountid.id}:root"
          },
            "Action": [
              "kms:*"
            ],
            "Resource": [
              "*"
            ]
          },    {
            "Sid": "Allow autoscalling to use the key",
            "Effect": "Allow",
            "Principal": {
              "AWS": [
                "arn:aws:iam::${awsAccountid.id}:role/aws-service-role/autoscaling.amazonaws.com/AWSServiceRoleForAutoScaling"
              ]
            },
            "Action": [
                "kms:Create*",
                "kms:Describe*",
                "kms:Enable*",
                "kms:List*",
                "kms:Put*",
                "kms:Update*",
                "kms:Revoke*",
                "kms:Disable*",
                "kms:Get*",
                "kms:Delete*",
                "kms:TagResource",
                "kms:UntagResource",
                "kms:ScheduleKeyDeletion",
                "kms:CancelKeyDeletion"
            ],
            "Resource": "*"
          },{
            "Sid": "Allow use of the key",
            "Effect": "Allow",
            "Principal": {
                "AWS": [
                "arn:aws:iam::${awsAccountid.id}:role/aws-service-role/autoscaling.amazonaws.com/AWSServiceRoleForAutoScaling"
                ]
            },
            "Action": [
                "kms:Encrypt",
                "kms:Decrypt",
                "kms:ReEncrypt*",
                "kms:GenerateDataKey*",
                "kms:DescribeKey"
            ],
            "Resource": "*"
            },        {
              "Sid": "Allow attachment of persistent resources",
              "Effect": "Allow",
              "Principal": {
                  "AWS": [
              "arn:aws:iam::${awsAccountid.id}:role/aws-service-role/autoscaling.amazonaws.com/AWSServiceRoleForAutoScaling"
              ]
              },
              "Action": [
                  "kms:CreateGrant",
                  "kms:ListGrants",
                  "kms:RevokeGrant"
              ],
              "Resource": "*",
              "Condition": {
                  "Bool": {
                      "kms:GrantIsForAWSResource": "true"
                  }
              }
          }
        ]
      }"""
        mykmskey=kms.KmsKey(self, "aws_kms",enable_key_rotation=True, policy=policy,tags={"Name": "CDKtf-python-Demo-KMS-key"})

        kms.KmsAlias(self, "kms_alias", target_key_id=mykmskey.id)

app = App()
MyStack(app, "cdktf-python-aws-kms")

app.synth()
