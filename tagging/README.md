AWS EC2 & EBS Tagging Automation Script

Overview
--------
This Python script automates the process of adding or updating tags on AWS EC2 instances and their attached EBS volumes using data provided in a CSV file.
It reads instance details from the CSV, applies tags to the EC2 instance, and also propagates the same tags to the associated EBS volume.

The script uses Boto3, the AWS SDK for Python, and works with AWS CLI profiles for account selection.

Features
--------
• Reads tagging data from a CSV file
• Supports multiple AWS regions
• Adds/updates tags on:
	◦EC2 instances
	◦Attached EBS volumes

• Uses AWS named profiles for secure authentication
• Simple and reusable for bulk tagging operations

Prerequisites
-------------
Before running the script, ensure the following are set up:

• Python 3.x
• AWS CLI installed
• Boto3 installed: pip install boto3
• AWS credentials configured

aws configure
or via named profiles in:
~/.aws/credentials
~/.aws/config

AWS Profile Configuration
-------------------------
The script uses an AWS profile:

aws_profile_name = 'default'

CSV File Format
---------------
The script expects a CSV file (e.g., dev.csv) with column headers matching tag keys.

Required Columns

InstanceId – EC2 instance ID

RegionName – AWS region where the instance exists

Example CSV (ec2-tags.csv)
InstanceId,RegionName,Environment,Owner,Project
i-0123456789abcdef0,ap-south-1,Dev,CloudTeam,MyApp
i-0abcdef1234567890,ap-southeast-1,Prod,InfraTeam,Backend


⚠️ All columns (except InstanceId and RegionName) will be treated as tags.

How the Script Works
--------------------
• Reads each row from the CSV file
• Creates a Boto3 session using the specified AWS profile
• Connects to EC2 in the specified region
• Applies tags to the EC2 instance
• Retrieves attached EBS volume information
• Applies the same tags to the EBS volume

How to Run
----------
• Place the CSV file in the same directory as the script
• Update the CSV filename if needed:
input_file = csv.DictReader(open("dev.csv"))

• Execute the script:
python tag_ec2_instances.py

Output
------
• Prints the EC2 Instance ID after tagging
• Prints the associated EBS Volume ID
• Displays a message if an exception occurs

Error Handling
--------------
• The script uses a generic try-except block while fetching instance and volume details.
• If any issue occurs (e.g., missing permissions, invalid instance ID), it will print:
• An exception occurred

IAM Permissions Required
------------------------
• Ensure the IAM user/role has the following permissions:

{
  "Effect": "Allow",
  "Action": [
    "ec2:CreateTags",
    "ec2:DescribeInstances"
  ],
  "Resource": "*"
}

Notes
-----
• Existing tags with the same key will be updated
• New tags will be added
• The script currently tags only the first attached EBS volume
• Modify the script if multiple volumes need tagging

Disclaimer
----------
• Use this script carefully in production environments. Always validate CSV data and test in a non-production account first.
• Purpose: Bulk EC2 & EBS Tag Management using CSV input
