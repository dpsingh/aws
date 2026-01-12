import boto3
import csv
import sys

def create(row):
    # Define your AWS profile name (Account Selection B/w htmedia-primary (fabmarket), HH [default_hh])
    aws_profile_name = 'default'

    # Create a session with the AWS profile
    session = boto3.Session(profile_name=aws_profile_name)
    
    # Specify the Region Name Primary Account has Mumbai * Singapore Region and HH Account has Mumbai Region only
    regn_name = row['RegionName']

    # Initialize the Boto3 EC2 client
    ec2 = session.client('ec2',region_name=regn_name)

    # Specify the instance ID you want to add/update tags for
    instance_id = row['InstanceId']

    # Define the tags you want to add/update as a dictionary
    
    tags_to_add_update  = dict(row)
    #del tags_to_add_update['BusinessHead']
    # Get the existing tags for the instance (if any)

    # Create a list of tag updates, including both new and updated tags
    tag_updates = []
    for key, value in tags_to_add_update.items():
        tag_updates.append({'Key': key, 'Value': value})

    # Update the existing tags with the new/updated tags
    # Apply the tag updates to the instance
    #ec2.create_tags(Resources=[instance_id], Tags=tag_updates)
    ec2.create_tags(Resources=[instance_id], Tags=tag_updates)
    print(instance_id)
    instance_info = ec2.describe_instances(
            InstanceIds=[
                instance_id,
            ],
            DryRun=False
        )
    #print(instance_info)
    try:
        if (len(instance_info)):
            instance_reservations = instance_info['Reservations'][0]
            if 'Instances' in instance_reservations.keys():
                Instances = instance_reservations['Instances']
                if 'BlockDeviceMappings' in Instances[0].keys():
                    BlockDeviceMappings = Instances[0]['BlockDeviceMappings'][0]
                    for k in BlockDeviceMappings.keys():
                        if k == "Ebs" : 
                            VolumeId = BlockDeviceMappings['Ebs']['VolumeId']
                            print(VolumeId)
                            ec2.create_tags(Resources=[VolumeId], Tags=tag_updates)
    except:
        print("An exception occurred")
    '''
    print("Tags added/updated for instance {instance_id}:")
    for key, value in tag_updates.items():
        print(f"Key: {key}, Value: {value}")
    '''

#input_file = csv.DictReader(open(sys.argv[1]))
input_file = csv.DictReader(open("dev.csv"))
for row in input_file:
    create(row)
